"""BikeDemand : collecte, analyse et prévision calendaire J+1 sans météo future."""
from pathlib import Path
import json, zipfile, hashlib, urllib.request, platform
import numpy as np
import pandas as pd
import sklearn, joblib, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
P=Path(__file__).resolve().parent
for d in ['raw','collected','analysis','models','reports']: (P/d).mkdir(exist_ok=True)
url='https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip'
f=P/'raw/source.zip'
if not f.exists(): urllib.request.urlretrieve(url,f)
with zipfile.ZipFile(f) as z:
    df=pd.read_csv(z.open('hour.csv')); readme=z.read('Readme.txt').decode('utf-8',errors='replace')
(P/'reports/dictionnaire_source.txt').write_text(readme)
df['timestamp']=pd.to_datetime(df.dteday)+pd.to_timedelta(df.hr,unit='h')
df=df.sort_values('timestamp').reset_index(drop=True)
assert not df.isna().any().any() and df.timestamp.is_unique
assert (df.cnt==df.casual+df.registered).all() and (df.cnt>=0).all()
expected=pd.date_range(df.timestamp.min(),df.timestamp.max(),freq='h')
missing=expected.difference(df.timestamp)
df.to_csv(P/'collected/locations_horaires.csv',index=False)
quality={'lignes':len(df),'debut':str(df.timestamp.min()),'fin':str(df.timestamp.max()),'heures_absentes':len(missing),'valeurs_absentes':int(df.isna().sum().sum()),'doublons_horodatage':int(df.timestamp.duplicated().sum()),'total_locations':int(df.cnt.sum())}
(P/'reports/qualite.json').write_text(json.dumps(quality,indent=2))
pd.DataFrame({'timestamp':missing}).to_csv(P/'reports/heures_absentes.csv',index=False)
# Exploration descriptive uniquement ; aucune transformation apprise sur l'ensemble.
hour=df.groupby(['workingday','hr']).cnt.agg(['mean','median','count']).reset_index()
hour.to_csv(P/'analysis/profil_horaire.csv',index=False)
monthly=df.set_index('timestamp').cnt.resample('MS').agg(['sum','mean','count'])
monthly.to_csv(P/'analysis/mensuel.csv')
fig,ax=plt.subplots(figsize=(9,4))
for w,g in hour.groupby('workingday'): ax.plot(g.hr,g['mean'],label='Jour ouvré' if w else 'Week-end ou jour férié')
ax.set(title='Locations moyennes par heure — 2011–2012',xlabel='Heure locale du fichier source',ylabel='Locations / heure');ax.legend();ax.set_xlim(0,23);ax.set_ylim(bottom=0);fig.tight_layout();fig.savefig(P/'analysis/profil_horaire.png',dpi=160);plt.close(fig)
# Prévision J+1 : calendrier connu uniquement ; pas de cnt décalé, ni météo réalisée.
features=['hr','weekday','mnth','workingday','holiday','yr']
train=df.timestamp<pd.Timestamp('2012-07-01');val=(df.timestamp>=pd.Timestamp('2012-07-01'))&(df.timestamp<pd.Timestamp('2012-10-01'));test=df.timestamp>=pd.Timestamp('2012-10-01')
def make_model(name):
    enc=ColumnTransformer([('calendrier',OneHotEncoder(handle_unknown='ignore',sparse_output=False),features)],remainder='drop')
    return make_pipeline(enc,Ridge(alpha=10) if name=='Ridge' else HistGradientBoostingRegressor(max_iter=150,max_leaf_nodes=15,l2_regularization=10,random_state=42))
def score(y,p): return {'MAE':float(mean_absolute_error(y,p)),'RMSE':float(np.sqrt(mean_squared_error(y,p))),'R2':float(r2_score(y,p))}
def baseline(frame,mask):
    med=frame.groupby(['weekday','hr']).cnt.median()
    return np.array([med.get((r.weekday,r.hr),frame.cnt.median()) for r in df.loc[mask].itertuples()])
rows=[]; models={}
for name in ['Ridge','Boosting']:
    m=make_model(name);m.fit(df.loc[train,features],df.loc[train,'cnt']);models[name]=m
    for split,mask in [('entrainement',train),('validation',val)]:rows.append({'modele':name,'ensemble':split,**score(df.loc[mask,'cnt'],np.maximum(0,m.predict(df.loc[mask,features])))})
rows.append({'modele':'Mediane_jour_heure','ensemble':'validation',**score(df.loc[val,'cnt'],baseline(df.loc[train],val))})
winner=min([r for r in rows if r['ensemble']=='validation'],key=lambda r:r['MAE'])['modele']
final_train=train|val
ref=baseline(df.loc[final_train],test)
if winner=='Mediane_jour_heure':
    final={'type':'mediane','table':df.loc[final_train].groupby(['weekday','hr']).cnt.median().to_dict(),'fallback':float(df.loc[final_train,'cnt'].median())};pred=ref
else:
    final=make_model(winner);final.fit(df.loc[final_train,features],df.loc[final_train,'cnt']);pred=np.maximum(0,final.predict(df.loc[test,features]))
rows.append({'modele':'Mediane_jour_heure','ensemble':'test',**score(df.loc[test,'cnt'],ref)})
if winner!='Mediane_jour_heure': rows.append({'modele':winner,'ensemble':'test',**score(df.loc[test,'cnt'],pred)})
results=pd.DataFrame(rows);results.to_csv(P/'models/resultats.csv',index=False)
joblib.dump(final,P/'models/pipeline.joblib',compress=3)
loaded=joblib.load(P/'models/pipeline.joblib') # fichier créé par ce script uniquement
if winner!='Mediane_jour_heure': np.testing.assert_allclose(np.maximum(0,loaded.predict(df.loc[test,features].head(10))),pred[:10])
preds=df.loc[test,['timestamp','cnt','hr','workingday']].copy();preds['prediction']=pred;preds['reference']=ref;preds['erreur_absolue']=abs(preds.cnt-pred);preds.to_csv(P/'models/predictions_test.csv',index=False)
preds.groupby(['workingday','hr']).erreur_absolue.agg(['mean','count']).to_csv(P/'models/erreurs_par_groupe.csv')
fig,ax=plt.subplots(figsize=(9,4));day=preds.set_index('timestamp')[['cnt','prediction']].resample('D').sum(min_count=1);ax.plot(day.index,day.cnt,label='Observé');ax.plot(day.index,day.prediction,label='Prévu');ax.set(title='Test final — octobre à décembre 2012',ylabel='Somme des heures présentes / jour');ax.legend();fig.autofmt_xdate();fig.tight_layout();fig.savefig(P/'models/test.png',dpi=160);plt.close(fig)
a=score(df.loc[test,'cnt'],pred);b=score(df.loc[test,'cnt'],ref);gain=100*(b['MAE']-a['MAE'])/b['MAE']
summary={'modele':winner,'test':a,'reference_test':b,'gain_mae_pct':gain,'decoupage':{'entrainement':int(train.sum()),'validation':int(val.sum()),'test':int(test.sum())},'versions':{'python':platform.python_version(),'pandas':pd.__version__,'scikit_learn':sklearn.__version__,'numpy':np.__version__,'joblib':joblib.__version__,'matplotlib':matplotlib.__version__},**quality}
(P/'models/bilan.json').write_text(json.dumps(summary,indent=2))
(P/'requirements.txt').write_text('\n'.join(f'{k.replace("_","-")}=={v}' for k,v in summary['versions'].items() if k!='python')+'\n')
report=f'''# BikeDemand — Junior BOOTO Waba

Prévision calendaire des locations horaires à J+1. Exécution des trois rôles dans un pipeline Python partagé ; aucun appel automatique aux GPT indépendants.

## Source et qualité
UCI Bike Sharing, Hadi Fanaee-T (2013), DOI 10.24432/C5W894, CC BY 4.0. Capital Bikeshare, 2011–2012. Source : {url}
{len(df):,} observations ; {len(missing)} heures absentes de la grille. Ces absences sont conservées et ne sont pas remplacées par des zéros. Leur origine n'est pas établie. Les totaux portent sur les heures présentes. Pas de valeurs manquantes dans les lignes observées, ni de doublons d'horodatage. Le fuseau n'est pas explicité dans les CSV : aucune conversion arbitraire.

## Analyse
Profil des jours ouvrés et non ouvrés, évolution mensuelle, sans interprétation causale. Les graphiques décrivent tout l'historique ; le choix de variables et le protocole étaient fixés avant l'entraînement.

## Modélisation
Variables : {', '.join(features)}. Calendrier connu à J+1. Météo réalisée exclue, ainsi que casual, registered, instant et la cible cnt. Aucune variable future ni transformation apprise sur le jeu complet.
Entraînement : janvier 2011–juin 2012 ({train.sum()} lignes). Validation : juillet–septembre 2012 ({val.sum()}). Test final : octobre–décembre 2012 ({test.sum()}). Comparaison de deux configurations fixées et d'une référence médiane par jour de semaine et heure. Encodage ajusté dans les pipelines. Sélection sur MAE validation, puis réentraînement jusqu'au 30 septembre. Aucun réglage sur le test. Prédictions négatives ramenées à zéro, règle fixée avant évaluation.
Modèle retenu : **{winner}**. MAE test **{a['MAE']:.2f} locations/heure**, RMSE {a['RMSE']:.2f}, R² {a['R2']:.3f}. Référence MAE {b['MAE']:.2f} ; gain {gain:.1f} %. Résultats complets : models/resultats.csv.
Export et rechargement vérifiés sur dix observations. Le modèle est un prototype historique, pas un service déployé ni une prévision de la demande actuelle. Le seul trimestre de test ne démontre pas une performance annuelle ; évolution de la demande et météo limitent cette approche calendaire. Les heures absentes peuvent biaiser l'évaluation.

## Reproduction
Python {platform.python_version()}. Installer requirements.txt puis lancer `python pipeline.py`. Le ZIP brut est conservé ; toutes les sorties sont régénérées dans ce dossier. Ne charger que les fichiers joblib de provenance fiable.
'''
(P/'README.md').write_text(report)
(P/'models/fiche_modele.md').write_text(report[report.index('## Modélisation'):])
manifest={'objectif':'Prévoir à J+1 les locations horaires à partir du calendrier connu','cible':'cnt','horizon':'J+1, calendrier uniquement','source':url,'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'etapes':{s:'completed' for s in ['DataCollect','DataAnalyse','DataML']},'fichiers':[str(x.relative_to(P)) for x in P.rglob('*') if x.is_file()],'transformations':['Horodatage date + heure','Tri chronologique','Aucune suppression/imputation','Encodage ajusté sur entraînement'],'erreurs':[],'prochaine_action':'Publication du prototype documenté'}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(summary,indent=2))
