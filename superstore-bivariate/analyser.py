"""Analyse descriptive bivariée, sans inférence causale ni tests sur lignes répétées."""
from pathlib import Path
import json,zipfile,hashlib,urllib.request,importlib.metadata
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
URL='https://www.tableau.com/sites/default/files/training/global_superstore.zip'
SHA='c37f715220c07f5be5279896d751c9988b7100cdc7a43dc30ddefd850fccbd1b'
NUM=['Sales','Profit','Discount','Quantity','Shipping Cost']
def main():
    for d in ['raw','collected','analysis','reports','models']:(ROOT/d).mkdir(exist_ok=True)
    archive=ROOT/'raw/source.zip'
    if not archive.exists():urllib.request.urlretrieve(URL,archive)
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==SHA
    with zipfile.ZipFile(archive) as z:(ROOT/'raw/source.xls').write_bytes(z.read('Global Superstore.xls'))
    data=pd.read_excel(ROOT/'raw/source.xls',sheet_name='Orders')
    fields=['Row ID','Order ID','Market','Region','Category','Sub-Category']+NUM
    assert len(data)==51290 and data['Row ID'].is_unique and not data[fields].isna().any().any()
    assert np.isfinite(data[NUM].to_numpy()).all() and data.Discount.between(0,1).all() and data.Sales.gt(0).all()
    assert abs(data.Sales.sum()-12642501.90988)<.001 and abs(data.Profit.sum()-1467457.29128)<.001
    orders=data[['Market','Order ID']].drop_duplicates().shape[0];assert orders==25072
    contingency=pd.crosstab(data.Market,data.Category)
    contingency.to_csv(ROOT/'analysis/effectifs_marche_categorie.csv')
    row_shares=contingency.div(contingency.sum(axis=1),axis=0);row_shares.to_csv(ROOT/'analysis/parts_categorie_dans_marche.csv')
    observed=contingency.to_numpy();n=observed.sum();expected=observed.sum(axis=1)[:,None]*observed.sum(axis=0)[None,:]/n
    chi_square=float(((observed-expected)**2/expected).sum())
    v=float(np.sqrt(chi_square/(n*min(observed.shape[0]-1,observed.shape[1]-1))))
    def summarize(group):
        return group.agg(lines=('Sales','size'),sales=('Sales','sum'),profit=('Profit','sum'),sales_mean=('Sales','mean'),profit_mean=('Profit','mean'),profit_median=('Profit','median'),profit_q25=('Profit',lambda s:s.quantile(.25)),profit_q75=('Profit',lambda s:s.quantile(.75)),discount_mean=('Discount','mean'),loss_rate=('Profit',lambda s:s.lt(0).mean()))
    categories=summarize(data.groupby('Category'));categories['aggregate_margin']=categories.profit/categories.sales
    categories.to_csv(ROOT/'analysis/profils_categories.csv')
    cells=summarize(data.groupby(['Market','Category']));cells['aggregate_margin']=cells.profit/cells.sales;cells.to_csv(ROOT/'analysis/profils_marche_categorie.csv')
    regions=summarize(data.groupby(['Market','Region']));regions['aggregate_margin']=regions.profit/regions.sales;regions.to_csv(ROOT/'analysis/profils_regions.csv')
    data['DiscountBand']=np.select([data.Discount.eq(0),data.Discount.le(.2),data.Discount.le(.4)],['0 %',']0,20 %]',']20,40 %]'],default='>40 %')
    bands=summarize(data.groupby('DiscountBand'));bands['aggregate_margin']=bands.profit/bands.sales;bands.to_csv(ROOT/'analysis/profils_remises.csv')
    by_cat=summarize(data.groupby(['Category','DiscountBand']));by_cat['aggregate_margin']=by_cat.profit/by_cat.sales;by_cat.to_csv(ROOT/'analysis/remises_par_categorie.csv')
    pearson=data[NUM].corr(method='pearson');spearman=data[NUM].corr(method='spearman')
    pearson.to_csv(ROOT/'analysis/correlations_pearson.csv');spearman.to_csv(ROOT/'analysis/correlations_spearman.csv')
    within=[]
    for category,frame in data.groupby('Category'):
        within.append({'category':category,'lines':len(frame),'discount_profit_pearson':float(frame.Discount.corr(frame.Profit)),'discount_profit_spearman':float(frame.Discount.corr(frame.Profit,method='spearman'))})
    pd.DataFrame(within).to_csv(ROOT/'analysis/correlations_par_categorie.csv',index=False)
    for table in [categories,cells,regions,bands,by_cat]:
        assert int(table.lines.sum())==51290 and abs(table.sales.sum()-data.Sales.sum())<.001 and abs(table.profit.sum()-data.Profit.sum())<.001
    assert np.allclose(row_shares.sum(axis=1),1)
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    row_shares.plot.bar(stacked=True,ax=axes[0],color=['#167d8d','#7971ad','#c17d35']);axes[0].set(title='Catégories : parts des lignes par marché',ylabel='Part des lignes',xlabel='Marché');axes[0].tick_params(axis='x',rotation=45);axes[0].legend(fontsize=8)
    margins=cells.aggregate_margin.unstack();im=axes[1].imshow(margins,cmap='RdBu',vmin=-.2,vmax=.3,aspect='auto');axes[1].set(xticks=range(3),xticklabels=margins.columns,yticks=range(len(margins)),yticklabels=margins.index,title='Marge agrégée : bénéfice total / ventes totales')
    for i in range(len(margins)):
        for j in range(3):axes[1].text(j,i,f'{margins.iloc[i,j]*100:.1f} %',ha='center',va='center',fontsize=8)
    fig.colorbar(im,ax=axes[1],label='Ratio de marge');fig.tight_layout();fig.savefig(ROOT/'reports/marches_categories.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    im=axes[0].imshow(spearman,vmin=-1,vmax=1,cmap='RdBu');axes[0].set(xticks=range(5),xticklabels=NUM,yticks=range(5),yticklabels=NUM,title='Corrélations de Spearman · toutes les lignes');axes[0].tick_params(axis='x',rotation=45)
    for i in range(5):
        for j in range(5):axes[0].text(j,i,f'{spearman.iloc[i,j]:.2f}',ha='center',va='center',fontsize=9)
    fig.colorbar(im,ax=axes[0],fraction=.046)
    sample=data.sample(5000,random_state=42);axes[1].scatter(sample.Discount*100,sample.Profit,s=6,alpha=.25,color='#167d8d');axes[1].axhline(0,color='gray',ls='--');axes[1].set(xlabel='Remise (%)',ylabel='Bénéfice de ligne (UM)',title='Remise et bénéfice · échantillon visuel 5 000 lignes')
    fig.tight_layout();fig.savefig(ROOT/'reports/correlations.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,5));names=categories.index.tolist()
    axes[0].boxplot([data.loc[data.Category.eq(c),'Profit'] for c in names],tick_labels=names,showfliers=False);axes[0].axhline(0,color='gray',ls='--');axes[0].set(ylabel='Bénéfice de ligne (UM)',title='Bénéfices par catégorie · médiane et dispersion')
    names_b=['0 %',']0,20 %]',']20,40 %]','>40 %'];axes[1].bar(names_b,bands.reindex(names_b).loss_rate*100,color='#b56c4b');axes[1].set(ylabel='Lignes à bénéfice négatif (%)',xlabel='Tranche de remise',title='Fréquence des pertes par tranche de remise',ylim=(0,100));fig.text(.03,.015,'Boîtes : points au-delà des moustaches non affichés ; toutes les données sont conservées et utilisées dans les calculs.',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(ROOT/'reports/distributions.png',dpi=150);plt.close(fig)
    summary={'rows':51290,'orders':25072,'sales':float(data.Sales.sum()),'profit':float(data.Profit.sum()),'aggregate_margin':float(data.Profit.sum()/data.Sales.sum()),'loss_rate':float(data.Profit.lt(0).mean()),'cramers_v_market_category':v,'discount_profit_pearson':float(pearson.loc['Discount','Profit']),'discount_profit_spearman':float(spearman.loc['Discount','Profit']),'categories':categories.reset_index().to_dict('records'),'discount_bands':bands.reset_index().to_dict('records'),'within_category_correlations':within}
    (ROOT/'reports/resultats.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    versions={name:importlib.metadata.version(name) for name in ['pandas','numpy','matplotlib','scipy','xlrd']};(ROOT/'requirements.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
    manifest={'objective':'Projet 3 : analyse bivariée descriptive des performances commerciales Superstore.','source':URL,'archive_sha256':SHA,'steps':{'DataCollect':'completed','DataAnalyse':'completed','DataML':'skipped'},'reason_ml_skipped':'Description des associations, sans objectif prédictif.','unit_of_observation':'Ligne de commande, pas client indépendant','transformations':['Aucune suppression ni imputation','Tranches de remise fixes','Marges calculées comme ratio des totaux','Échantillon de 5000 pour un nuage visuel seulement'],'checks':['51290 Row ID uniques, 25072 clés Market/Order ID','Champs requis présents et numériques finis','Totaux réconciliés dans les tableaux groupés','Parts de tableau croisé totalisant 1 par marché'],'versions':versions,'limits':['Données fictives historiques 2011–2014','Commandes et clients répétés : pas de tests sur une indépendance supposée des lignes','Corrélations descriptives sans causalité','Bénéfice défini par la source, pas résultat net validé'],'next_action':'Examiner compositions et coûts avec contexte métier avant toute recommandation opérationnelle.'}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
