"""Tests unitaires du moteur explicable, sans audio ni identités d'élèves."""
from dataclasses import replace
import json
import pytest
from phonofle import DEFAULT_PAIRS, load_pairs, build_quiz, evaluate, teacher_observation

@pytest.fixture
def pairs():
    return load_pairs(DEFAULT_PAIRS)

@pytest.fixture
def quiz(pairs):
    return build_quiz(pairs, count=10, seed=23)


def test_pairs_minimum(pairs): assert len(pairs) >= 10

def test_pairs_have_distinct_words(pairs): assert all(x.word_y != x.word_u for x in pairs)

def test_pairs_ipa_is_present(pairs): assert all(x.ipa_y.startswith('/') and x.ipa_u.startswith('/') for x in pairs)

def test_keys_unique(pairs): assert len({x.key for x in pairs}) == len(pairs)

def test_build_question_count(quiz): assert len(quiz) == 10

def test_build_deterministic(pairs): assert build_quiz(pairs,10,23) == build_quiz(pairs,10,23)

def test_question_two_options(quiz): assert all(len(set(q.options)) == 2 for q in quiz)

def test_all_targets_in_options(quiz): assert all(q.target in q.options for q in quiz)

def test_balance(quiz): assert sum(q.phoneme=='y' for q in quiz) == sum(q.phoneme=='u' for q in quiz)

def test_target_ipa_corresponds_to_pair(quiz,pairs):
    table={p.key:p for p in pairs}
    assert all(q.target_ipa == table[q.pair_key].ipa(q.phoneme) for q in quiz)

def test_question_public_hides_correct(quiz):
    assert all('answer' not in q.public() and 'target' not in q.public() for q in quiz)

def test_score_perfect(quiz):
    result=evaluate(quiz, [q.answer for q in quiz])
    assert result['accuracy_percent']==100 and result['level']=='consolidation'

def test_score_zero(quiz):
    result=evaluate(quiz,[q.distractor for q in quiz])
    assert result['accuracy_percent']==0 and result['level']=='support'
    assert set(result['focus_phonemes'])=={'y','u'}

def test_score_partial(quiz):
    choices=[q.answer for q in quiz[:7]]+[q.distractor for q in quiz[7:]]
    result=evaluate(quiz,choices)
    assert result['correct']==7 and result['level']=='progressing'

def test_missing_not_counted(quiz):
    result=evaluate(quiz,[None]*10)
    assert result['accuracy_percent'] is None and result['answered']==0 and result['level']=='not_scored'

def test_invalid_response_rejected(quiz):
    with pytest.raises(ValueError): evaluate(quiz,['not_an_option']*10)

def test_mismatched_length_rejected(quiz):
    with pytest.raises(ValueError): evaluate(quiz,[quiz[0].answer])

def test_too_many_questions_rejected(pairs):
    with pytest.raises(ValueError): build_quiz(pairs,100)

def test_too_few_questions_rejected(pairs):
    with pytest.raises(ValueError): build_quiz(pairs,1)

def test_reject_too_few_pairs(pairs):
    with pytest.raises(ValueError): build_quiz(pairs[:3])

def test_reject_duplicate_pair_ids(tmp_path,pairs):
    data=[pairs[0].__dict__,pairs[0].__dict__,pairs[1].__dict__,pairs[2].__dict__]
    file=tmp_path/'duplicate.json';file.write_text(json.dumps(data))
    with pytest.raises(ValueError):load_pairs(file)

def test_teacher_complete():
    x=teacher_observation({'mouth_position':2,'word_repetition':1,'short_phrase':0})
    assert x['points']==3 and x['maximum']==6 and x['automatic_pronunciation_score'] is False

def test_teacher_invalid():
    with pytest.raises(ValueError):teacher_observation({'mouth_position':3,'word_repetition':1,'short_phrase':1})

def test_teacher_boolean_rejected():
    with pytest.raises(ValueError):teacher_observation({'mouth_position':True,'word_repetition':1,'short_phrase':1})

def test_teacher_missing_criterion_rejected():
    with pytest.raises(ValueError):teacher_observation({'mouth_position':1,'word_repetition':2})

def test_recommendations_both_confusions(quiz):
    result=evaluate(quiz,[q.distractor for q in quiz])
    assert any('/y/' in item for item in result['recommendations'])
    assert any('/u/' in item for item in result['recommendations'])

def test_odd_length_sound_balance(pairs):
    quiz=build_quiz(pairs,count=11)
    n=sum(q.phoneme=='y' for q in quiz)
    assert abs(n-(11-n))==1

def test_no_student_data_in_report(quiz):
    data=json.dumps(evaluate(quiz,[q.answer for q in quiz]))
    assert 'name' not in data and 'microphone' not in data

