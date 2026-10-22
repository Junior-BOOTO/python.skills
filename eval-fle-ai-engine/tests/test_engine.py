import sys
from pathlib import Path
from io import BytesIO
import zipfile
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from evalfle.engine import load_bank,validate_bank,generate_exam,grade_answers,overview,safe_label
from evalfle.exports import build_pdf,build_docx

@pytest.fixture(scope='module')
def bank():return load_bank()

def test_bank_size(bank):assert len(bank)==60

def test_bank_categories(bank):
    for grade in (4,5):
        a=[x for x in bank if x['grade']==grade]
        assert len(a)==30
        assert sorted([sum(x['category']==c for x in a) for c in set(x['category'] for x in a)])==[10,10,10]

def test_bank_unique_questions(bank):assert len(set(x['question'] for x in bank))==len(bank)

def test_bank_bad_id(bank):
    invalid=bank+[bank[0]]
    with pytest.raises(ValueError):validate_bank(invalid)

def test_generate_full_30():
    for grade in (4,5):
        q=generate_exam(grade,n=30,seed=99)
        assert len(q)==30
        assert len(set(x.id for x in q))==30
        assert len(overview(q))==3
        assert [x['count'] for x in overview(q)]==[10]*3

def test_generate_balanced_12_15():
    for n in (12,15):
        q=generate_exam(4,n=n,seed=9)
        assert len(q)==n and len(set(x.id for x in q))==n
        assert all(x['count']==n//3 for x in overview(q))

def test_seed_determinism():assert generate_exam(5,seed=3)==generate_exam(5,seed=3)

def test_seed_changes_variant():assert generate_exam(5,seed=2)!=generate_exam(5,seed=5)

def test_correct_index_after_shuffle(bank):
    expected={x['id']:x['choices'][x['correct_index']] for x in bank}
    for grade in (4,5):
        for seed in (1,2,42,2201):
            for q in generate_exam(grade,seed=seed):
                assert q.choices['ABCD'.index(q.answer)]==expected[q.id]

def test_incorrect_grade():
    with pytest.raises(ValueError):generate_exam(3)

def test_incorrect_n():
    with pytest.raises(ValueError):generate_exam(4,n=29)

def test_correct_answer_grading():
    questions=generate_exam(4,n=12)
    actual=grade_answers(questions,{i:q.answer for i,q in enumerate(questions,1)})
    assert actual['correct']==12
    assert sum(v['correct'] for v in actual['per_category'].values())==12

def test_blank_graded_zero():
    questions=generate_exam(5,n=12)
    assert grade_answers(questions,{})['correct']==0

def test_grade_wrong_case_insensitive():
    q=generate_exam(5,n=12)
    assert grade_answers(q,{1:q[0].answer.lower()})['correct']==1

def test_pdf_student():
    data=build_pdf(generate_exam(4,n=12))
    assert data.startswith(b'%PDF') and len(data)>2000

def test_pdf_teacher():
    data=build_pdf(generate_exam(5,n=30),teacher=True)
    assert data.startswith(b'%PDF') and len(data)>6000

def test_docx_student():
    data=build_docx(generate_exam(4,n=12))
    assert zipfile.is_zipfile(BytesIO(data))

def test_docx_teacher():
    data=build_docx(generate_exam(5,n=30),teacher=True)
    with zipfile.ZipFile(BytesIO(data)) as z:
        assert b'Corrig' in z.read('word/document.xml')

def test_safe_label():assert safe_label('<img>\nEcole')=='imgEcole'
