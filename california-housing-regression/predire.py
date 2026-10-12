"""Exemple historique de zone, sans chargement pickle et sans clipping implicite."""
from pathlib import Path
import json,numpy as np
ROOT=Path(__file__).resolve().parent
def predict(values):
    model=json.loads((ROOT/'models/regression.json').read_text())
    x=np.array([values[feature] for feature in model['features']],dtype=float)
    if not np.isfinite(x).all():raise ValueError('Toutes les valeurs doivent être finies.')
    return float(((x-np.array(model['mean']))/np.array(model['scale']))@np.array(model['coefficients_standardized'])+model['intercept_standardized'])
if __name__=='__main__':
    example=json.loads((ROOT/'reports/exemple_synthetique.json').read_text())
    value=predict(example['input'])
    assert abs(value-example['prediction'])<1e-7
    print('Profil synthétique de zone :',round(value,2),'USD de 1990 ; pas estimation immobilière actuelle.')
