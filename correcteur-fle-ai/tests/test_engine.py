from pathlib import Path
import sys
from io import BytesIO
from zipfile import ZipFile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import pytest
from correcteur_fle import analyze,review_suggestions,to_docx,to_pdf,to_text,RULES


def test_routine_basic():
    result=analyze('je se leve et je va a sept heures.','routine')
    assert 'je me lève' in result.preview and 'je vais' in result.preview and 'à sept heures' in result.preview


def test_eco_basic():
    result=analyze('je doit protege les arbre. nous doit recycler les dechets.','ecologie')
    assert 'je dois protéger' in result.preview
    assert 'les arbres' in result.preview
    assert 'nous devons' in result.preview
    assert 'les déchets' in result.preview


def test_no_cross_theme():
    assert not analyze('je doit','routine').suggestions
    assert not analyze('je va','ecologie').suggestions


def test_preserve_case():
    assert 'Je me lève' in analyze('Je se leve.','routine').preview


def test_no_claim_perfect():
    a=analyze('Phrase libre non analysable.','routine')
    assert not a.suggestions
    assert 'ne garantit pas' in a.observation


def test_ignore_nonmatching():
    assert analyze('Je vais à l’école.','routine').preview=='Je vais à l’école.'


def test_reject_all():
    result=analyze('je va et je manges','routine')
    assert review_suggestions(result.original,result.suggestions,set())==result.original


def test_partial_review():
    result=analyze('je va et je manges','routine')
    actual=review_suggestions(result.original,result.suggestions,{0})
    assert actual=='je vais et je manges'


def test_spans_consistent():
    r=analyze('je se leve. je va.','routine')
    assert all(r.original[s.start:s.end]==s.original for s in r.suggestions)
    assert [(s.start,s.end) for s in r.suggestions]==sorted((s.start,s.end) for s in r.suggestions)


def test_reject_out_of_range():
    r=analyze('je va','routine')
    with pytest.raises(ValueError):review_suggestions(r.original,r.suggestions,{99})


def test_no_text():
    with pytest.raises(ValueError):analyze('  ','routine')


def test_unknown_theme():
    with pytest.raises(ValueError):analyze('je va','unknown')


def test_size_cap():
    with pytest.raises(ValueError):analyze('a'*901,'routine')


def test_rules_unique():
    assert len({x.ident for x in RULES})==len(RULES)


def test_rule_correction_no_overlap():
    a=analyze('je se leve je me leve','routine')
    assert a.preview=='je me lève je me lève'


def test_docx_output():
    a=analyze('je va et je manges','routine')
    result=to_docx(a,{1},'Observer la conjugaison.')
    with ZipFile(BytesIO(result)) as z:
        xml=z.read('word/document.xml').decode()
        assert 'je va et je mange' in xml
        assert 'Observer la conjugaison' in xml
        assert 'je vais et je mange' not in xml


def test_pdf_output():
    a=analyze('je se leve.','routine')
    assert to_pdf(a,{0}).startswith(b'%PDF')


def test_empty_selection_exports():
    a=analyze('je va','routine')
    assert 'Aucune proposition retenue' in to_text(a,set())
    assert to_docx(a,set())[:2]==b'PK'


def test_text_feedback():
    a=analyze('je va','routine')
    t=to_text(a,{0},'Rappel du verbe aller.')
    assert 'je vais' in t and 'Rappel du verbe aller' in t


def test_html_injection_is_plain_text():
    a=analyze('<script>alert(1)</script> je va','routine')
    assert '<script>alert(1)</script>' in review_suggestions(a.original,a.suggestions)
    assert to_pdf(a,{0}).startswith(b'%PDF')


def test_multi_occurrences():
    a=analyze('je va et je va','routine')
    assert len(a.suggestions)==2
    assert a.preview=='je vais et je vais'


def test_unchanged_input():
    text='Je me lève à huit heures.'
    a=analyze(text,'routine')
    assert a.original==text
