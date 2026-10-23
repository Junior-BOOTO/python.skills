"""Weekly forecasts: fixed candidates, chronological validation and held-out test."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge


def demo():
    rng = np.random.default_rng(42)
    dates = pd.date_range('2023-01-02', periods=156, freq='W-MON')
    return pd.concat([pd.DataFrame({'date': dates, 'product': name,
        'sales': np.maximum(0, np.rint(base + .12*np.arange(156) + 8*np.sin(2*np.pi*np.arange(156)/52) + rng.normal(0,3,156)))})
        for name,base in [('A',30),('B',55),('C',80)]], ignore_index=True)


def validate(df):
    df = df.copy()
    if df.empty:
        raise ValueError('Le fichier ne contient aucune vente.')
    if not {'date','product','sales'} <= set(df):
        raise ValueError('Colonnes requises : date, product, sales.')
    df['date'] = pd.to_datetime(df['date'], errors='raise')
    df['sales'] = pd.to_numeric(df['sales'], errors='raise')
    if df[['date','product','sales']].isna().any().any() or not np.isfinite(df.sales).all() or (df.sales < 0).any():
        raise ValueError('Valeurs manquantes, infinies ou ventes négatives.')
    if df.duplicated(['product','date']).any():
        raise ValueError('Doublons produit/date.')
    for _,g in df.groupby('product'):
        d=g.sort_values('date').date
        if len(d)<112 or not d.diff().dropna().eq(pd.Timedelta(days=7)).all():
            raise ValueError('Au moins 112 semaines consécutives par produit sont requises.')
    return df.sort_values(['product','date'])


def features(t):
    t=np.asarray(t)
    return np.column_stack([t/52, np.sin(2*np.pi*t/52), np.cos(2*np.pi*t/52)])


def forecast(y, method, horizon=4):
    y=np.asarray(y,dtype=float)
    if method=='mean4': return np.repeat(y[-4:].mean(),horizon)
    model=Ridge(alpha=1).fit(features(np.arange(len(y))),y)
    return np.maximum(0,model.predict(features(np.arange(len(y),len(y)+horizon))))


def evaluate(y, method, origins):
    errors=[]
    for o in origins:
        errors.extend(np.abs(np.asarray(y[o:o+4])-forecast(y[:o],method)))
    return float(np.mean(errors))


def order_quantity(demand, stock, incoming, buffer=0):
    if any(not np.isfinite(v) or v<0 for v in [demand,stock,incoming,buffer]):
        raise ValueError('Les paramètres de stock doivent être positifs ou nuls et finis.')
    return int(np.ceil(max(0,demand+buffer-stock-incoming)))


def run(df):
    df=validate(df); metrics=[]; predictions=[]
    for product,g in df.groupby('product'):
        y=g.sales.to_numpy(); n=len(y)
        # Validation: 3 disjoint four-week blocks; final test: 3 later blocks.
        validation=list(range(n-24,n-12,4)); test=list(range(n-12,n,4))
        scores={m:evaluate(y,m,validation) for m in ['mean4','ridge']}
        chosen=min(scores,key=scores.get)
        metrics.append({'product':str(product),'selected':chosen,
            'validation_mae':scores,'test_mae_selected':evaluate(y,chosen,test),
            'test_mae_baseline':evaluate(y,'mean4',test),'test_forecasts':12})
        for i,p in enumerate(forecast(y,chosen)):
            predictions.append({'product':product,'date':g.date.max()+pd.Timedelta(weeks=i+1),'forecast':float(p)})
    return pd.DataFrame(predictions),metrics


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--csv');args=parser.parse_args()
    df=pd.read_csv(args.csv) if args.csv else demo()
    pred,metrics=run(df);Path('reports').mkdir(exist_ok=True)
    pred.to_csv('reports/forecast.csv',index=False)
    Path('reports/metrics.json').write_text(json.dumps(metrics,indent=2))
    if not args.csv: df.to_csv('reports/synthetic_sales.csv',index=False)
    print(json.dumps(metrics,indent=2))
