"""Prépare les indicateurs historiques Global Superstore et le dashboard web."""
from pathlib import Path
import pandas as pd
import numpy as np
import json, hashlib, urllib.request, zipfile, importlib.metadata

ROOT = Path(__file__).resolve().parent
URL = 'https://www.tableau.com/sites/default/files/training/global_superstore.zip'
DIMS = ['month','market','region','category','segment']

def main():
    for d in ['raw','collected','analysis','reports','web']:
        (ROOT/d).mkdir(exist_ok=True)
    source=ROOT/'raw'/'Global Superstore.xls'
    if not source.exists():
        archive=ROOT/'raw'/'source.zip'
        urllib.request.urlretrieve(URL, archive)
        with zipfile.ZipFile(archive) as z:
            source.write_bytes(z.read('Global Superstore.xls'))
    orders=pd.read_excel(source,sheet_name='Orders')
    returns=pd.read_excel(source,sheet_name='Returns')
    # Correspondance de libellé confirmée entre les deux tables source.
    returns['Market']=returns['Market'].replace({'United States':'US'})
    required=['Row ID','Order ID','Order Date','Market','Region','Category','Segment','Sales','Profit','Quantity']
    assert orders[required].isna().sum().sum()==0
    assert orders['Row ID'].is_unique and len(orders)==51290
    assert orders['Order Date'].notna().all()
    assert np.isfinite(orders[['Sales','Profit','Quantity']].to_numpy()).all()
    assert (orders['Sales']>=0).all() and (orders['Quantity']>0).all()
    assert not returns.duplicated(['Market','Order ID']).any()
    assert set(returns['Returned'])=={'Yes'}
    # Les clés de commande combinent marché et identifiant ; aucun nom de client n’est exporté.
    keys=orders[['Market','Order ID']].drop_duplicates().sort_values(['Market','Order ID'])
    keys['order_key']=range(1,len(keys)+1)
    known=returns.merge(keys,on=['Market','Order ID'],how='left',validate='one_to_one',indicator=True)
    unmatched=int(known['order_key'].isna().sum())
    assert unmatched==0
    data=orders.merge(keys,on=['Market','Order ID'],validate='many_to_one')
    data=data.merge(returns[['Market','Order ID','Returned']],on=['Market','Order ID'],how='left',validate='many_to_one')
    data['returned']=data['Returned'].eq('Yes')
    data['month']=data['Order Date'].dt.strftime('%Y-%m')
    data=data.rename(columns={'Market':'market','Region':'region','Category':'category','Segment':'segment','Sales':'sales','Profit':'profit','Quantity':'quantity'})
    data=data[DIMS+['order_key','sales','profit','quantity','returned']]
    data.to_csv(ROOT/'collected'/'ventes_preparees.csv',index=False)
    grouped=data.groupby(DIMS,sort=True,observed=True)
    cells=[]
    for dims, block in grouped:
        cells.append([*dims,float(block.sales.sum()),float(block.profit.sum()),int(block.quantity.sum()),len(block),sorted(block.order_key.unique().tolist()),sorted(block.loc[block.returned,'order_key'].unique().tolist())])
    payload={'schema':DIMS+['sales','profit','quantity','lines','orders','returned_orders'],'cells':cells,'source':URL,'period':[str(orders['Order Date'].min().date()),str(orders['Order Date'].max().date())],'unit':'unités monétaires du jeu (UM)','snapshot':'2011–2014 · Données fictives historiques'}
    (ROOT/'web'/'dashboard-data.json').write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')))
    summary={'lines':len(data),'orders':len(keys),'sales':float(data.sales.sum()),'profit':float(data.profit.sum()),'margin':float(data.profit.sum()/data.sales.sum()),'quantity':int(data.quantity.sum()),'returned_orders':int(data.loc[data.returned,'order_key'].nunique()),'unmatched_returns':unmatched,'period':payload['period'],'cells':len(cells)}
    assert np.isclose(sum(c[5] for c in cells),summary['sales'])
    assert np.isclose(sum(c[6] for c in cells),summary['profit'])
    for dimension in ['market','region','category']:
        table=data.groupby(dimension).agg(sales=('sales','sum'),profit=('profit','sum'),quantity=('quantity','sum'),orders=('order_key','nunique'))
        table['margin']=table.profit/table.sales
        table.to_csv(ROOT/'analysis'/f'par_{dimension}.csv')
        assert np.isclose(table.sales.sum(),summary['sales'])
    monthly=data.groupby('month').agg(sales=('sales','sum'),profit=('profit','sum'))
    assert len(monthly)==48
    monthly.to_csv(ROOT/'analysis'/'mensuel.csv')
    (ROOT/'reports'/'resultats.json').write_text(json.dumps(summary,indent=2))
    fixtures=[]
    for filters in [{},{'year':'2014'},{'market':'APAC'},{'category':'Furniture'},{'year':'2013','market':'EU','category':'Technology'},{'region':'Central','segment':'Consumer'},{'market':'US','category':'Office Supplies','segment':'Corporate'},{'market':'none'}]:
        frame=data
        for k,v in filters.items():frame=frame[frame.month.str[:4].eq(v)] if k=='year' else frame[frame[k].eq(v)]
        fixtures.append({'filters':filters,'expected':{'sales':float(frame.sales.sum()),'profit':float(frame.profit.sum()),'quantity':int(frame.quantity.sum()),'lines':len(frame),'orders':int(frame.order_key.nunique()),'returned':int(frame.loc[frame.returned,'order_key'].nunique())}})
    (ROOT/'reports'/'verification_filtres.json').write_text(json.dumps(fixtures))
    versions={n:importlib.metadata.version(n) for n in ['pandas','numpy','xlrd']}
    (ROOT/'requirements.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
    manifest={'objective':'Tableau de bord historique des performances commerciales, projet 7','source':URL,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_sheets':['Orders','Returns'],'collection_date':'2026-10-11','unit':payload['unit'],'steps':{'DataCollect':'completed','DataAnalyse':'completed','DataML':'skipped'},'reason_ml_skipped':'Pas de demande prédictive ; indicateurs descriptifs suffisants.','transformations':['Données brutes préservées','Harmonisation Returns.Market : United States -> US (296 retours)', 'Jointure Returns sur Market + Order ID, many_to_one, sans multiplication','Clé interne de commande, aucun nom de client exporté','Agrégation mois/marché/région/catégorie/segment, clés de commande pour décompte distinct sous filtres'],'checks':['51290 Row ID uniques et champs requis présents','1173 retours reliés aux commandes','Ventes et bénéfices réconciliés par dimension','48 mois présents'],'versions':versions,'redistribution':'Classeur source non redistribué : conditions spécifiques non identifiées. URL et script de collecte fournis.','next_action':'Explorer les filtres ; aucune connexion temps réel configurée.'}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
