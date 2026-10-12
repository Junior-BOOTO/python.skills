"""Collecte API réelle, vérification et analyse descriptive sans transfert manuel."""
from pathlib import Path
from datetime import date,datetime,timezone,timedelta
import json,csv,hashlib,urllib.request,urllib.parse,statistics,sys
ROOT=Path(__file__).resolve().parent
PARAMS={'latitude':4.7110,'longitude':-74.0721,'start_date':'2025-01-01','end_date':'2025-12-31','daily':'temperature_2m_mean,precipitation_sum','timezone':'America/Bogota','models':'era5'}
URL='https://archive-api.open-meteo.com/v1/archive?'+urllib.parse.urlencode(PARAMS)
def main(refresh=False):
    for name in ['raw','collected','analysis','reports','models']:(ROOT/name).mkdir(exist_ok=True)
    path=ROOT/'raw/reponse.json'
    if refresh or not path.exists():
        with urllib.request.urlopen(URL,timeout=30) as response:
            if response.status!=200:raise RuntimeError(f'HTTP {response.status}')
            content=response.read()
        parsed=json.loads(content)
        if parsed.get('error'):raise RuntimeError(parsed.get('reason','Erreur API'))
        # Historiser les réponses au lieu d'écraser une collecte antérieure.
        if path.exists():
            archive=ROOT/'raw'/('reponse_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json')
            path.rename(archive)
        path.write_bytes(content)
    d=json.loads(path.read_text());assert not d.get('error') and d['timezone']=='America/Bogota'
    daily=d['daily'];units=d['daily_units'];assert units['temperature_2m_mean']=='°C' and units['precipitation_sum']=='mm'
    start=date.fromisoformat(PARAMS['start_date']);end=date.fromisoformat(PARAMS['end_date'])
    expected=[(start+timedelta(days=i)).isoformat() for i in range((end-start).days+1)]
    assert daily['time']==expected
    assert all(len(daily[name])==len(expected) for name in ['temperature_2m_mean','precipitation_sum'])
    rows=[{'date':dt,'temperature_moyenne_c':temp,'precipitations_mm':rain} for dt,temp,rain in zip(daily['time'],daily['temperature_2m_mean'],daily['precipitation_sum'])]
    missing=sum(value is None for row in rows for value in [row['temperature_moyenne_c'],row['precipitations_mm']])
    if missing:raise ValueError(f'{missing} valeurs absentes : analyse interrompue, pas imputation arbitraire.')
    assert all(isinstance(row['temperature_moyenne_c'],(float,int)) and isinstance(row['precipitations_mm'],(float,int)) and row['precipitations_mm']>=0 for row in rows)
    with (ROOT/'collected/bogota_2025.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    monthly=[]
    for month in sorted(set(row['date'][:7] for row in rows)):
        subset=[row for row in rows if row['date'].startswith(month)]
        monthly.append({'mois':month,'jours':len(subset),'temperature_moyenne_c':statistics.mean(row['temperature_moyenne_c'] for row in subset),'precipitations_totales_mm':sum(row['precipitations_mm'] for row in subset)})
    with (ROOT/'analysis/mensuel.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(monthly[0]));w.writeheader();w.writerows(monthly)
    assert sum(row['jours'] for row in monthly)==365
    total=sum(row['precipitations_mm'] for row in rows)
    assert abs(sum(row['precipitations_totales_mm'] for row in monthly)-total)<1e-8
    result={'jours':365,'valeurs_absentes':missing,'temperature_moyenne_annuelle_c':statistics.mean(row['temperature_moyenne_c'] for row in rows),'precipitations_annuelles_mm':total,'coordonnees_demandees':[PARAMS['latitude'],PARAMS['longitude']],'coordonnees_grille_retournees':[d['latitude'],d['longitude']],'elevation_grille_m':d['elevation'],'timezone':d['timezone'],'nature':'Réanalyse ERA5 via Open-Meteo, pas observation directe de station'}
    (ROOT/'reports/resultats.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    manifest={'objectif':'Tester une collecte API réelle et une analyse enchaînée sur Bogotá 2025','requete':URL,'parametres':PARAMS,'reponse_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'verifications':['365 dates consécutives et uniques','Unités °C/mm et timezone','Absences contrôlées','Totaux mensuels et annuel réconciliés'],'etapes':{'DataCollect':'completed','DataAnalyse':'completed','DataML':'pending'},'raison_ml':'Exécuter analyser_modeliser.py pour le modèle J+1 ; les sorties précédentes ne sont pas revalidées par une nouvelle collecte seule.','licence':'Données CC BY 4.0 ; attribution Open-Meteo et Copernicus ERA5. Accès gratuit API destiné au non-commercial, conditions à vérifier pour offre commerciale.','connexion_gpt':'Appel exécuté depuis le script ; aucune action installée dans les trois GPT indépendants.','prochaine_etape':'Configurer et tester l’action DataCollect ; définir ensuite les données et objectifs utiles aux autres assistants.'}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main('--refresh' in sys.argv)
