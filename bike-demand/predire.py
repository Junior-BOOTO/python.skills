"""Exemple calendaire historique ; ne pas extrapoler à une année actuelle."""
from pathlib import Path
import json, joblib, numpy as np, pandas as pd
P=Path(__file__).resolve().parent
model=joblib.load(P/'models/pipeline.joblib') # uniquement le modèle de provenance vérifiée du projet
example=pd.DataFrame([{'hr':8,'weekday':1,'mnth':10,'workingday':1,'holiday':0,'yr':1}])
pred=np.maximum(0,model.predict(example))
print(json.dumps({'scenario':'Lundi ouvré, octobre 2012, 8h','locations_estimees':float(pred[0])},ensure_ascii=False))
