from io import BytesIO
from zipfile import ZipFile
import json
import pytest
from autodata.efficiency import session_value, diagnostics, learning_exports, experiment_archive
from autodata.demo import make_demo
from autodata.training import run_experiment
from autodata.reports import provenance


def test_cache_hit_invalidation_and_session_isolation():
    calls = []
    def compute():
        calls.append(1)
        return len(calls)
    first, second = {}, {}
    assert session_value(first, 'slot', 'a', compute) == 1
    assert session_value(first, 'slot', 'a', compute) == 1
    assert session_value(first, 'slot', 'b', compute) == 2
    assert session_value(second, 'slot', 'b', compute) == 3
    assert len(first) == 1


def test_failed_computation_not_cached():
    state = {}
    def fail():
        raise ValueError('failure')
    with pytest.raises(ValueError):
        session_value(state, 'slot', 'a', fail)
    assert not state


def test_diagnostics_does_not_change_data():
    frame = make_demo('regression')
    before = frame.copy(deep=True)
    result = diagnostics(frame)
    assert frame.equals(before)
    assert result['quality']['rows'] == len(frame)
    assert result['dataframe_bytes'] == int(frame.memory_usage(index=True, deep=True).sum())


@pytest.mark.parametrize('include_source', [False, True])
def test_complete_archive_integrity_and_source_opt_in(include_source):
    frame = make_demo('classification')
    raw = frame.to_csv(index=False).encode()
    result = run_experiment(frame, frame.columns[-1], 'classification')
    quality = diagnostics(frame)['quality']
    prov = provenance(raw, 'source.csv')
    exports = learning_exports(result, quality, prov)
    output = experiment_archive(result, quality, prov, exports, raw if include_source else None, 'source.csv')
    with ZipFile(BytesIO(output)) as archive:
        assert archive.testzip() is None
        assert {'rapport.html', 'manifeste.json', 'analyse.ipynb', 'code_imprimable.html', 'parametres.json', 'OUVRIR_EXPERIENCE.txt'} <= set(archive.namelist())
        assert ('donnees/source.csv' in archive.namelist()) == include_source
        config = json.loads(archive.read('parametres.json'))
        assert config['source_sha256'] == prov['sha256']
        assert config['source_included'] == include_source
        assert json.loads(archive.read('analyse.ipynb'))['nbformat'] == 4
        assert 'predictions' not in json.loads(archive.read('manifeste.json'))['experiment']
