"""Parcours coordonné : contrôle des sources, exploration et clustering descriptif."""
from pathlib import Path
import json,hashlib,urllib.request,importlib.metadata
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans,AgglomerativeClustering,DBSCAN
from sklearn.metrics import silhouette_score,adjusted_rand_score,davies_bouldin_score
ROOT=Path(__file__).resolve().parent
FEATURES=['Annual Income (k$)','Spending Score (1-100)']
SEED=42
def write_json(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2))
def git_hash(path):
    b=path.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def measure(z,labels):
    mask=labels>=0;n=int(mask.sum());k=len(set(labels[mask]));valid=1<k<n
    return {'clusters':k,'coverage':n/len(z),'silhouette':float(silhouette_score(z[mask],labels[mask])) if valid else None,'davies_bouldin':float(davies_bouldin_score(z[mask],labels[mask])) if valid else None}
def main():
    for d in ['raw','collected','analysis','models','reports']:(ROOT/d).mkdir(exist_ok=True)
    src=json.loads((ROOT/'source.json').read_text());path=ROOT/'raw'/'Mall_Customers.csv'
    if not path.exists() or git_hash(path)!=src['git_blob_sha']:urllib.request.urlretrieve(src['url'],path)
    assert git_hash(path)==src['git_blob_sha']
    df=pd.read_csv(path,dtype={'CustomerID':str});assert len(df)==200 and df.CustomerID.is_unique
    assert df.isna().sum().sum()==0 and np.isfinite(df[FEATURES+['Age']].to_numpy()).all()
    assert df[FEATURES[0]].gt(0).all() and df[FEATURES[1]].between(1,100).all()
    assert df.Age.between(0,120).all()
    duplicate_profiles=int(df.duplicated(['Genre','Age']+FEATURES).sum())
    df.to_csv(ROOT/'collected'/'clients.csv',index=False)
    df[FEATURES+['Age']].describe().to_csv(ROOT/'analysis'/'statistiques.csv')
    scaler=StandardScaler();z=scaler.fit_transform(df[FEATURES])
    curve=[];fits={}
    for k in range(2,9):
        model=KMeans(n_clusters=k,random_state=SEED,n_init=30).fit(z);fits[k]=model
        curve.append({'k':k,'inertia':float(model.inertia_),**measure(z,model.labels_)})
    pd.DataFrame(curve).to_csv(ROOT/'analysis'/'choix_k.csv',index=False)
    best=max(curve,key=lambda r:r['silhouette']);k=best['k'];model=fits[k]
    # Noms stables pour la restitution : centroïdes triés par revenu puis score.
    centers_original=scaler.inverse_transform(model.cluster_centers_)
    order=np.lexsort((centers_original[:,1],centers_original[:,0]));mapping=np.empty(k,dtype=int);mapping[order]=np.arange(k)
    labels=mapping[model.labels_];centers=model.cluster_centers_[order];original=centers_original[order]
    ward=AgglomerativeClustering(n_clusters=k,linkage='ward').fit_predict(z)
    density=DBSCAN(eps=.35,min_samples=5).fit_predict(z)
    comparison=[{'method':'K-means','configuration':f'k={k}, n_init=30',**measure(z,labels),'ari_vs_kmeans':1.0},
                {'method':'Ward','configuration':f'k={k}',**measure(z,ward),'ari_vs_kmeans':float(adjusted_rand_score(labels,ward))},
                {'method':'DBSCAN','configuration':'eps=.35, min_samples=5',**measure(z,density),'ari_vs_kmeans':float(adjusted_rand_score(labels,density))}]
    pd.DataFrame(comparison).to_csv(ROOT/'analysis'/'comparaison_methodes.csv',index=False)
    starts=[]
    for seed in range(10):
        other=KMeans(n_clusters=k,random_state=seed,n_init=30).fit_predict(z)
        starts.append(float(adjusted_rand_score(labels,other)))
    rng=np.random.default_rng(SEED);resamples=[]
    for repeat in range(20):
        ix=rng.choice(len(df),size=160,replace=False)
        local_scaler=StandardScaler().fit(df[FEATURES].iloc[ix])
        local_z=local_scaler.transform(df[FEATURES])
        local_model=KMeans(n_clusters=k,random_state=repeat,n_init=30).fit(local_z[ix])
        predicted=local_model.predict(local_z)
        resamples.append({'repeat':repeat,'sample_size':160,'ari_common_160':float(adjusted_rand_score(labels[ix],predicted[ix]))})
    pd.DataFrame(resamples).to_csv(ROOT/'analysis'/'stabilite_sous_echantillons.csv',index=False)
    stability={'seeds_ari_min':min(starts),'seeds_ari_mean':float(np.mean(starts)),'subsamples_ari_mean':float(np.mean([r['ari_common_160'] for r in resamples])),'subsamples_ari_min':min(r['ari_common_160'] for r in resamples),'replicates':20,'fraction':.8}
    age_z=StandardScaler().fit_transform(df[FEATURES+['Age']])
    age_labels=KMeans(n_clusters=k,random_state=SEED,n_init=30).fit_predict(age_z)
    sensitivity={'features':'revenu, score et âge','k_fixed':k,'ari_vs_primary':float(adjusted_rand_score(labels,age_labels)),**measure(age_z,age_labels)}
    profiles=df[FEATURES].assign(group=labels).groupby('group').agg(count=(FEATURES[0],'size'),income_mean=(FEATURES[0],'mean'),income_min=(FEATURES[0],'min'),income_max=(FEATURES[0],'max'),score_mean=(FEATURES[1],'mean'),score_min=(FEATURES[1],'min'),score_max=(FEATURES[1],'max'))
    profiles.to_csv(ROOT/'analysis'/'profils_groupes.csv')
    df.assign(group=labels).to_csv(ROOT/'collected'/'affectations.csv',index=False)
    np.savez(ROOT/'models'/'kmeans.npz',mean=scaler.mean_,scale=scaler.scale_,centers=centers,features=np.array(FEATURES))
    with np.load(ROOT/'models'/'kmeans.npz',allow_pickle=False) as saved:
        zz=(df[FEATURES].to_numpy()-saved['mean'])/saved['scale']
        recovered=((zz[:,None,:]-saved['centers'][None,:,:])**2).sum(axis=2).argmin(axis=1)
    assert np.array_equal(labels,recovered)
    assert profiles['count'].sum()==200 and sum(best['inertia'] for _ in [0])<float((z*z).sum())
    colors=['#137e8d','#bf554b','#7670ac','#ab7a17','#287748','#a05e8a','#446782','#bc772f']
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    axes[0].plot([r['k'] for r in curve],[r['inertia'] for r in curve],'-o',color='#137e8d');axes[0].set(xlabel='Nombre de groupes k',ylabel='Inertie (espace standardisé)',title='Compacité des groupes')
    axes[1].plot([r['k'] for r in curve],[r['silhouette'] for r in curve],'-o',color='#7670ac');axes[1].axvline(k,ls='--',color='gray');axes[1].set(xlabel='Nombre de groupes k',ylabel='Silhouette moyenne',title='Séparation interne des groupes')
    fig.suptitle('Mall Customers · K-means, k = 2 à 8');fig.tight_layout();fig.savefig(ROOT/'reports'/'choix_k.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,6))
    for g in range(k):
        mask=labels==g;ax.scatter(df.loc[mask,FEATURES[0]],df.loc[mask,FEATURES[1]],s=35,color=colors[g],alpha=.75,label=f'G{g} · n={mask.sum()}')
        ax.scatter(original[g,0],original[g,1],s=160,marker='X',c=colors[g],edgecolor='white',linewidth=1.4)
    ax.set(xlabel='Revenu annuel (k$, libellé de la source)',ylabel='Score de dépense (1–100)',title=f'K-means · {k} groupes descriptifs et centroïdes')
    ax.legend(title='Groupes / X : centroïdes');fig.tight_layout();fig.savefig(ROOT/'reports'/'groupes.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.5));ax.plot(np.arange(1,21),[r['ari_common_160'] for r in resamples],'o-',color='#137e8d');ax.set(xlabel='Répétition (160 clients sur 200)',ylabel='ARI sur les observations communes',ylim=(0,1.02),title='Stabilité à 20 sous-échantillonnages, standardisation réajustée');fig.tight_layout();fig.savefig(ROOT/'reports'/'stabilite.png',dpi=150);plt.close(fig)
    summary={'rows':200,'missing_cells':0,'duplicate_profiles':duplicate_profiles,'primary_features':FEATURES,'selected_k':k,'selection':'Maximum de silhouette parmi K-means k=2..8, sur le même échantillon exploratoire.','silhouette':best['silhouette'],'inertia':best['inertia'],'single_group_inertia':float((z*z).sum()),'comparison':comparison,'stability':stability,'age_sensitivity':sensitivity,'groups':profiles.reset_index().to_dict('records')}
    write_json(ROOT/'reports'/'resultats.json',summary)
    versions={n:importlib.metadata.version(n) for n in ['numpy','pandas','scikit-learn','matplotlib']};(ROOT/'requirements.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
    manifest={'objective':'Clustering descriptif de profils pédagogiques ; pas de ciblage commercial validé.','source':src,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'steps':{'DataCollect':'completed','DataAnalyse':'completed','DataML':'completed'},'features':FEATURES,'excluded':['CustomerID','Genre','Age (analyse primaire uniquement)'],'validation':'Métriques internes, répétitions et sous-échantillonnage ; aucun test indépendant de performance commerciale.','transformations':['IDs lus comme texte','Valeurs brutes préservées','Standardisation pour chaque fit et sous-échantillon','Pas de suppression automatique des profils répétés'],'versions':versions,'seed':SEED,'checks':['200 identifiants uniques','Valeurs absentes et plages','Somme des tailles de groupes = 200','Export numérique rechargé ; 200 affectations identiques'],'raw_redistributed':False,'next_action':'Valider sur des données indépendantes et objectifs métier avant toute utilisation opérationnelle.'}
    write_json(ROOT/'manifest.json',manifest);print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
