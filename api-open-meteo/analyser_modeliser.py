"""Analyse et modèle pédagogique à J+1 sur la réanalyse ERA5 Bogotá 2025."""
from pathlib import Path
import json,hashlib,importlib.metadata
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error,root_mean_squared_error,r2_score
ROOT=Path(__file__).resolve().parent
BASE=['temp_lag1','temp_lag2','temp_mean3','temp_mean7','rain_lag1','rain_mean3']
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2))
def metrics(y,p):return {'MAE_C':float(mean_absolute_error(y,p)),'RMSE_C':float(root_mean_squared_error(y,p)),'R2':float(r2_score(y,p)),'mean_error_observed_minus_predicted_C':float(np.mean(np.asarray(y)-np.asarray(p)))}
def main():
    data=pd.read_csv(ROOT/'collected/bogota_2025.csv',parse_dates=['date']).set_index('date').sort_index()
    assert len(data)==365 and data.index.equals(pd.date_range('2025-01-01','2025-12-31',freq='D'))
    assert not data.isna().any().any() and np.isfinite(data.to_numpy()).all()
    t=data.temperature_moyenne_c;r=data.precipitations_mm
    assert r.ge(0).all()
    monthly=data.resample('MS').agg(temperature_moyenne_c=('temperature_moyenne_c','mean'),precipitations_mm=('precipitations_mm','sum'),jours_pluie_1mm=('precipitations_mm',lambda x:x.ge(1).sum()))
    monthly.to_csv(ROOT/'analysis/mensuel_detaille.csv')
    data.describe().to_csv(ROOT/'analysis/statistiques.csv')
    overview={'days':365,'temperature_mean_C':float(t.mean()),'temperature_min_daily_mean_C':float(t.min()),'temperature_max_daily_mean_C':float(t.max()),'precipitation_total_mm':float(r.sum()),'rainy_days_at_least_1mm':int(r.ge(1).sum()),'wettest_month':str(monthly.precipitations_mm.idxmax().date()),'wettest_month_mm':float(monthly.precipitations_mm.max()),'spearman_temperature_precipitation':float(t.corr(r,method='spearman'))}
    save(ROOT/'reports/analyse.json',overview)
    # Index = date cible. Toutes les valeurs météo explicatives sont strictement antérieures.
    frame=pd.DataFrame({'target':t,'temp_lag1':t.shift(1),'temp_lag2':t.shift(2),
      'temp_mean3':t.shift(1).rolling(3).mean(),'temp_mean7':t.shift(1).rolling(7).mean(),
      'rain_lag1':r.shift(1),'rain_mean3':r.shift(1).rolling(3).mean()})
    frame['sin_day']=np.sin(2*np.pi*frame.index.dayofyear/365)
    frame['cos_day']=np.cos(2*np.pi*frame.index.dayofyear/365)
    usable=frame.dropna();assert len(usable)==358
    assert np.allclose(usable.temp_lag1.to_numpy(),t.loc[usable.index-pd.Timedelta(days=1)].to_numpy())
    train=usable.loc[:'2025-07-31'];val=usable.loc['2025-08-01':'2025-09-30'];test=usable.loc['2025-10-01':]
    assert len(train)+len(val)+len(test)==358 and train.index.max()<val.index.min()<test.index.min()
    assert val.index.max()<test.index.min()
    frame.to_csv(ROOT/'collected/donnees_modele.csv')
    candidates=[];fits={}
    mean=float(train.target.mean())
    candidates.append({'model':'Persistance','features':['temp_lag1'],**metrics(val.target,val.temp_lag1)})
    candidates.append({'model':'Moyenne_train','features':[],**metrics(val.target,np.repeat(mean,len(val)))})
    for scope,features in [('retards',BASE),('retards_calendrier',BASE+['sin_day','cos_day'])]:
        for alpha in [.1,1,10,100]:
            name=f'Ridge_{scope}_alpha_{alpha}'
            model=Pipeline([('scale',StandardScaler()),('ridge',Ridge(alpha=alpha))]).fit(train[features],train.target)
            candidates.append({'model':name,'features':features,**metrics(val.target,model.predict(val[features]))});fits[name]=(features,model)
    pd.DataFrame([{k:v for k,v in c.items() if k!='features'} for c in candidates]).to_csv(ROOT/'analysis/comparaison_validation.csv',index=False)
    # Préférence pour une référence simple si elle est à moins de 1 % du meilleur MAE.
    best=min(candidates,key=lambda c:c['MAE_C']);simple=[c for c in candidates[:2] if c['MAE_C']<=best['MAE_C']*1.01]
    chosen=min(simple,key=lambda c:c['MAE_C']) if simple else best
    if chosen['model']=='Persistance':
        prediction=test.temp_lag1.to_numpy();train_prediction=train.temp_lag1.to_numpy();export={'type':'persistence','features':['temp_lag1']}
    elif chosen['model']=='Moyenne_train':
        prediction=np.repeat(mean,len(test));train_prediction=np.repeat(mean,len(train));export={'type':'constant','features':[],'value':mean}
    else:
        features,model=fits[chosen['model']];prediction=model.predict(test[features]);train_prediction=model.predict(train[features]);scaler=model.named_steps['scale'];reg=model.named_steps['ridge']
        export={'type':'ridge','features':features,'mean':scaler.mean_.tolist(),'scale':scaler.scale_.tolist(),'coefficients':reg.coef_.tolist(),'intercept':float(reg.intercept_)}
        pd.DataFrame({'feature':features,'coefficient_for_one_train_std_C':reg.coef_}).to_csv(ROOT/'analysis/coefficients.csv',index=False)
    export.update({'name':chosen['model'],'target':'Température quotidienne moyenne ERA5, °C','horizon':'J+1, une prévision par jour à partir des jours précédents','trained_until':'2025-07-31','validation_until':'2025-09-30','test_period':['2025-10-01','2025-12-31'],'raw_source_sha256':hashlib.sha256((ROOT/'raw/reponse.json').read_bytes()).hexdigest(),'warning':'Réanalyse rétrospective ; pas garantie que les entrées étaient disponibles à une heure de prévision réelle.'})
    save(ROOT/'models/temperature_j1.json',export)
    loaded=json.loads((ROOT/'models/temperature_j1.json').read_text())
    if loaded['type']=='ridge':recovered=((test[loaded['features']].to_numpy()-np.array(loaded['mean']))/np.array(loaded['scale']))@np.array(loaded['coefficients'])+loaded['intercept']
    elif loaded['type']=='persistence':recovered=test.temp_lag1.to_numpy()
    else:recovered=np.repeat(loaded['value'],len(test))
    assert np.allclose(recovered,prediction,atol=1e-10)
    # Test final du choix figé et références ; aucun réglage sur octobre–décembre.
    finals=[{'model':chosen['model'],**metrics(test.target,prediction)}, {'model':'Reference_persistance',**metrics(test.target,test.temp_lag1)}, {'model':'Reference_moyenne_train',**metrics(test.target,np.repeat(mean,len(test)))}]
    pd.DataFrame(finals).to_csv(ROOT/'analysis/scores_test.csv',index=False)
    output=pd.DataFrame({'observed_C':test.target,'predicted_C':prediction,'persistence_C':test.temp_lag1,'error_observed_minus_predicted_C':test.target-prediction});output.to_csv(ROOT/'analysis/predictions_test.csv')
    residuals=test.target.to_numpy()-prediction
    pd.DataFrame([{'month':str(month.date()),'days':len(block),**metrics(block.observed_C,block.predicted_C)} for month,block in output.resample('MS')]).to_csv(ROOT/'analysis/erreurs_test_par_mois.csv',index=False)
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(2,1,figsize=(11,7),sharex=True);axes[0].plot(data.index,t,color='#167d8d');axes[0].set(ylabel='Température moyenne (°C)',title='Bogotá 2025 · Réanalyse ERA5 via Open-Meteo');axes[1].bar(data.index,r,width=1,color='#7770ac');axes[1].set(ylabel='Précipitations quotidiennes (mm)',xlabel='Date locale America/Bogota');fig.tight_layout();fig.savefig(ROOT/'reports/analyse_meteo.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(11,7),sharex=True);axes[0].plot(test.index,test.target,label='Réanalyse cible',color='#167d8d');axes[0].plot(test.index,prediction,label='Modèle retenu',color='#b56c4b');axes[0].plot(test.index,test.temp_lag1,label='Persistance',color='#7770ac',alpha=.5);axes[0].set(ylabel='Température moyenne (°C)',title='Test octobre–décembre 2025 · Prévisions à un jour');axes[0].legend();axes[1].plot(test.index,residuals,color='#b56c4b');axes[1].axhline(0,ls='--',color='gray');axes[1].set(ylabel='Cible − estimation (°C)',xlabel='Date cible');fig.tight_layout();fig.savefig(ROOT/'reports/test_modele.png',dpi=150);plt.close(fig)
    summary={'analysis':overview,'horizon':'J+1','usable_days':358,'train_days':len(train),'validation_days':len(val),'test_days':len(test),'selected_model':chosen['model'],'selection':'MAE validation ; référence simple privilégiée si écart inférieur à 1 %','validation_selected':{k:v for k,v in chosen.items() if k!='features'},'train':metrics(train.target,train_prediction),'test':finals,'mae_reduction_vs_persistence':1-finals[0]['MAE_C']/finals[1]['MAE_C'],'test_residual_lag1_correlation':float(pd.Series(residuals).autocorr(1)),'export_reload_verified':True}
    save(ROOT/'reports/modelisation.json',summary)
    versions={n:importlib.metadata.version(n) for n in ['numpy','pandas','scikit-learn','matplotlib']};(ROOT/'requirements.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
    manifest=json.loads((ROOT/'manifest.json').read_text());manifest.update({'etapes':{'DataCollect':'completed','DataAnalyse':'completed','DataML':'completed'},'objectif_modele':'Température moyenne du lendemain à partir du passé, démonstration sur réanalyse','horizon':'1 jour','selection':summary['selection'],'decoupage':'Dates cibles : train janvier–juillet, validation août–septembre, test octobre–décembre 2025','pretraitement':'Retards et moyennes strictement décalés ; standardisation ajustée sur train uniquement','versions':versions,'raison_ml':None,'prochaine_etape':'Tester sur autres années et observations indépendantes ; vérifier la disponibilité réelle des données à l’heure d’émission.'});save(ROOT/'manifest.json',manifest)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
