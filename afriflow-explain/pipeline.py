"""AfriFlow Explain : revue rétrospective de réseaux SYNTHÉTIQUES, fenêtres UTC 24 h."""
from pathlib import Path
from collections import defaultdict
import json,math,hashlib,platform
import numpy as np
import pandas as pd
import sklearn,joblib
from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score
P=Path(__file__).resolve().parent
SEED=73
BUDGET=.10

def simulate():
    rng=np.random.default_rng(SEED);rows=[];truth=[]
    patterns=['random','random','random','random','payroll','collection','legit_chain','legit_cycle','random','random','random','random','random','random','random','random','random','random','rapid_cycle','rapid_relay']
    currencies=['NGN','GHS','KES','RWF'];countries=['Nigeria','Ghana','Kenya','Rwanda']
    for day in range(60):
        base=pd.Timestamp('2025-01-01',tz='UTC')+pd.Timedelta(days=day)
        for case in range(30):
            cid=f'D{day:02d}-C{case:02d}';typ=str(rng.choice(patterns));n=int(rng.integers(4,9));nodes=[cid+f'-A{i}' for i in range(n)];currency=currencies[case%4];scale=[15000,100,2000,25000][case%4];amount=float(rng.lognormal(np.log(scale),.8));start=int(rng.integers(180,1000));edges=[]
            if typ in ['rapid_cycle','legit_cycle']:
                # Les cycles légitimes peuvent être aussi rapides : un motif ne prouve rien.
                step=float(rng.uniform(1,10) if typ=='rapid_cycle' else rng.uniform(3,50))
                for i in range(3):edges.append((i,(i+1)%3,start+i*step,amount*rng.uniform(.96,1.04)))
                for i in range(3,n):edges.append((0,i,start+180+i*3,amount*rng.uniform(.1,.8)))
            elif typ in ['rapid_relay','legit_chain']:
                step=float(rng.uniform(1,7) if typ=='rapid_relay' else rng.uniform(3,60))
                for i in range(n-1):edges.append((i,i+1,start+i*step,amount*rng.uniform(.94,1.06)))
            elif typ=='payroll':
                for i in range(1,n):edges.append((0,i,start+i,amount*rng.uniform(.7,1.3)))
            elif typ=='collection':
                for i in range(1,n):edges.append((i,0,start+i,amount*rng.uniform(.5,1.5)))
            else:
                for i in range(1,n):edges.append((int(rng.integers(0,i)),i,start+float(rng.uniform(0,300)),amount*rng.uniform(.1,2)))
                for _ in range(int(rng.integers(0,5))):
                    a,b=rng.choice(n,2,replace=False);edges.append((int(a),int(b),start+float(rng.uniform(0,350)),amount*rng.uniform(.1,2)))
            # Corruption de qualité indépendante du label, jamais utilisée pour fabriquer une fraude.
            mask_case=bool(rng.random()<.12)
            for k,(a,b,minute,amt) in enumerate(edges):
                t=(base+pd.Timedelta(minutes=minute)).isoformat()
                if mask_case and k==0:t=''
                rows.append({'transaction_id':f'{cid}-T{k:02d}','timestamp':t,'window_date':base.date().isoformat(),'sender_id':nodes[a],'recipient_id':nodes[b],'amount':round(amt,2),'currency':currency,'sender_institution':'Institution '+chr(65+a%3),'recipient_institution':'Institution '+chr(65+b%3),'country_context':countries[case%4],'source':'synthetic_local'})
            truth.append({'simulation_group':cid,'injected_anomaly':int(typ in ['rapid_cycle','rapid_relay']),'scenario':typ})
    return pd.DataFrame(rows),pd.DataFrame(truth)

def connected_components(frame):
    adjacency=defaultdict(set)
    for r in frame.itertuples():adjacency[r.sender_id].add(r.recipient_id);adjacency[r.recipient_id].add(r.sender_id)
    remaining=set(adjacency);groups=[]
    while remaining:
        first=min(remaining);stack=[first];found=set()
        while stack:
            a=stack.pop()
            if a in found:continue
            found.add(a);stack.extend(sorted(adjacency[a]-found,reverse=True))
        remaining-=found;groups.append(found)
    return groups

def signals(frame):
    valid=frame.dropna(subset=['parsed_time']).sort_values(['parsed_time','transaction_id']);records=list(valid.to_dict('records'));paths=[];cycles=[]
    outgoing=defaultdict(list)
    for r in records:outgoing[r['sender_id']].append(r)
    def walk(path):
        last=path[-1];start=path[0]['sender_id'];visited=[start]+[r['recipient_id'] for r in path]
        if len(path)>=4:return
        for nxt in outgoing[last['recipient_id']]:
            seconds=(nxt['parsed_time']-last['parsed_time']).total_seconds();total=(nxt['parsed_time']-path[0]['parsed_time']).total_seconds()
            ratio=nxt['amount']/last['amount']
            if not (0<seconds<=600 and total<=1800 and .7<=ratio<=1.3):continue
            new=path+[nxt]
            if nxt['recipient_id']==start:
                if len(new)>=3:cycles.append([r['transaction_id'] for r in new])
            elif nxt['recipient_id'] not in visited:
                if len(new)>=3:paths.append([r['transaction_id'] for r in new])
                walk(new)
    for r in records:walk([r])
    cycles=sorted({tuple(a) for a in cycles});paths=sorted({tuple(a) for a in paths})
    outdegree=frame.groupby('sender_id').recipient_id.nunique();indegree=frame.groupby('recipient_id').sender_id.nunique()
    duration=(valid.parsed_time.max()-valid.parsed_time.min()).total_seconds()/60 if len(valid)>1 else 0
    return {'temporal_cycles':len(cycles),'compatible_chains':len(paths),'max_outdegree':int(outdegree.max()),'max_indegree':int(indegree.max()),'nodes':len(set(frame.sender_id)|set(frame.recipient_id)),'edges':len(frame),'duration_minutes':float(duration)},cycles,paths

def rank_metrics(y,score,budget=BUDGET):
    k=max(1,int(math.ceil(len(y)*budget)));ix=np.argsort(-score,kind='stable')[:k];tp=int(np.asarray(y)[ix].sum());positives=int(np.sum(y))
    return {'cases':len(y),'alert_budget':k,'true_positives':tp,'false_positives':k-tp,'false_negatives':positives-tp,'precision_at_budget':tp/k,'recall_at_budget':tp/positives if positives else None,'average_precision':float(average_precision_score(y,score)),'positive_cases':positives,'alert_indices':ix.tolist()}

def run():
    for d in ['raw','collected','analysis','models','reports']:(P/d).mkdir(exist_ok=True)
    manifest={'objectif':'Comparer la priorisation de dossiers par transactions et par parcours à budget égal','unite':'Composante connexe dans une fenêtre UTC de 24 h et une devise','moment':'Après fermeture de la fenêtre, revue rétrospective','source':'Générateur local original, 100 % synthétique, seed=73','etapes':{'DataCollect':'running','DataAnalyse':'pending','DataML':'pending'},'API_externe':'not_connected','GPT_independants':'not_called'}
    def save():(P/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
    save();raw,truth=simulate();raw.to_csv(P/'raw/transfers.csv',index=False);truth.to_csv(P/'raw/simulation_truth.csv',index=False)
    assert raw.transaction_id.is_unique and (raw.amount>0).all()
    df=raw.copy();df['parsed_time']=pd.to_datetime(df.timestamp,utc=True,errors='coerce',format='mixed');df.to_csv(P/'collected/transfers.csv',index=False)
    manifest['etapes']['DataCollect']='completed';manifest['etapes']['DataAnalyse']='running';save()
    data=[];cases=[]
    for (day,currency),window in df.groupby(['window_date','currency'],sort=True):
        for nodes in connected_components(window):
            sub=window[window.sender_id.isin(nodes)].copy();case_id=sub.transaction_id.min().rsplit('-T',1)[0]
            # Identifiant utilisé seulement pour rapprocher la vérité de simulation, pas comme feature.
            assert all(t.startswith(case_id+'-T') for t in sub.transaction_id)
            sig,cycles,paths=signals(sub)
            data.append({'case_id':case_id,'date':day,'currency':currency,'amount_median':float(sub.amount.median()),'amount_max':float(sub.amount.max()),'amount_std':float(sub.amount.std(ddof=0)),'missing_time_rate':float(sub.parsed_time.isna().mean()),**sig})
            reasons=[]
            if cycles:reasons.append({'type':'Circuit temporel compatible','ids':list(cycles[0]),'detail':'Retour vers le compte initial en moins de 30 minutes, étapes strictement ordonnées et montants comparables. Ce motif peut être légitime.'})
            if paths:reasons.append({'type':'Chaîne de transferts rapprochés','ids':list(paths[0]),'detail':'Au moins trois opérations reliées, espacées de moins de 10 minutes, montants comparables. Aucun traçage juridique des mêmes fonds n’est établi.'})
            if not reasons:reasons.append({'type':'Pas de motif temporel retenu','ids':[],'detail':'L’absence de ce motif n’exclut pas une irrégularité.'})
            cases.append({'id':case_id,'date':day,'currency':currency,'signals':sig,'quality':{'missing_timestamps':int(sub.parsed_time.isna().sum()),'observed_edges':len(sub),'coverage':'Exhaustivité bancaire inconnue ; jeu local synthétique seulement'},'reasons':reasons,'transactions':sub.drop(columns='parsed_time').fillna('').to_dict('records')})
    f=pd.DataFrame(data).sort_values(['date','case_id']).reset_index(drop=True);f.to_csv(P/'analysis/features.csv',index=False)
    cases={c['id']:c for c in cases};manifest['etapes']['DataAnalyse']='completed';manifest['etapes']['DataML']='running';save()
    train=f.date<'2025-02-06';validation=(f.date>='2025-02-06')&(f.date<'2025-02-18');test=f.date>='2025-02-18'
    amount_cols=['amount_median','amount_max','amount_std'];scale=f.loc[train].groupby('currency')[amount_cols].median()
    x=f[amount_cols+['edges']].copy()
    for col in amount_cols:x[col]=np.log1p(f[col]/f.currency.map(scale[col]).clip(lower=.01))
    graph_cols=['temporal_cycles','compatible_chains','max_outdegree','max_indegree','nodes','duration_minutes']
    features={'transactions':x,'parcours':pd.concat([x,f[graph_cols]],axis=1)};scores={};models={}
    for name,inputs in features.items():
        model=IsolationForest(n_estimators=160,max_samples=256,random_state=SEED,n_jobs=2);model.fit(inputs.loc[train]);scores[name]=-model.score_samples(inputs);models[name]=model
    # Étiquettes consultées seulement après entraînement et génération des scores.
    joined=f.merge(truth.rename(columns={'simulation_group':'case_id'}),on='case_id',validate='one_to_one');y=joined.injected_anomaly.to_numpy()
    results={}
    for split,mask in [('validation',validation),('test',test)]:results[split]={name:rank_metrics(y[mask],score[mask]) for name,score in scores.items()}
    test_positions=np.flatnonzero(test);chosen={name:set(test_positions[results['test'][name]['alert_indices']]) for name in scores}
    for i,r in f.iterrows():
        c=cases[r.case_id];c['split']='train' if train.iloc[i] else 'validation' if validation.iloc[i] else 'test';c['scores']={k:float(v[i]) for k,v in scores.items()};c['selected_test']={name:i in chosen[name] for name in scores};c['simulation_truth']={'label':int(y[i]),'scenario':joined.scenario.iloc[i]}
    # Incertitude exploratoire bootstrap dossiers ; uniquement du test, pas de nouveau réglage.
    rng=np.random.default_rng(SEED);diff=[];yt=y[test];st={k:v[test] for k,v in scores.items()}
    for _ in range(300):
        idx=rng.integers(0,len(yt),len(yt));a=rank_metrics(yt[idx],st['transactions'][idx]);b=rank_metrics(yt[idx],st['parcours'][idx]);diff.append(b['recall_at_budget']-a['recall_at_budget'])
    summary={'source':'SYNTHETIQUE','transfer_rows':len(df),'cases':len(f),'missing_timestamps':int(df.parsed_time.isna().sum()),'split':{'train':int(train.sum()),'validation':int(validation.sum()),'test':int(test.sum())},'budget':BUDGET,'results':results,'recall_difference_bootstrap_95pct':np.quantile(diff,[.025,.975]).tolist(),'features':{k:v.columns.tolist() for k,v in features.items()}}
    (P/'models/metrics.json').write_text(json.dumps(summary,indent=2));(P/'analysis/cases.json').write_text(json.dumps([cases[k] for k in f.case_id],ensure_ascii=False,separators=(',',':')))
    for name,model in models.items():
        joblib.dump({'model':model,'amount_scale':scale.to_dict(),'feature_columns':features[name].columns.tolist(),'budget':BUDGET},P/f'models/{name}.joblib',compress=3)
        restored=joblib.load(P/f'models/{name}.joblib');np.testing.assert_allclose(-restored['model'].score_samples(features[name].loc[test].head(20)),scores[name][test][:20])
    out=joined[['case_id','date','currency','scenario','injected_anomaly']].copy()
    for name,s in scores.items():out['score_'+name]=s;out['alert_'+name]=[i in chosen[name] for i in range(len(f))]
    out.loc[test].to_csv(P/'models/test_cases.csv',index=False)
    versions={'numpy':np.__version__,'pandas':pd.__version__,'scikit-learn':sklearn.__version__,'joblib':joblib.__version__};(P/'requirements.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n');(P/'reports/versions.json').write_text(json.dumps({'python':platform.python_version(),**versions},indent=2))
    manifest['etapes']['DataML']='completed';manifest['source_sha256']=hashlib.sha256((P/'raw/transfers.csv').read_bytes()).hexdigest();manifest['verification']={'model_reload':'passed','external_api':'not_executed'};save()
    print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
