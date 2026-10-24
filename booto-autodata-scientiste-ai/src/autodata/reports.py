"""Export human-readable report plus machine-readable run metadata."""
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from html import escape
import json
import hashlib
import pandas as pd

def provenance(data: bytes, label: str) -> dict:
    return {'source':label,'sha256':hashlib.sha256(data).hexdigest(), 'bytes':len(data)}

def report_html(result:dict,quality:dict,prov:dict) -> str:
    rows=''.join('<tr><th>'+escape(str(k))+'</th><td>'+escape(str(v))+'</td></tr>'
                 for k,v in result['test_metrics'].get(result['best_model'],{}).items())
    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>BOOTO AutoData — rapport V1</title>
<style>body{{font-family:system-ui;margin:3rem auto;max-width:880px;color:#16304e;padding:0 1rem;line-height:1.6}}h1,h2{{color:#087a83}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #dce7f1;padding:.65rem;text-align:left}}.notice{{background:#eef6ff;padding:1rem;border-left:5px solid #4b8eca}}</style></head>
<body><h1>BOOTO AutoData Scientiste AI — Rapport expérimental V1</h1>
<p>Source : {escape(str(prov['source']))} · SHA-256 : <code>{escape(str(prov['sha256']))}</code></p>
<h2>Données</h2><p>{quality['rows']} lignes · {quality['columns']} colonnes · {quality['duplicates']} doublons · {quality['missing_percent']} % de valeurs manquantes.</p>
<h2>Protocole</h2><p>Tâche : {escape(result['task'])} · Cible : {escape(result['target'])} · Variables retenues : {len(result['columns_used'])}.
{escape(result['method'])} Graine : {result['seed']}.</p>
<h2>Modèle sélectionné</h2><p>{escape(result['best_model'])} (par validation croisée sur entraînement).</p><h2>Mesures sur test réservé</h2><table>{rows}</table>
<h2>Limites et contrôles</h2><div class="notice">{' '.join(escape(x) for x in result['warnings'])}</div>
<p>Ce rapport est généré sur les valeurs calculées réellement. Les données sources ne sont pas jointes à l’export par défaut.</p>
</body></html>"""

def export_zip(result:dict,quality:dict,prov:dict,raw:bytes|None=None,filename:str='source.csv') -> bytes:
    buf=BytesIO()
    safe={k:v for k,v in result.items() if k!='predictions'}
    with ZipFile(buf,'w',ZIP_DEFLATED) as z:
        z.writestr('rapport.html',report_html(result,quality,prov))
        z.writestr('manifeste.json',json.dumps({'experiment':safe,'data_quality':quality,'provenance':prov},ensure_ascii=False,indent=2,default=str))
        # Indices/labels may contain sensitive outcomes: predictions are not exported by default.
        z.writestr('LIRE_MOI.txt','BOOTO AutoData V1. Données et prédictions non incluses par défaut. Conserver la source et vérifier son empreinte SHA-256 avant de reproduire les résultats.\n')
        if raw is not None:
            z.writestr('donnees/'+filename.split('/')[-1].split('\\')[-1],raw)
    return buf.getvalue()
