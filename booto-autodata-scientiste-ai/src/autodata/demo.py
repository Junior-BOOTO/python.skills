"""Two reproducible artificial datasets, no real-person records."""
from io import StringIO
import numpy as np
import pandas as pd
from .ingestion import validate_frame

def make_demo(kind:str, n:int=180)->pd.DataFrame:
    rng=np.random.default_rng(2026)
    experience=rng.integers(0,18,n)
    hours=rng.normal(37,8,n).clip(10,65).round(1)
    sector=rng.choice(['commerce','education','industrie'],size=n)
    level=rng.choice(['debutant','intermediaire','avance'],size=n)
    if kind=='regression':
        target=(900+experience*75+hours*18+(sector=='industrie')*350+rng.normal(0,170,n)).round(0)
        name='montant_simule'
    elif kind=='classification':
        logits=experience*.16+hours*.065+(level=='avance')*.9-4.3+rng.normal(0,.8,n)
        target=np.where(logits>0,'categorie_B','categorie_A')
        name='categorie_fictive'
    else:
        raise ValueError('type de jeu inconnu')
    df=pd.DataFrame({'experience_simulee':experience,'heures_simulees':hours,'secteur_fictif':sector,
                     'niveau_fictif':level,name:target})
    df.loc[np.arange(0,n,19),'heures_simulees']=np.nan
    return validate_frame(df)
