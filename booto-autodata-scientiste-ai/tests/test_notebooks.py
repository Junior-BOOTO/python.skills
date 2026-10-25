from io import BytesIO
import json
from zipfile import ZipFile
import pandas as pd
import pytest
from autodata.demo import make_demo
from autodata.training import run_experiment
from autodata.quality import profile
from autodata.reports import provenance
from autodata.notebooks import analysis_notebook, notebook_bytes, printable_notebook


@pytest.mark.parametrize('task', ['classification', 'regression'])
def test_notebook_reexecutes_entire_analysis(task, tmp_path, monkeypatch):
    frame = make_demo(task)
    raw = frame.to_csv(index=False).encode()
    # Train from the same parsed bytes the notebook will read.
    frame = pd.read_csv(BytesIO(raw))
    result = run_experiment(frame, frame.columns[-1], task)
    prov = provenance(raw, 'source.csv')
    prov['collection'] = {'sources': []}
    notebook = analysis_notebook(result, profile(frame), prov)
    loaded = json.loads(notebook_bytes(notebook))
    assert loaded['nbformat'] == 4
    assert all('id' in cell for cell in loaded['cells'])
    assert all(cell.get('execution_count') is None for cell in loaded['cells'])
    assert b'valeur_reelle' not in json.dumps([c.get('outputs', []) for c in loaded['cells']]).encode()
    (tmp_path / 'source.csv').write_bytes(raw)
    monkeypatch.chdir(tmp_path)
    namespace = {}
    for cell in loaded['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if not source.startswith('%pip'):
                exec(compile(source, '<exported notebook>', 'exec'), namespace)
    assert namespace['result']['best_model'] == result['best_model']
    assert namespace['result']['test_metrics'] == result['test_metrics']
    with ZipFile(tmp_path / 'booto_autodata_rapport_reproduit.zip') as archive:
        assert 'rapport.html' in archive.namelist()
    printable = printable_notebook(loaded).decode()
    assert 'Ctrl+P' in printable and '@page' in printable
    assert 'run_experiment' in printable and '<li><code>' in printable


def test_print_escapes_source_and_tables():
    frame = make_demo('regression')
    result = run_experiment(frame, frame.columns[-1], 'regression')
    result['target'] = '<script>alert(1)</script>'
    notebook = analysis_notebook(result, profile(frame), provenance(b'data', 'source.csv'))
    output = printable_notebook(notebook).decode()
    assert '<script>' not in output
    assert '&lt;script&gt;' in output
