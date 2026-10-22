"""PhonoFLE AI V1: deterministic, explainable auditory-discrimination engine.

This module does NOT assess recorded pronunciation and does not claim
speech recognition, machine learning, or CEFR certification.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import random
from collections import Counter
from typing import Iterable

SOUND_LABELS = {"y": "/y/ — u français", "u": "/u/ — ou français"}
MAX_ITEMS = 24


@dataclass(frozen=True)
class Pair:
    key: str
    word_y: str
    word_u: str
    ipa_y: str
    ipa_u: str
    meaning_y_es: str
    meaning_u_es: str

    def word(self, phoneme: str) -> str:
        if phoneme not in SOUND_LABELS:
            raise ValueError("Phonème inconnu")
        return self.word_y if phoneme == "y" else self.word_u

    def ipa(self, phoneme: str) -> str:
        if phoneme not in SOUND_LABELS:
            raise ValueError("Phonème inconnu")
        return self.ipa_y if phoneme == "y" else self.ipa_u


@dataclass(frozen=True)
class Question:
    number: int
    pair_key: str
    target: str
    answer: str
    distractor: str
    options: tuple[str, str]
    phoneme: str
    target_ipa: str

    def public(self) -> dict:
        """Expose choices only; excludes answer and target audio text."""
        return {"number": self.number, "pair_key": self.pair_key,
                "options": list(self.options)}


def load_pairs(path: str | Path) -> list[Pair]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) < 4:
        raise ValueError("Prévoir au moins quatre paires distinctes")
    pairs = []
    for row in rows:
        obj = Pair(**row)
        if not all((obj.key, obj.word_y, obj.word_u, obj.ipa_y, obj.ipa_u)):
            raise ValueError("Paire incomplète")
        if obj.word_y.casefold() == obj.word_u.casefold():
            raise ValueError("Les deux mots doivent être différents")
        pairs.append(obj)
    if len(set(p.key for p in pairs)) != len(pairs):
        raise ValueError("Identifiants de paires dupliqués")
    return pairs


def build_quiz(pairs: list[Pair], count: int = 10, seed: int = 42) -> list[Question]:
    if not 2 <= count <= MAX_ITEMS:
        raise ValueError(f"Le nombre de questions doit être entre 2 et {MAX_ITEMS}")
    if len(pairs) < 4:
        raise ValueError("Au moins quatre paires nécessaires")
    rng = random.Random(seed)
    shuffled = pairs.copy()
    rng.shuffle(shuffled)
    # Maintain an equal /y/–/u/ exposure even for odd lengths (±1).
    targets = ["y", "u"] * ((count + 1) // 2)
    targets = targets[:count]
    rng.shuffle(targets)
    quiz = []
    for i, phoneme in enumerate(targets):
        pair = shuffled[i % len(shuffled)]
        target = pair.word(phoneme)
        distractor = pair.word("u" if phoneme == "y" else "y")
        opts = [target, distractor]
        rng.shuffle(opts)
        quiz.append(Question(i + 1, pair.key, target, target, distractor,
                             (opts[0], opts[1]), phoneme, pair.ipa(phoneme)))
    return quiz


def evaluate(questions: Iterable[Question], choices: Iterable[str | None]) -> dict:
    questions = list(questions)
    choices = list(choices)
    if len(choices) != len(questions):
        raise ValueError("Réponses et questions : tailles incohérentes")
    per_sound = {s: {"correct": 0, "total": 0, "confused_as_other": 0} for s in SOUND_LABELS}
    records = []
    for item, answer in zip(questions, choices):
        if answer not in item.options and answer is not None:
            raise ValueError(f"Choix invalide à la question {item.number}")
        correct = answer == item.answer
        scored = answer is not None
        if scored:
            per_sound[item.phoneme]["total"] += 1
            per_sound[item.phoneme]["correct"] += int(correct)
            per_sound[item.phoneme]["confused_as_other"] += int(not correct)
        records.append({"question": item.number, "pair": item.pair_key,
                        "target_phoneme": item.phoneme, "target": item.target,
                        "selected": answer, "correct": correct if scored else None})
    answered = sum(row["total"] for row in per_sound.values())
    total_correct = sum(row["correct"] for row in per_sound.values())
    accuracy = round(total_correct / answered * 100, 1) if answered else None
    if accuracy is None:
        level = "not_scored"
    elif accuracy >= 80:
        level = "consolidation"
    elif accuracy >= 60:
        level = "progressing"
    else:
        level = "support"
    weak = sorted(SOUND_LABELS, key=lambda s: (
        per_sound[s]["correct"] / per_sound[s]["total"] if per_sound[s]["total"] else 1,
        s))
    weak = [s for s in weak if per_sound[s]["total"] and
            per_sound[s]["correct"] < per_sound[s]["total"]]
    return {"answered": answered, "total": len(questions), "correct": total_correct,
            "accuracy_percent": accuracy, "level": level,
            "per_sound": per_sound, "focus_phonemes": weak,
            "recommendations": recommendations(per_sound, level),
            "responses": records}


def recommendations(per_sound: dict, level: str) -> list[str]:
    guidance = []
    if per_sound["y"]["confused_as_other"]:
        guidance.append("/y/ : dire « i » en gardant la langue vers l'avant, puis arrondir les lèvres comme pour « ou » ; comparer tu/tout.")
    if per_sound["u"]["confused_as_other"]:
        guidance.append("/u/ : arrondir les lèvres et reculer la langue ; comparer rue/roue et vu/vous.")
    if level == "support":
        guidance.append("Refaire quatre oppositions à vitesse lente avec l'enseignant, puis à vitesse normale.")
    elif level == "progressing":
        guidance.append("Alterner discrimination, répétition guidée et reprise de deux paires difficiles.")
    elif level == "consolidation":
        guidance.append("Passer à des phrases courtes et à l'observation orale par l'enseignant.")
    else:
        guidance.append("Effectuer le diagnostic avant d'interpréter une progression.")
    return guidance


def teacher_observation(criteria: dict[str, int]) -> dict:
    """Human ratings: 0=not yet, 1=with help, 2=autonomous, no acoustic inference."""
    needed = {"mouth_position", "word_repetition", "short_phrase"}
    if set(criteria) != needed or any(not isinstance(v, int) or isinstance(v, bool) or v not in (0, 1, 2) for v in criteria.values()):
        raise ValueError("Observation enseignante : trois critères, notes 0–2")
    return {"criteria": criteria, "points": sum(criteria.values()), "maximum": 6,
            "assessed_by": "teacher", "automatic_pronunciation_score": False}


DEFAULT_PAIRS = Path(__file__).resolve().parents[2] / "data" / "minimal_pairs.json"
