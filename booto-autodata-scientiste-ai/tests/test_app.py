from streamlit.testing.v1 import AppTest
import pytest
from pathlib import Path
APP = Path(__file__).resolve().parents[1] / "app" / "main.py"


@pytest.mark.parametrize('choice', ['Démonstration — classification', 'Démonstration — régression'])
def test_demo_end_to_end(choice):
    app = AppTest.from_file(APP, default_timeout=60).run()
    app.radio[0].set_value(choice).run()
    assert not app.exception
    app.checkbox[1].check().run()
    app.button[0].click().run()
    assert not app.exception
    assert not app.error
    assert app.success
    assert app.session_state['exp_result']['test_rows'] == 45


def test_all_missing_numeric_exploration_does_not_crash(monkeypatch):
    import autodata.demo as demo
    original = demo.make_demo
    def with_empty_numeric(kind):
        frame = original(kind)
        frame['vide'] = float('nan')
        return frame
    monkeypatch.setattr(demo, 'make_demo', with_empty_numeric)
    app = AppTest.from_file(APP, default_timeout=60).run()
    app.selectbox[0].set_value('vide').run()
    assert not app.exception
    assert not app.error
