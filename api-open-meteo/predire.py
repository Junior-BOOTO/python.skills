"""Réutiliser l'export, à partir de sept jours passés complets, sans pickle."""
from pathlib import Path
import json,numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parent
def predict_next(history):
    history=history.sort_index()
    if len(history)<7:raise ValueError('Sept jours de données sont requis.')
    last=history.iloc[-7:]
    if not last.index.equals(pd.date_range(last.index[0],periods=7,freq='D')):raise ValueError('Les sept derniers jours doivent être consécutifs.')
    if not np.isfinite(last[['temperature_moyenne_c','precipitations_mm']].to_numpy()).all():raise ValueError('Valeurs finies requises.')
    target=last.index[-1]+pd.Timedelta(days=1);t=last.temperature_moyenne_c;r=last.precipitations_mm
    features={'temp_lag1':float(t.iloc[-1]),'temp_lag2':float(t.iloc[-2]),'temp_mean3':float(t.iloc[-3:].mean()),'temp_mean7':float(t.mean()),'rain_lag1':float(r.iloc[-1]),'rain_mean3':float(r.iloc[-3:].mean()),'sin_day':float(np.sin(2*np.pi*target.dayofyear/365)),'cos_day':float(np.cos(2*np.pi*target.dayofyear/365))}
    model=json.loads((ROOT/'models/temperature_j1.json').read_text())
    if model['type']=='ridge':
        x=np.array([features[name] for name in model['features']]);value=float(((x-np.array(model['mean']))/np.array(model['scale']))@np.array(model['coefficients'])+model['intercept'])
    elif model['type']=='persistence':value=features['temp_lag1']
    else:value=model['value']
    return {'date_cible':str(target.date()),'estimation_temperature_moyenne_c':value,'nature':'Illustration sur réanalyse historique, pas prévision opérationnelle validée'}
if __name__=='__main__':
    history=pd.read_csv(ROOT/'collected/bogota_2025.csv',parse_dates=['date']).set_index('date')
    print(json.dumps(predict_next(history),ensure_ascii=False,indent=2))
