"""Prévision historique à six mois, validation glissante et test final chronologique."""
from pathlib import Path
import json,hashlib,warnings,importlib.metadata
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.sm_exceptions import ConvergenceWarning
ROOT=Path(__file__).resolve().parent
MODELS=['Derniere_valeur','Saisonnier_12','Saisonnier_avec_derive','SARIMA_011_010_12']
HORIZON=6
def predict(history,name):
    history=np.asarray(history,dtype=float)
    if name=='Derniere_valeur':return np.repeat(history[-1],HORIZON),None
    if name=='Saisonnier_12':return history[-12:-6].copy(),None
    if name=='Saisonnier_avec_derive':return history[-12:-6]+np.mean(history[12:]-history[:-12]),None
    with warnings.catch_warnings():
        warnings.simplefilter('error',ConvergenceWarning)
        result=SARIMAX(history,order=(0,1,1),seasonal_order=(0,1,0,12),trend=None).fit(disp=False,maxiter=300)
    assert result.mle_retvals['converged']
    return np.asarray(result.forecast(HORIZON)),result
def metrics(observed,forecast):
    err=np.asarray(observed)-np.asarray(forecast)
    return {'MAE':float(np.abs(err).mean()),'RMSE':float(np.sqrt(np.mean(err**2))),
            'WAPE':float(np.abs(err).sum()/np.abs(observed).sum())}
def main():
    df=pd.read_csv(ROOT/'raw/mensuel.csv');df['month']=pd.to_datetime(df.month)
    df=df.sort_values('month');dates=pd.DatetimeIndex(df.month)
    assert len(df)==48 and dates.is_unique and dates.equals(pd.date_range('2011-01-01',periods=48,freq='MS'))
    y=df.sales.to_numpy();assert np.isfinite(y).all() and (y>0).all()
    assert abs(y.sum()-12642501.90988)<.001
    rows=[];predictions=[]
    # Trois fenêtres de six mois : 2013 S1, 2013 S2, 2014 S1 ; pas de futur dans les fits.
    for origin in [24,30,36]:
        history=y[:origin];actual=y[origin:origin+HORIZON]
        for name in MODELS:
            prediction,_=predict(history,name)
            rows.append({'model':name,'origin':str(dates[origin-1].date()),**metrics(actual,prediction)})
            predictions.extend({'model':name,'origin':str(dates[origin-1].date()),'month':str(dates[origin+h].date()),'horizon':h+1,'observed':float(actual[h]),'predicted':float(prediction[h])} for h in range(HORIZON))
    scores=pd.DataFrame(rows);scores.to_csv(ROOT/'analysis/validation_fenetres.csv',index=False)
    comparison=scores.groupby('model').agg(MAE_mean=('MAE','mean'),MAE_std_windows=('MAE','std'),RMSE_mean=('RMSE','mean'),WAPE_mean=('WAPE','mean')).sort_values('MAE_mean')
    comparison.to_csv(ROOT/'analysis/comparaison.csv')
    chosen=comparison.index[0]
    # Les modèles, horizon et sélection sont figés avant le dernier semestre test.
    test_prediction,_=predict(y[:42],chosen);reference,_=predict(y[:42],'Saisonnier_12')
    test=[{'model':chosen,**metrics(y[42:],test_prediction)}, {'model':'Reference_saisonniere_12',**metrics(y[42:],reference)}]
    pd.DataFrame(test).to_csv(ROOT/'analysis/test_final.csv',index=False)
    pd.DataFrame({'month':dates[42:],'observed':y[42:],'chosen_forecast':test_prediction,'seasonal_reference':reference}).to_csv(ROOT/'analysis/predictions_test.csv',index=False)
    pd.DataFrame(predictions).to_csv(ROOT/'analysis/validation_predictions.csv',index=False)
    # Après l’évaluation, refit sur les 48 mois ; ce fit n’a pas de score indépendant.
    future,fit=predict(y,chosen);future_dates=pd.date_range(dates[-1]+pd.offsets.MonthBegin(1),periods=HORIZON,freq='MS')
    export={'model':chosen,'history':y.tolist(),'last_observed_month':str(dates[-1].date()),'horizon_months':HORIZON,'unit':'UM du jeu fictif','orders':{'order':[0,1,1],'seasonal_order':[0,1,0,12]},'parameters':fit.params.tolist() if fit is not None else None,'note':'Fit final sur 48 mois ; prolongement historique 2015 sans ventes observées correspondantes.'}
    (ROOT/'models/prevision.json').write_text(json.dumps(export,ensure_ascii=False,indent=2))
    if fit is not None:
        loaded=json.loads((ROOT/'models/prevision.json').read_text())
        reloaded=SARIMAX(loaded['history'],order=(0,1,1),seasonal_order=(0,1,0,12),trend=None).filter(loaded['parameters'])
        assert np.allclose(reloaded.forecast(HORIZON),future,atol=1e-8)
        interval=fit.get_forecast(HORIZON).conf_int(alpha=.05)
    else:
        assert np.allclose(predict(export['history'],chosen)[0],future)
        interval=None
    output=pd.DataFrame({'month':future_dates,'forecast':future})
    if interval is not None:output['lower_95_model']=interval[:,0];output['upper_95_model']=interval[:,1]
    output.to_csv(ROOT/'analysis/prolongement_2015.csv',index=False)
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(11,5));ax.plot(dates,y,label='Ventes observées fictives',color='#167d8d');ax.plot(dates[42:],test_prediction,'--o',label='Prévision test, fit fin juin 2014',color='#7770ac');ax.plot(future_dates,future,'--o',label='Prolongement 2015, refit fin 2014',color='#b96942');ax.axvline(dates[42],ls=':',color='gray')
    if interval is not None:ax.fill_between(future_dates,interval[:,0],interval[:,1],alpha=.16,color='#b96942',label='Intervalle 95 % conditionnel au modèle')
    ax.set(xlabel='Mois',ylabel='Ventes mensuelles (UM)',title='Prévision à six mois · Historique 2011–2014');ax.legend(fontsize=8);fig.tight_layout();fig.savefig(ROOT/'reports/prevision.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5));ax.barh(comparison.index,comparison.MAE_mean,xerr=comparison.MAE_std_windows,color='#167d8d');ax.invert_yaxis();ax.set(xlabel='MAE en UM · barres : écart-type entre 3 fenêtres',title='Comparaison sur validation chronologique, horizon fixe 6 mois');fig.tight_layout();fig.savefig(ROOT/'reports/comparaison.png',dpi=150);plt.close(fig)
    summary={'months':48,'period':['2011-01','2014-12'],'source_sales':float(y.sum()),'horizon_months':6,'validation_origins':['2012-12','2013-06','2013-12'],'test_period':['2014-07','2014-12'],'selected_model':chosen,'validation':comparison.reset_index().to_dict('records'),'test':test,'MAE_reduction_vs_seasonal':1-test[0]['MAE']/test[1]['MAE'],'future_dates':[str(x.date()) for x in future_dates],'future_forecast':future.tolist(),'uncertainty':'Intervalle paramétrique conditionnel au SARIMA' if interval is not None else 'Pas d’intervalle probabiliste revendiqué pour la référence retenue.'}
    (ROOT/'reports/resultats.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    versions={n:importlib.metadata.version(n) for n in ['numpy','pandas','statsmodels','matplotlib']};(ROOT/'requirements.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
    manifest={'objective':'Projet 12 : prévision de ventes mensuelles fictives à 6 mois.','source':'Global Superstore, agrégats vérifiés du projet 7','source_metadata':'source.json','source_sha256':hashlib.sha256((ROOT/'raw/mensuel.csv').read_bytes()).hexdigest(),'stages':{'DataCollect':'completed','DataAnalyse':'completed','DataML':'completed'},'validation':'3 origines glissantes, 6 mois à chaque fois, entraînement croissant. Choix MAE avant test.','test':'6 derniers mois 2014, seulement modèle choisi et référence saisonnière.','future_fit':'Refit 48 mois après évaluation, prolongement 2015 non évalué.','versions':versions,'checks':['48 mois uniques consécutifs, valeurs positives et finies','Total égal au projet source','Convergence SARIMA aux fits','Rechargement numérique de la prévision'],'limits':['Seulement 4 cycles annuels','Données fictives historiques','Pas exogènes, promotions ou ruptures de stock','Pas prévision actuelle ou suivi automatisé'],'next_action':'Plus d’historique et validation sur données opérationnelles indépendantes pour un usage réel.'}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
