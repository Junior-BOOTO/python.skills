import json
import pytest
from booto_fle.engine import (SKILLS, evaluate, group_summary, load_activities,
                               load_question_bank, load_synthetic_profiles, recommend)


@pytest.fixture
def bank():
    return load_question_bank()


def correct_answers(bank):
    return {q['id']: q['answer_index'] for q in bank['items']}


def wrong_answers(bank):
    return {q['id']: (q['answer_index'] + 1) % 3 for q in bank['items']}


def test_bank_12_unique_questions_and_four_skills(bank):
    assert len(bank['items']) == 12
    assert len({q['id'] for q in bank['items']}) == 12
    assert {q['competence'] for q in bank['items']} == set(SKILLS[:-1])


def test_full_success_does_not_recommend_remediation(bank):
    diag = evaluate(correct_answers(bank), oral_score=2, bank=bank)
    assert all(s.status == 'mastered' for s in diag.results)
    assert recommend(diag) == []


def test_full_failure_prioritizes_remediation(bank):
    diag = evaluate(wrong_answers(bank), oral_score=0, bank=bank)
    assert all(s.status == 'priority' for s in diag.results)
    assert len(recommend(diag)) == 3


def test_missing_answers_are_unassessed_not_errors(bank):
    diag = evaluate({}, bank=bank)
    assert diag.answered == 0
    assert all(s.status == 'unassessed' for s in diag.results)
    assert recommend(diag) == []


def test_partially_answered_skill_is_unassessed(bank):
    a = correct_answers(bank)
    a.pop('LEX01')
    diag = evaluate(a, bank=bank)
    assert diag.results[0].status == 'unassessed'
    assert diag.results[1].status == 'mastered'


def test_two_out_of_three_acquired_on_tasks(bank):
    a = correct_answers(bank)
    a['LEX01'] = 1
    diag = evaluate(a, bank=bank)
    assert diag.results[0].status == 'mastered'
    assert diag.results[0].correct == 2


def test_one_out_of_three_in_progress(bank):
    a = wrong_answers(bank)
    a['VER01'] = 0
    diag = evaluate(a, bank=bank)
    assert diag.results[1].status == 'developing'


def test_human_oral_assessment_distinct_from_auto_score(bank):
    a = correct_answers(bank)
    for oral, expected in [(None, 'unassessed'), (0, 'priority'), (1, 'developing'), (2, 'mastered')]:
        diag = evaluate(a, oral_score=oral, bank=bank)
        assert diag.results[-1].status == expected


def test_unknown_question_ids_are_rejected(bank):
    with pytest.raises(ValueError, match='inconnus'):
        evaluate({'FAKE': 1}, bank=bank)


def test_non_numeric_oral_value_rejected(bank):
    with pytest.raises(ValueError, match="orale"):
        evaluate({}, oral_score=5, bank=bank)


def test_invalid_mcq_values_rejected(bank):
    for bad in (-1, 3, '0', True):
        with pytest.raises(ValueError, match='invalide'):
            evaluate({'LEX01': bad}, bank=bank)


def test_correction_does_not_lose_original_learner_answer(bank):
    diag = evaluate({'LEX01': 1}, bank=bank)
    entry = diag.corrections[0]
    assert entry['answer'] == bank['items'][0]['options'][1]
    assert entry['correct_answer'] == bank['items'][0]['options'][0]


def test_recommendation_reason_and_success_criterion(bank):
    diag = evaluate(wrong_answers(bank), bank=bank)
    assert len(recommend(diag, max_activities=2)) == 2
    assert all('motif' in x and 'reussite' in x and 'accompagnement' in x for x in recommend(diag))


def test_zero_limit_returns_no_recommendations(bank):
    diag = evaluate(wrong_answers(bank), bank=bank)
    assert recommend(diag, max_activities=0) == []


def test_activity_catalogue_covers_competencies():
    catalog = load_activities()
    assert set(catalog) == set(SKILLS)


def test_12_profiles_are_exclusively_synthetic():
    profiles = load_synthetic_profiles()
    assert len(profiles) == 12
    assert all(p['student_id'].startswith('SYN-') for p in profiles)


def test_group_summary_counts_add_up_to_12():
    summary = group_summary()
    assert summary['n_profiles'] == 12
    assert all(sum(n.values()) == 12 for n in summary['status_totals'].values())


def test_group_summary_rejects_real_profiles():
    with pytest.raises(ValueError, match='synthétiques'):
        group_summary([{'student_id': 'real-name', 'type_donnees': 'reels', 'answers': {}}])


def test_questionnaire_rejects_duplicate_ids(tmp_path, bank):
    bank['items'][1]['id'] = bank['items'][0]['id']
    p = tmp_path / 'bad.json'
    p.write_text(json.dumps(bank), encoding='utf-8')
    with pytest.raises(ValueError, match='dupliqués'):
        load_question_bank(p)
