"""Reproduce a toy diagnostic on a fictional learner; no audio is recorded."""
from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from phonofle import DEFAULT_PAIRS, load_pairs, build_quiz, evaluate

quiz = build_quiz(load_pairs(DEFAULT_PAIRS), count=10, seed=2026)
choices = [item.answer if idx not in (1, 5, 8) else item.distractor for idx, item in enumerate(quiz)]
report = evaluate(quiz, choices)
print(json.dumps({key: value for key, value in report.items() if key != 'responses'}, ensure_ascii=False, indent=2))
