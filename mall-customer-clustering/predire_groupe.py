"""Affectation illustrative au centroïde le plus proche, pas prédiction d'achat."""
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
def assign(points):
    x=np.asarray(points,dtype=float)
    if x.ndim!=2 or x.shape[1]!=2 or not np.isfinite(x).all():raise ValueError('Tableau fini à deux colonnes : revenu k$, score 1–100.')
    if (x[:,0]<=0).any() or ((x[:,1]<1)|(x[:,1]>100)).any():raise ValueError('Revenu positif et score entre 1 et 100 attendus.')
    with np.load(ROOT/'models'/'kmeans.npz',allow_pickle=False) as model:
        z=(x-model['mean'])/model['scale'];dist=((z[:,None,:]-model['centers'][None,:,:])**2).sum(axis=2)
    return dist.argmin(axis=1),np.sqrt(dist.min(axis=1))
if __name__=='__main__':
    # Exemples inventés, clairement distincts des données sources.
    examples=[[40,50],[90,80]]
    groups,distances=assign(examples)
    for x,g,d in zip(examples,groups,distances):print('Exemple synthétique',x,'-> groupe',int(g),'distance standardisée',round(float(d),3))
