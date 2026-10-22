"""Générateur déterministe d'évaluations QCM FLE. Aucune certification CECRL."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parents[2]
BANK_PATH = ROOT / 'data' / 'banque_demo_a1.json'
LETTERS = ('A', 'B', 'C', 'D')


@dataclass(frozen=True)
class Question:
    id: str
    grade: int
    category: str
    criterion: str
    question: str
    choices: tuple[str, str, str, str]
    answer: str


def load_bank(path: Path = BANK_PATH) -> list[dict]:
    items = json.loads(Path(path).read_text(encoding='utf-8'))
    validate_bank(items)
    return items


def validate_bank(items: list[dict]) -> None:
    if not isinstance(items, list) or not items:
        raise ValueError('Banque de questions vide ou invalide.')
    ids = set()
    for item in items:
        needed = ('id','grade','category','criterion','question','choices','correct_index')
        if any(k not in item for k in needed):
            raise ValueError('Métadonnées de question incomplètes.')
        if item['id'] in ids:
            raise ValueError(f"Identifiant en double : {item['id']}")
        ids.add(item['id'])
        if item['grade'] not in (4, 5):
            raise ValueError('Niveau non pris en charge.')
        choices = item['choices']
        if not isinstance(choices, list) or len(choices) != 4 or len(set(choices)) != 4:
            raise ValueError(f"Les choix doivent être 4 réponses distinctes : {item['id']}")
        if not isinstance(item['correct_index'], int) or not 0 <= item['correct_index'] <= 3:
            raise ValueError('Index de correction invalide.')
        for key in ('question', 'criterion', 'category'):
            if not isinstance(item[key], str) or not item[key].strip():
                raise ValueError(f'Champ {key} absent.')


def generate_exam(grade: int, seed: int = 2026, n: int = 30, bank: list[dict] | None = None) -> list[Question]:
    if grade not in (4, 5):
        raise ValueError('Les niveaux pris en charge sont Grade 4 et Grade 5.')
    if n not in (12, 15, 30):
        raise ValueError('Les formats disponibles sont 12, 15 ou 30 questions.')
    entries = load_bank() if bank is None else bank
    validate_bank(entries)
    groups = {}
    for it in entries:
        if it['grade'] == grade:
            groups.setdefault(it['category'], []).append(it)
    if len(groups) != 3:
        raise ValueError('La version initiale exige trois domaines distincts par niveau.')
    target, rem = divmod(n, 3)
    rng = random.Random(seed)
    picked = []
    for i, (_, questions) in enumerate(sorted(groups.items())):
        count = target + (i < rem)
        if len(questions) < count:
            raise ValueError('Banque insuffisante pour le nombre demandé.')
        picked.extend(rng.sample(questions, count))
    rng.shuffle(picked)
    output = []
    for source in picked:
        options = list(enumerate(source['choices']))
        rng.shuffle(options)
        right_new = next(i for i, (old, _) in enumerate(options) if old == source['correct_index'])
        output.append(Question(id=source['id'], grade=grade, category=source['category'],
                               criterion=source['criterion'], question=source['question'],
                               choices=tuple(v for _, v in options), answer=LETTERS[right_new]))
    return output


def overview(questions: list[Question]) -> list[dict]:
    categories = sorted(set(q.category for q in questions))
    return [{'category':c, 'count':sum(q.category==c for q in questions),
             'criterion':next(q.criterion for q in questions if q.category==c)} for c in categories]


def grade_answers(questions: list[Question], answers: dict[int, str]) -> dict:
    if not questions:
        raise ValueError('Évaluation vide.')
    per = {c:{'correct':0,'total':0} for c in sorted({q.category for q in questions})}
    for i,q in enumerate(questions, 1):
        per[q.category]['total'] += 1
        if answers.get(i, '').upper() == q.answer:
            per[q.category]['correct'] += 1
    return {'correct':sum(v['correct'] for v in per.values()), 'total':len(questions), 'per_category':per}


def safe_label(text: str, limit: int = 80) -> str:
    """Texte de titre facultatif ; aucun HTML ni caractères de contrôle."""
    return ''.join(c for c in text if c.isprintable() and c not in '<>\r\n\t')[:limit].strip()
