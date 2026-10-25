"""Bounded caches owned by one session, and a portable experience archive."""
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import json
from .quality import profile
from .reports import export_zip
from .notebooks import analysis_notebook, notebook_bytes, printable_notebook


def session_value(state, slot, key, factory):
    previous = state.get(slot)
    if previous is not None and previous['key'] == key:
        return previous['value']
    value = factory()
    state[slot] = {'key': key, 'value': value}
    return value


def diagnostics(frame):
    numeric = frame.select_dtypes(include='number')
    return {'quality': profile(frame),
            'describe': numeric.describe().round(2) if not numeric.empty else None,
            'dataframe_bytes': int(frame.memory_usage(index=True, deep=True).sum())}


def learning_exports(result, quality, prov):
    notebook = analysis_notebook(result, quality, prov)
    return {'notebook': notebook_bytes(notebook), 'html': printable_notebook(notebook)}


def experiment_archive(result, quality, prov, exports, raw=None, filename='source.csv'):
    output = BytesIO()
    with ZipFile(BytesIO(export_zip(result, quality, prov, raw, filename))) as report, ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        for name in report.namelist():
            archive.writestr(name, report.read(name))
        archive.writestr('analyse.ipynb', exports['notebook'])
        archive.writestr('code_imprimable.html', exports['html'])
        archive.writestr('parametres.json', json.dumps({
            'target': result['target'], 'task': result['task'],
            'exclusions': result['columns_excluded'], 'remove_duplicates': result['duplicates_removed'],
            'seed': result['seed'], 'source_sha256': prov['sha256'], 'source_included': raw is not None,
        }, ensure_ascii=False, indent=2))
        archive.writestr('OUVRIR_EXPERIENCE.txt',
            'BOOTO AutoData — archive portable\n'
            'Extraire les fichiers. Placer la source originale ou le CSV collecté à côté du notebook.\n'
            'Si la source est incluse, copier le fichier du dossier donnees/ à côté du notebook sans le renommer.\n'
            'Ouvrir analyse.ipynb dans Jupyter puis exécuter les cellules dans l’ordre.\n'
            'Ouvrir code_imprimable.html dans un navigateur pour consulter ou imprimer (Ctrl+P).\n'
            'Aucune restauration de session dans le site, aucun modèle sérialisé ni prédiction individuelle dans cette archive.\n')
    return output.getvalue()
