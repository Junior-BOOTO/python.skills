"""SMS anglais : modèle explicable, séparation par similarité, JSON portable."""
from pathlib import Path
from urllib.request import urlopen
import argparse,csv,hashlib,io,json,re,zipfile
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer,HashingVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import precision_score,recall_score,f1_score,confusion_matrix,average_precision_score
SOURCE='https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip'

def normalize(text):
    s=re.sub(r'https?://\S+|www\.\S+',' url ',str(text).lower())
    s=re.sub(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}',' email ',s)
    return ' '.join(re.findall(r'[a-z]{2,}',re.sub(r'\d+',' number ',s)))

def grouped(texts,threshold=.94):
    n=len(texts);parent=list(range(n))
    def root(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def union(a,b):
        a,b=root(a),root(b)
        if a!=b:parent[max(a,b)]=min(a,b)
    norm=[normalize(t) for t in texts];seen={}
    for i,t in enumerate(norm):
        if t in seen:union(i,seen[t])
        else:seen[t]=i
    h=HashingVectorizer(analyzer='char',ngram_range=(3,5),n_features=65536,alternate_sign=False,norm='l2',binary=True)
    x=h.transform(norm)
    for start in range(0,n,150):
        s=(x[start:start+150]@x.T).tocoo()
        for a,b,v in zip(s.row,s.col,s.data):
            i=start+int(a);b=int(b)
            if i<b and v>=threshold:union(i,b)
    return np.array([root(i) for i in range(n)])

def split(y,g):
    dev,test=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(y,y,g))
    a,b=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=43).split(dev,y[dev],g[dev]))
    train,val=dev[a],dev[b]
    assert not(set(g[train])&set(g[val]) or set(g[train])&set(g[test]) or set(g[val])&set(g[test]))
    for p in [train,val,test]:
        if len(set(y[p]))!=2:raise ValueError('Deux classes requises dans chaque partition')
    return train,val,test

def metric(y,p,t):
    z=(np.array(p)>=t).astype(int)
    return {'precision':float(precision_score(y,z,zero_division=0)),'recall':float(recall_score(y,z,zero_division=0)),'f1':float(f1_score(y,z,zero_division=0)),'matrix':confusion_matrix(y,z,labels=[0,1]).tolist()}

def portable(text,m):
    vocab={t:i for i,t in enumerate(m['terms'])};counts={}
    for t in normalize(text).split():
        if t in vocab:counts[vocab[t]]=counts.get(vocab[t],0)+1
    weights={i:c*m['idf'][i] for i,c in counts.items()};norm=np.sqrt(sum(w*w for w in weights.values()))
    parts=[{'term':m['terms'][i],'value':float(w/norm*m['coef'][i])} for i,w in weights.items()] if norm else []
    logit=m['intercept']+sum(p['value'] for p in parts);score=float(1/(1+np.exp(-np.clip(logit,-700,700))))
    return {'score':score,'label':'spam' if score>=m['threshold'] else 'ham','known_terms':len(counts),'logit':float(logit),'contributions':sorted(parts,key=lambda p:abs(p['value']),reverse=True)[:8]}

def train(out,archive=None):
    out=Path(out)
    if out.exists() and any(out.iterdir()):raise ValueError('Sortie non vide')
    out.mkdir(parents=True,exist_ok=True)
    if archive:raw=Path(archive).read_bytes()
    else:
        with urlopen(SOURCE,timeout=25) as r:raw=r.read(2_000_001)
        if len(raw)>2_000_000:raise ValueError('Archive trop volumineuse')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:lines=z.read('SMSSpamCollection').decode('utf-8').splitlines()
    texts=[];labels=[];excluded=0
    for line in lines:
        if not line.strip():continue
        l,t=line.split('\t',1)
        if l not in ('ham','spam'):raise ValueError('Label invalide')
        if not normalize(t):excluded+=1;continue
        labels.append(int(l=='spam'));texts.append(t)
    texts=np.array(texts);y=np.array(labels);g=grouped(texts);tr,va,te=split(y,g)
    pipe=Pipeline([('tfidf',TfidfVectorizer(preprocessor=normalize,token_pattern=r'(?u)\b[a-z]{2,}\b',max_features=5000)),('classifier',LogisticRegression(C=1,class_weight='balanced',solver='liblinear',random_state=42,max_iter=1000))])
    pipe.fit(texts[tr],y[tr]);pv=pipe.predict_proba(texts[va])[:,1]
    options=[dict(threshold=t,**metric(y[va],pv,t)) for t in [.3,.5,.7]]
    threshold=max(options,key=lambda r:(r['f1'],r['precision'],r['threshold']))['threshold']
    scores=pipe.predict_proba(texts[te])[:,1];test=metric(y[te],scores,threshold);test['average_precision']=float(average_precision_score(y[te],scores))
    v=pipe.named_steps['tfidf'];c=pipe.named_steps['classifier']
    m={'terms':v.get_feature_names_out().tolist(),'idf':v.idf_.tolist(),'coef':c.coef_[0].tolist(),'intercept':float(c.intercept_[0]),'threshold':threshold,'score_note':'Uncalibrated logistic score, not probability of fraud'}
    (out/'model.json').write_text(json.dumps(m,separators=(',',':')))
    loaded=json.loads((out/'model.json').read_text());p=np.array([portable(t,loaded)['score'] for t in texts[te]])
    np.testing.assert_allclose(p,scores,atol=1e-10,rtol=1e-10)
    sizes={name:{'messages':len(ids),'spam':int(y[ids].sum()),'groups':len(set(g[ids]))} for name,ids in [('train',tr),('validation',va),('test',te)]}
    r={'messages':len(y),'excluded_without_ascii_tokens':excluded,'spam':int(y.sum()),'groups':len(set(g)),'similarity_group_threshold':.94,'group_overlap':0,'split':sizes,'validation_options':options,'selected_threshold':threshold,'test':test,'baseline_all_ham':metric(y[te],np.zeros(len(te)),.5),'portable_max_error':float(np.max(np.abs(p-scores))),'source':SOURCE,'raw_archive_sha256':hashlib.sha256(raw).hexdigest()}
    (out/'metrics.json').write_text(json.dumps(r,indent=2))
    with (out/'test_predictions.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['row_id','group','actual_spam','score','predicted_spam'])
        for i,s in zip(te,scores):w.writerow([int(i),int(g[i]),int(y[i]),float(s),int(s>=threshold)])
    (out/'split_indices.json').write_text(json.dumps({name:ids.tolist() for name,ids in [('train',tr),('validation',va),('test',te)]}))
    examples=['Congratulations! Claim your free prize now. Visit https://example.org/claim','Can we meet at the library tomorrow afternoon?','Your account needs verification. Please contact support.','Free Python workshop at the community school next week.']
    (out/'examples.json').write_text(json.dumps([{'text':t,**portable(t,m),'type':'original synthetic example, no security ground truth'} for t in examples],indent=2))
    (out/'manifest.json').write_text(json.dumps({'status':'completed','target':'English SMS spam UCI label','source':SOURCE,'raw_sha256':r['raw_archive_sha256'],'test_consulted':True,'group_overlap':0,'model':'model.json','limits':'No French/Spanish, phishing, fraud or current-email validation; uncalibrated score'},indent=2))
    return r

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--archive');a=p.parse_args();print(json.dumps(train(a.out,a.archive),indent=2))
