"""Export readable, reproducible Python analysis and a printable companion."""
from pathlib import Path
from html import escape
import hashlib
import json
import platform
import numpy as np
import pandas as pd
import scipy
import sklearn
import openpyxl


def analysis_notebook(result, quality, prov):
    cells = []
    def markdown(text):
        cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': text.splitlines(True)})
    def code(text, tables=()):
        outputs = [{'output_type': 'display_data', 'metadata': {}, 'data': {'text/html': [table.to_html(index=False, escape=True)], 'text/plain': [table.to_string(index=False)]}} for table in tables]
        cells.append({'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'source': text.splitlines(True), 'outputs': outputs})

    filename = str(prov['source']).replace('\\', '/').split('/')[-1]
    versions = {'pandas': pd.__version__, 'numpy': np.__version__, 'scipy': scipy.__version__, 'scikit-learn': sklearn.__version__, 'openpyxl': openpyxl.__version__}
    markdown('# BOOTO AutoData Scientiste AI — Notebook explicatif\n\nAuteur du projet : Junior BOOTO Waba.\n\n'
             'Ce notebook contient le code Python du traitement : lecture, contrôles, diagnostic, préparation, comparaison, évaluation et rapport. '
             'Les résultats enregistrés ci-dessous proviennent de l’analyse réalisée dans l’application ; ils ne signifient pas que ce notebook a déjà été exécuté.\n\n'
             'Exécutez les cellules dans l’ordre. La cible, la tâche et les exclusions sont celles de cette expérience. '
             'Le choix du modèle utilise uniquement la validation croisée sur entraînement. '
             'Les scores ne garantissent pas la performance sur de nouvelles données.\n\n'
             'Les données d’origine ne sont pas intégrées. Placez le fichier source à côté du notebook. '
             'Pour une collecte Web, utilisez le CSV normalisé téléchargeable dans l’application. '
             'L’empreinte SHA-256 est vérifiée avant lecture.\n\n'
             f'Environnement de référence : Python {platform.python_version()}. '
             'Pour imprimer : utilisez le fichier HTML compagnon, puis Ctrl+P → Imprimer ou Enregistrer en PDF.')
    markdown('## 1. Dépendances\n\nCette cellule installe les versions utilisées. À exécuter dans un environnement Jupyter dédié.')
    code('%pip install ' + ' '.join(f'{key}=={value}' for key, value in versions.items()))
    markdown('## 2. Code complet du traitement\n\nLes fonctions suivantes sont copiées des modules de l’application. '
             'Seuls les imports relatifs entre ces modules sont retirés : toutes les fonctions sont ici dans le même notebook. '
             'Les commentaires et chaque ligne de calcul sont conservés.')
    for name, title in [('ingestion', 'Lecture et contrôles'), ('quality', 'Diagnostic qualité'), ('task_router', 'Vérification de la tâche'), ('training', 'Préparation, validation et modèles'), ('reports', 'Rapport et manifeste')]:
        markdown('### ' + title)
        source = (Path(__file__).parent / f'{name}.py').read_text(encoding='utf-8')
        source = ''.join(line for line in source.splitlines(True) if not line.startswith('from .'))
        code(source)
    if 'collection' in prov:
        markdown('### Collecte publique — code du connecteur\n\nCe code permet de comprendre la collecte initiale. '
                 'La réexécution de l’analyse utilise le CSV collecté et son empreinte, sans renouveler automatiquement les appels réseau. '
                 'Les paramètres d’URL ont été masqués dans la traçabilité.')
        source = (Path(__file__).parent / 'collection.py').read_text(encoding='utf-8')
        code(''.join(line for line in source.splitlines(True) if not line.startswith('from .')))
    markdown('## 3. Paramètres et fichier source\n\nAdaptez SOURCE_FILE si le fichier a été renommé. Une empreinte différente interrompt la reproduction.')
    code('from pathlib import Path\nfrom IPython.display import display\nimport hashlib\nimport json\n\n'
         f'SOURCE_FILE = Path({filename!r})\nEXPECTED_SHA256 = {prov["sha256"]!r}\n'
         f'TARGET = {result["target"]!r}\nTASK = {result["task"]!r}\nEXCLUSIONS = {result["columns_excluded"]!r}\n'
         f'REMOVE_DUPLICATES = {result["duplicates_removed"]!r}\n\n'
         'source_bytes = SOURCE_FILE.read_bytes()\n'
         "if hashlib.sha256(source_bytes).hexdigest() != EXPECTED_SHA256:\n    raise ValueError('Le fichier diffère de la source de cette expérience.')\n"
         'df = read_upload(source_bytes, SOURCE_FILE.name)\ndisplay(df.head(20))\n')
    markdown('## 4. Qualité des données\n\nLe diagnostic conserve les données intactes. Les éventuelles imputations sont apprises dans les plis d’entraînement.')
    code("quality = profile(df)\ndisplay(pd.DataFrame(quality['column_details']))\n", (pd.DataFrame(quality['column_details']),))
    markdown('## 5. Entraînement et sélection\n\nLa séparation, les transformations et la graine sont définies dans run_experiment ci-dessus. '
             'Les cinq modèles candidats utilisent les mêmes plis. Le test réservé ne sert pas à choisir le gagnant.')
    code('result = run_experiment(df, TARGET, TASK, EXCLUSIONS, remove_duplicates=REMOVE_DUPLICATES)\n'
         "print(result['method'])\nprint('Modèle retenu :', result['best_model'])\n"
         "display(pd.DataFrame(result['comparison_cv']).drop(columns=['score_validation_train']))\n",
         (pd.DataFrame(result['comparison_cv']).drop(columns=['score_validation_train']),))
    markdown('## 6. Évaluation sur le test réservé\n\nClassification : accuracy = proportion correcte ; balanced_accuracy = rappel moyen des classes ; '
             'F1 macro = F1 moyen des classes. Régression : MAE = erreur absolue moyenne ; RMSE pénalise davantage les grandes erreurs ; '
             'R² compare la variance résiduelle à celle des observations du test.')
    code("display(pd.DataFrame(result['test_metrics']).T)\n"
         "if result['confusion']:\n    display(pd.DataFrame(result['confusion']['matrix'], index=result['confusion']['labels'], columns=result['confusion']['labels']))\n",
         (pd.DataFrame(result['test_metrics']).rename_axis('modèle').reset_index(),))
    markdown('## 7. Prédictions\n\nLes valeurs individuelles ne sont pas enregistrées dans le notebook exporté. '
             'Cette cellule les calcule localement après entraînement ; le résidu de régression vaut réel moins prédit.')
    code("predictions = result['predictions'].copy()\nif TASK == 'regression':\n    predictions['residu'] = predictions['valeur_reelle'] - predictions['prediction']\ndisplay(predictions)\n")
    markdown('## 8. Rapport reproductible\n\nLe rapport contient les métriques recalculées. Les données et prédictions individuelles ne sont pas incluses dans le ZIP par défaut.')
    code('prov = provenance(source_bytes, SOURCE_FILE.name)\n'
         "Path('booto_autodata_rapport_reproduit.zip').write_bytes(export_zip(result, quality, prov))\n"
         "print('Rapport créé.')\n")
    markdown('## Résumé enregistré de l’expérience\n\nModèle retenu : ' + result['best_model'] + '\n\n' + result['method'] + '\n\n' + '\n'.join('- ' + str(w) for w in result['warnings']))
    for index, cell in enumerate(cells):
        cell['id'] = hashlib.sha256(f'{index}'.encode()).hexdigest()[:12]
    return {'nbformat': 4, 'nbformat_minor': 5, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python', 'version': platform.python_version()}, 'booto': {'source_sha256': prov['sha256'], 'versions': versions, 'outputs': 'Snapshots de l’expérience dans l’application ; cellules non exécutées dans ce notebook.'}}, 'cells': cells}


def notebook_bytes(notebook):
    return json.dumps(notebook, ensure_ascii=False, indent=2).encode('utf-8')


def printable_notebook(notebook):
    sections = []
    for cell in notebook['cells']:
        source = ''.join(cell['source'])
        if cell['cell_type'] == 'markdown':
            sections.append('<div class="explanation">' + escape(source) + '</div>')
        else:
            lines = ''.join('<li><code>' + escape(line or ' ') + '</code></li>' for line in source.splitlines())
            sections.append('<ol class="code">' + lines + '</ol>')
            for output in cell['outputs']:
                # Only application-generated escaped DataFrame HTML is included.
                sections.append('<div class="output">' + ''.join(output['data'].get('text/html', [])) + '</div>')
    return ('<!doctype html><html lang="fr"><meta charset="utf-8"><title>BOOTO AutoData — Code et notebook imprimable</title>'
            '<style>body{font:14px system-ui;color:#16304e;max-width:1100px;margin:2rem auto;padding:1rem}'
            '.explanation{white-space:pre-wrap;margin:1.5rem 0;font-size:15px;overflow-wrap:anywhere}'
            '.code{background:#f1f6fa;padding:1rem 1rem 1rem 4rem;border:1px solid #dbe5ed}'
            '.code li{padding-left:.5rem;white-space:pre-wrap;overflow-wrap:anywhere;font:11px monospace;break-inside:avoid}'
            'table{border-collapse:collapse;font-size:11px}td,th{padding:.3rem;border:1px solid #ccd8e3}'
            '.output{overflow-x:auto} @page{size:A4;margin:15mm}@media print{body{margin:0;padding:0}.code{background:white}.output{overflow:visible}table{width:100%}thead{display:table-header-group}}</style>'
            '<h1>BOOTO AutoData — Code Python et résultats</h1><p>Impression : Ctrl+P → Imprimer ou Enregistrer en PDF.</p>'
            + ''.join(sections) + '</html>').encode('utf-8')
