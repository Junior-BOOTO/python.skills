"""Régressions linéaires avec test géographique indépendant des choix de modèle."""
from pathlib import Path
import json,hashlib,urllib.request,tarfile,importlib.metadata
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import GroupShuffleSplit,GroupKFold,cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression,Ridge
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error,root_mean_squared_error,r2_score
ROOT=Path(__file__).resolve().parent
FEATURES=['MedInc','HouseAge','AveRooms','AveBedrms','Population','AveOccup','Latitude','Longitude']
URL='https://ndownloader.figshare.com/files/5976036'
SHA='aaa5c9a6afe2225cc2aed2723682ae403280c4a3695a2ddda4ffb5d8215ea681'
SEED=42
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2))
def collect():
    path=ROOT/'raw'/'cal_housing.tgz'
    if not path.exists():urllib.request.urlretrieve(URL,path)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==SHA
    with tarfile.open(path) as archive:
        with archive.extractfile('CaliforniaHousing/cal_housing.data') as file:
            original=np.loadtxt(file,delimiter=',')
    # Transformations du jeu scikit-learn à partir de l’archive originale.
    frame=pd.DataFrame({'MedInc':original[:,7],'HouseAge':original[:,2],
        'AveRooms':original[:,3]/original[:,6],'AveBedrms':original[:,4]/original[:,6],
        'Population':original[:,5],'AveOccup':original[:,5]/original[:,6],
        'Latitude':original[:,1],'Longitude':original[:,0],'MedHouseVal':original[:,8]/100000})
    path=ROOT/'raw'/'california.csv'
    if path.exists():assert np.allclose(pd.read_csv(path).to_numpy(),frame.to_numpy(),rtol=1e-12)
    else:frame.to_csv(path,index=False)
    return frame
def score(y,prediction):
    return {'MAE_USD_1990':float(mean_absolute_error(y,prediction)),
            'RMSE_USD_1990':float(root_mean_squared_error(y,prediction)),
            'R2':float(r2_score(y,prediction))}
def main():
    for d in ['raw','collected','analysis','models','reports']:(ROOT/d).mkdir(exist_ok=True)
    df=collect();assert len(df)==20640 and df.isna().sum().sum()==0
    assert np.isfinite(df.to_numpy()).all() and df.MedHouseVal.gt(0).all()
    groups=(np.floor(df.Latitude/.5).astype(int).astype(str)+'_'+np.floor(df.Longitude/.5).astype(int).astype(str)).to_numpy()
    dev,test=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=SEED).split(df,groups=groups))
    assert not set(groups[dev]) & set(groups[test])
    X=df[FEATURES];y=df.MedHouseVal.to_numpy()*100000
    # Exploration des distributions réservée au développement ; le test ne choisit aucun réglage.
    df.iloc[dev].describe().to_csv(ROOT/'analysis'/'statistiques_developpement.csv')
    split=pd.DataFrame({'row':np.arange(len(df)),'cell':groups,'partition':np.where(np.isin(np.arange(len(df)),test),'test','development')})
    split.to_csv(ROOT/'collected'/'decoupage.csv',index=False)
    cv=GroupKFold(n_splits=4,shuffle=True,random_state=SEED)
    folds=list(cv.split(X.iloc[dev],y[dev],groups[dev]))
    for train,val in folds:assert not set(groups[dev][train])&set(groups[dev][val])
    candidates=[('Reference_moyenne',FEATURES,DummyRegressor(strategy='mean')),
                ('Lineaire_simple_revenu',['MedInc'],Pipeline([('scale',StandardScaler()),('regression',LinearRegression())])),
                ('Lineaire_multiple',FEATURES,Pipeline([('scale',StandardScaler()),('regression',LinearRegression())]))]
    for alpha in [.1,1,10,100]:candidates.append((f'Ridge_alpha_{alpha}',FEATURES,Pipeline([('scale',StandardScaler()),('regression',Ridge(alpha=alpha))])))
    cv_results=[]
    for name,features,model in candidates:
        scores=cross_validate(model,X.iloc[dev][features],y[dev],cv=folds,scoring={'mae':'neg_mean_absolute_error','rmse':'neg_root_mean_squared_error','r2':'r2'},n_jobs=1)
        cv_results.append({'model':name,'MAE_mean':float(-scores['test_mae'].mean()),'MAE_std_between_folds':float(scores['test_mae'].std()),'RMSE_mean':float(-scores['test_rmse'].mean()),'R2_mean':float(scores['test_r2'].mean())})
    pd.DataFrame(cv_results).to_csv(ROOT/'analysis'/'validation_croisee.csv',index=False)
    chosen=min(cv_results,key=lambda r:r['MAE_mean'])['model']
    name,features,model=next(c for c in candidates if c[0]==chosen)
    if name=='Reference_moyenne':raise RuntimeError('Les modèles linéaires ne dépassent pas la référence en validation ; conserver la référence sans export linéaire.')
    model.fit(X.iloc[dev][features],y[dev])
    baseline=DummyRegressor(strategy='mean').fit(X.iloc[dev],y[dev])
    # Test final après sélection, uniquement modèle retenu et référence.
    prediction=model.predict(X.iloc[test][features]);reference=baseline.predict(X.iloc[test])
    final=[{'model':chosen,'partition':'test',**score(y[test],prediction)},
           {'model':'Reference_moyenne','partition':'test',**score(y[test],reference)},
           {'model':chosen,'partition':'development_fit',**score(y[dev],model.predict(X.iloc[dev][features]))}]
    pd.DataFrame(final).to_csv(ROOT/'analysis'/'scores_finaux.csv',index=False)
    pd.DataFrame({'row':test,'observed_usd_1990':y[test],'predicted_usd_1990':prediction,'residual_observed_minus_predicted':y[test]-prediction}).to_csv(ROOT/'analysis'/'predictions_test.csv',index=False)
    residual=y[test]-prediction
    segments=[]
    for label,mask in [('cible_au_plafond',np.isclose(y[test],500001)),('cible_sous_plafond',~np.isclose(y[test],500001))]:
        segments.append({'scope':label,'count':int(mask.sum()),'MAE':float(np.abs(residual[mask]).mean()),'mean_residual':float(residual[mask].mean())})
    pd.DataFrame(segments).to_csv(ROOT/'analysis'/'erreurs_par_plafond.csv',index=False)
    transform=model.named_steps['scale'];reg=model.named_steps['regression']
    coefficient=reg.coef_/transform.scale_;intercept=reg.intercept_-np.sum(reg.coef_*transform.mean_/transform.scale_)
    pd.DataFrame({'feature':features,'coefficient_original_units':coefficient,'coefficient_one_training_std':reg.coef_}).to_csv(ROOT/'analysis'/'coefficients.csv',index=False)
    exported={'model':chosen,'features':features,'mean':transform.mean_.tolist(),'scale':transform.scale_.tolist(),'coefficients_standardized':reg.coef_.tolist(),'intercept_standardized':float(reg.intercept_),'coefficients_original':coefficient.tolist(),'intercept_original':float(intercept),'target_unit':'USD de 1990, valeur médiane par zone','training_min':X.iloc[dev][features].min().to_dict(),'training_max':X.iloc[dev][features].max().to_dict()}
    save(ROOT/'models'/'regression.json',exported)
    reloaded=json.loads((ROOT/'models'/'regression.json').read_text())
    recovered=((X.iloc[test][features].to_numpy()-np.array(reloaded['mean']))/np.array(reloaded['scale']))@np.array(reloaded['coefficients_standardized'])+reloaded['intercept_standardized']
    assert np.allclose(recovered,prediction,atol=1e-7)
    examples=X.iloc[dev][features].median().to_numpy()
    # Médianes marginales assemblées : profil synthétique, pas observation de maison.
    save(ROOT/'reports'/'exemple_synthetique.json',{'input':dict(zip(features,examples.tolist())),'prediction':float(model.predict(pd.DataFrame([examples],columns=features))[0]),'synthetic':True})
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(10,6))
    ordered=sorted(cv_results,key=lambda r:r['MAE_mean']);ax.barh([r['model'] for r in ordered],[r['MAE_mean'] for r in ordered],xerr=[r['MAE_std_between_folds'] for r in ordered],color='#167d8d');ax.invert_yaxis();ax.set(xlabel='MAE en USD de 1990 (barres : écart-type entre plis)',title='Validation croisée géographique · 4 plis, développement uniquement');fig.tight_layout();fig.savefig(ROOT/'reports'/'comparaison.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,5));axes[0].scatter(y[test]/1000,prediction/1000,s=7,alpha=.3,color='#167d8d');limits=[min(0,float(prediction.min()/1000)),max(float(y[test].max()/1000),float(prediction.max()/1000))];axes[0].plot(limits,limits,'--',color='gray');axes[0].set(xlabel='Valeur observée (milliers USD de 1990)',ylabel='Valeur estimée (milliers USD de 1990)',title='Test : observations et estimations');axes[1].scatter(prediction/1000,residual/1000,s=7,alpha=.3,color='#bf6651');axes[1].axhline(0,color='gray',ls='--');axes[1].set(xlabel='Valeur estimée (milliers USD de 1990)',ylabel='Résidu observé − estimé (milliers USD)',title='Test : erreurs et dispersion');fig.tight_layout();fig.savefig(ROOT/'reports'/'erreurs.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,7))
    ax.scatter(df.Longitude.iloc[dev],df.Latitude.iloc[dev],s=2,alpha=.25,label='Développement',color='#167d8d');ax.scatter(df.Longitude.iloc[test],df.Latitude.iloc[test],s=3,alpha=.55,label='Test',color='#bf6651');ax.set(xlabel='Longitude (degrés)',ylabel='Latitude (degrés)',title='Séparation par cellules géographiques de 0,5°');ax.legend(markerscale=4);fig.tight_layout();fig.savefig(ROOT/'reports'/'decoupage.png',dpi=150);plt.close(fig)
    summary={'rows':len(df),'missing_cells':0,'development_rows':len(dev),'test_rows':len(test),'development_cells':len(set(groups[dev])),'test_cells':len(set(groups[test])),'selected_model':chosen,'test':final[0],'baseline_test':final[1],'train':final[2],'mae_reduction_vs_baseline':1-final[0]['MAE_USD_1990']/final[1]['MAE_USD_1990'],'capped_target_rows':int(np.isclose(y,500001).sum()),'negative_test_predictions':int((prediction<0).sum()),'test_cap_errors':segments,'minimum_cv_mae':min(cv_results,key=lambda r:r['MAE_mean'])}
    save(ROOT/'reports'/'resultats.json',summary)
    versions={n:importlib.metadata.version(n) for n in ['numpy','pandas','scikit-learn','matplotlib']};(ROOT/'requirements.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
    manifest={'objective':'Prédire la valeur médiane des logements par zone du recensement 1990, projet 10 adapté de Boston vers California.','source_url':URL,'archive_sha256':SHA,'raw_csv_sha256':hashlib.sha256((ROOT/'raw/california.csv').read_bytes()).hexdigest(),'target':'MedHouseVal × 100000, USD de 1990','unit_of_observation':'Census block group, pas maison individuelle','steps':{'DataCollect':'completed','DataAnalyse':'completed','DataML':'completed'},'seed':SEED,'split':'GroupShuffleSplit sur cellules de 0.5°, 20 % des cellules en test','validation':'4 plis GroupKFold géographiques sur développement, choix MAE minimum','test_usage':'Modèle retenu et référence évalués après sélection ; test non utilisé pour régler modèles ou variables.','preprocessing':'StandardScaler ajusté dans chaque pli, puis développement complet pour export. Aucune imputation nécessaire.','versions':versions,'checks':['Checksum de l’archive','20640 lignes, aucune cellule manquante','Cellules géographiques disjointes développement/test et CV','Rechargement JSON reproduit toutes les estimations test'],'limits':['1990, pas marché actuel','Zones agrégées, pas biens individuels','Plafond cible 500001 USD','Cellules voisines possibles sans tampon spatial','Les variables de zone doivent être disponibles pour estimer ; aucune prévision temporelle'],'next_action':'Valider sur données indépendantes et récentes avant toute utilisation opérationnelle.'}
    save(ROOT/'manifest.json',manifest);print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
