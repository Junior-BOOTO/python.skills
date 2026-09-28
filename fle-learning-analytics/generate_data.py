"""Generate explicitly synthetic, reproducible FLE assessment records."""
import csv
import random
from pathlib import Path

SKILLS = ('CO', 'CE', 'PO', 'PE')
GRADES = (2, 3, 4, 5)
OUT = Path(__file__).parent / 'data' / 'synthetic_assessments.csv'


def generate(seed=20260928):
    rng = random.Random(seed)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['synthetic_id', 'grade', 'period', 'skill', 'criterion_1', 'criterion_2', 'criterion_3', 'support'])
        writer.writeheader()
        for grade in GRADES:
            for index in range(1, 9):
                student = f'SYN-G{grade}-{index:02d}'
                for skill in SKILLS:
                    # Three local criteria scored 0–3. This is illustrative data, not a CEFR level.
                    baseline = [max(0, min(3, round(rng.gauss(1.8 + .12*(grade-2) - (.28 if skill == 'PO' else 0), .55)))) for _ in range(3)]
                    gains = [1 if rng.random() < (.48 if skill == 'PO' else .30) else 0 for _ in range(3)]
                    followup = [min(3, a+b) for a,b in zip(baseline,gains)]
                    for period, scores in [('T1', baseline), ('T2', followup)]:
                        writer.writerow(dict(synthetic_id=student, grade=grade, period=period, skill=skill,
                                             criterion_1=scores[0], criterion_2=scores[1], criterion_3=scores[2],
                                             support='visuals + model' if grade == 2 else 'visual prompt'))
    print(f'Wrote {OUT}')


if __name__ == '__main__':
    generate()
