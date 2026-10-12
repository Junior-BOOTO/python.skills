"""Vérification de l'export sur un profil entièrement inventé, sans décision de crédit."""
from pathlib import Path
import json,numpy as np
from scipy.special import expit
ROOT=Path(__file__).resolve().parent
def evaluate(values):
    m=json.loads((ROOT/'models/logistique.json').read_text())
    x=np.array([values[n] for n in m['numeric_features']],dtype=float)
    if not np.isfinite(x).all():raise ValueError('Montants finis requis.')
    categorical=[]
    for name,categories in zip(m['categorical_features'],m['categories']):
        value=values[name]
        if value not in categories:raise ValueError(f'Catégorie inconnue pour {name} ; revue nécessaire.')
        categorical.extend(float(value==c) for c in categories)
    prepared=np.r_[(x-np.array(m['mean']))/np.array(m['scale']),categorical]
    return float(expit(prepared@np.array(m['coefficients'])+m['intercept']))
if __name__=='__main__':
    example=json.loads((ROOT/'reports/exemple_synthetique.json').read_text());p=evaluate(example['features'])
    assert abs(p-example['probability'])<1e-12
    print('Export vérifié sur un profil fictif. Aucune décision de crédit produite.')
