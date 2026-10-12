"""Analyse un export historique quotidien Bitstamp BTC-USD, sans accès réseau."""
from pathlib import Path
import argparse, json, hashlib, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

def run(source, out):
    out=Path(out)
    for d in ['raw','collected','analysis','models','reports']: (out/d).mkdir(parents=True,exist_ok=True)
    raw=Path(source).read_bytes()
    (out/'raw/normalized_original.csv').write_bytes(raw)
    df=pd.read_csv(source)
    required=['Date','Open','High','Low','Close','Volume']
    if not set(required)<=set(df): raise ValueError('Colonnes nécessaires : '+', '.join(required))
    df=df[required].copy()
    df['Date']=pd.to_datetime(df.Date,utc=True,errors='raise').dt.normalize()
    for c in required[1:]: df[c]=pd.to_numeric(df[c],errors='raise')
    today=pd.Timestamp.now(tz='UTC').normalize()
    incomplete=int((df.Date>=today).sum())
    df=df[df.Date<today].sort_values('Date')
    if df.Date.duplicated().any(): raise ValueError('Dates dupliquées : vérifier les sources.')
    if df.isna().any().any(): raise ValueError('Valeurs manquantes : corriger la source avant entraînement.')
    if (df[['Open','High','Low','Close']]<=0).any().any() or (df.Volume<0).any(): raise ValueError('Valeurs impossibles.')
    if ((df.High<df[['Open','Close','Low']].max(axis=1)) | (df.Low>df[['Open','Close','High']].min(axis=1))).any(): raise ValueError('Incohérence OHLC.')
    if not df.Date.diff().dropna().eq(pd.Timedelta(days=1)).all(): raise ValueError('Historique non quotidien ou dates manquantes : ne pas combler artificiellement.')
    if len(df)<365: raise ValueError('Ce protocole exige au moins 365 jours complets consécutifs.')
    df.to_csv(out/'collected/btc_usd.csv',index=False)
    r=df.Close.pct_change()
    features=pd.DataFrame({'r1':r,'r3':df.Close.pct_change(3),'r7':df.Close.pct_change(7),'vol7':r.rolling(7).std(),'vol30':r.rolling(30).std(),'range':(df.High-df.Low)/df.Close,'volume_change':df.Volume.pct_change()})
    features=features.replace([np.inf,-np.inf],np.nan)
    target=df.Close.shift(-1)/df.Close-1
    mask=features.notna().all(axis=1)&target.notna()
    X=features.loc[mask]; y=target.loc[mask]; close=df.loc[mask,'Close']
    n=len(X); a=int(n*.6); b=int(n*.8)
    # Une observation de séparation : la cible d'une partition ne franchit pas la suivante.
    train=slice(0,a-1); valid=slice(a,b-1); test=slice(b,n)
    candidates={'ridge':make_pipeline(StandardScaler(),Ridge(alpha=10)), 'forest':RandomForestRegressor(n_estimators=150,max_depth=4,min_samples_leaf=20,random_state=42,n_jobs=1)}
    val={ 'persistence':float(mean_absolute_error(close.iloc[valid]*(1+y.iloc[valid]),close.iloc[valid])) }
    for name,m in candidates.items():
        m.fit(X.iloc[train],y.iloc[train])
        pred=close.iloc[valid]*(1+m.predict(X.iloc[valid]))
        val[name]=float(mean_absolute_error(close.iloc[valid]*(1+y.iloc[valid]),pred))
    selected=min(val,key=val.get)
    models={}
    if selected!='persistence':
        chosen=candidates[selected];chosen.fit(X.iloc[:b-1],y.iloc[:b-1]);models[selected]=chosen
    truth=close.iloc[test]*(1+y.iloc[test]); predictions={'persistence':close.iloc[test].to_numpy()}
    for name,m in models.items(): predictions[name]=close.iloc[test].to_numpy()*(1+m.predict(X.iloc[test]))
    metrics=[]
    for name,p in predictions.items(): metrics.append({'model':name,'test_mae_usd':float(mean_absolute_error(truth,p)),'test_rmse_usd':float(np.sqrt(mean_squared_error(truth,p)))})
    pd.DataFrame(metrics).to_csv(out/'reports/metrics.csv',index=False)
    result=pd.DataFrame({'date_target':df.loc[mask,'Date'].iloc[test].to_numpy()+pd.Timedelta(days=1),'actual':truth.to_numpy(),**predictions})
    result.to_csv(out/'analysis/test_predictions.csv',index=False)
    # Export des modèles appris et contrôle de rechargement, même si la référence gagne.
    for name,m in candidates.items():
        if name!=selected: m.fit(X.iloc[:b-1],y.iloc[:b-1])
        joblib.dump(m,out/f'models/{name}.joblib')
        restored=joblib.load(out/f'models/{name}.joblib')
        np.testing.assert_allclose(m.predict(X.iloc[[-1]]),restored.predict(X.iloc[[-1]]))
    fig,ax=plt.subplots(2,1,figsize=(11,7))
    ax[0].plot(df.Date,df.Close);ax[0].set_ylabel('BTC / USD');ax[0].set_title('Historique Bitstamp / CryptoDataDownload — jours complets')
    for name in ['actual']+list(predictions):ax[1].plot(result.date_target,result[name],label=name,alpha=.75)
    ax[1].legend();ax[1].set_ylabel('USD — test chronologique');fig.tight_layout();fig.savefig(out/'reports/analysis.png',dpi=160);plt.close(fig)
    summary={'rows':len(df),'start':str(df.Date.min()),'end':str(df.Date.max()),'excluded_incomplete':incomplete,'daily_return_std':float(r.std()),'max_drawdown':float((df.Close/df.Close.cummax()-1).min()),'validation_mae_usd':val,'selected_on_validation':selected,'test_metrics':metrics,'features':list(X),'protocol':'60/20/20 chronologique, une observation de séparation, cible rendement t+1, cours reconstruit ; prévision après clôture UTC'}
    (out/'reports/results.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (out/'manifest.json').write_text(json.dumps({'source':'Bitstamp / CryptoDataDownload BTC-USD CSV fourni','sha256':hashlib.sha256(raw).hexdigest(),'target':'clôture t+1','horizon':'1 jour','status':{'collection':'completed','analysis':'completed','model':'completed'},'results':'reports/results.json'},indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--out',default='output');args=p.parse_args();run(args.csv,args.out)
