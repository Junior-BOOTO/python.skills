"""Moteur de diagnostic formatif à règles explicites, sans données personnelles.

Ce moteur ne constitue pas un modèle ML ni une mesure certifiée du CECRL.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ("lexique", "verbes", "connecteurs", "heures", "oral")
LABELS = {
    "lexique": "Vocabulaire de la routine",
    "verbes": "Verbes pronominaux avec je",
    "connecteurs": "Organisation temporelle",
    "heures": "Indiquer une heure (à / vers)",
    "oral": "Production orale (observation humaine)",
}
STATUSES = {"mastered": "Acquis (sur ces tâches)", "developing": "En cours", "priority": "À renforcer", "unassessed": "Non évalué"}


def load_question_bank(path: str | Path | None = None) -> dict:
    """Charge et valide un questionnaire original du projet."""
    target = Path(path) if path else ROOT / "data/quiz_routine_a1.json"
    bank = json.loads(target.read_text(encoding="utf-8"))
    items = bank.get("items", [])
    if not items:
        raise ValueError("Le questionnaire ne contient aucune question.")
    ids = [q.get("id") for q in items]
    if len(ids) != len(set(ids)):
        raise ValueError("Identifiants de questions dupliqués.")
    for q in items:
        if not all(field in q for field in ("id", "question", "options", "answer_index", "competence", "feedback")):
            raise ValueError("Question incomplète.")
        if q["competence"] not in SKILLS[:-1]:
            raise ValueError(f"Compétence inconnue : {q['competence']}")
        if len(q["options"]) != 3 or q["answer_index"] not in (0, 1, 2):
            raise ValueError("Chaque question doit avoir trois options et une bonne réponse valide.")
        if len(set(q["options"])) != 3:
            raise ValueError("Les trois options doivent être distinctes.")
    counts = {skill: sum(q["competence"] == skill for q in items) for skill in SKILLS[:-1]}
    if any(value != 3 for value in counts.values()):
        raise ValueError("Chaque compétence écrite doit comporter trois questions pour les règles V1.")
    return bank


def load_activities(path: str | Path | None = None) -> dict:
    target = Path(path) if path else ROOT / "data/activities_a1.json"
    items = json.loads(target.read_text(encoding="utf-8"))
    if set(items) != set(SKILLS):
        raise ValueError("Une activité par compétence est obligatoire.")
    for skill, activity in items.items():
        if not {"id", "titre", "minutes", "consigne", "reussite", "accompagnement", "approfondissement"}.issubset(activity):
            raise ValueError(f"Activité incomplète : {skill}")
        if not isinstance(activity["minutes"], int) or activity["minutes"] < 1:
            raise ValueError("La durée doit être un entier positif.")
    return items


@dataclass(frozen=True)
class SkillResult:
    skill: str
    label: str
    correct: int | None
    answered: int
    total: int
    status: str
    rationale: str

    def as_dict(self) -> dict:
        d = asdict(self)
        d["status_label"] = STATUSES[self.status]
        return d


@dataclass(frozen=True)
class Diagnostic:
    results: tuple[SkillResult, ...]
    corrections: tuple[dict, ...]
    answered: int
    total: int

    def as_dict(self) -> dict:
        return {"skills": [r.as_dict() for r in self.results],
                "corrections": list(self.corrections),
                "answered": self.answered, "total": self.total}


def _status_for_count(correct: int, total: int) -> str:
    if correct >= 2 and total == 3:
        return "mastered"
    if correct == 1:
        return "developing"
    return "priority"


def evaluate(answers: dict[str, int | None], oral_score: int | None = None,
             bank: dict | None = None) -> Diagnostic:
    """Calcule un diagnostic explicable et évite toute conclusion en cas de réponses incomplètes.

    oral_score: None = pas d'observation ; 0 = non démontré, 1 = partiel, 2 = démontré.
    """
    bank = bank or load_question_bank()
    questions = bank["items"]
    valid_ids = {q["id"] for q in questions}
    unknown_ids = set(answers) - valid_ids
    if unknown_ids:
        raise ValueError(f"Identifiants de réponses inconnus : {sorted(unknown_ids)}")
    if oral_score not in (None, 0, 1, 2):
        raise ValueError("La note d'observation orale doit être vide, 0, 1 ou 2.")
    for key, choice in answers.items():
        if choice is not None and (type(choice) is not int or choice not in (0, 1, 2)):
            raise ValueError(f"Choix invalide pour la question {key}.")
    corrections = []
    for q in questions:
        choice = answers.get(q["id"])
        corrections.append({
            "id": q["id"], "competence": q["competence"], "question": q["question"],
            "answered": choice is not None,
            "correct": None if choice is None else choice == q["answer_index"],
            "answer": None if choice is None else q["options"][choice],
            "correct_answer": q["options"][q["answer_index"]], "feedback": q["feedback"],
        })
    results = []
    for skill in SKILLS[:-1]:
        selected = [c for c in corrections if c["competence"] == skill]
        total, answered = len(selected), sum(c["answered"] for c in selected)
        correct = sum(c["correct"] is True for c in selected)
        if answered != total:
            status = "unassessed"
            rationale = f"{answered}/{total} réponses : preuves insuffisantes pour attribuer un niveau."
        else:
            status = _status_for_count(correct, total)
            rationale = f"{correct}/{total} réponses correctes aux questions de {LABELS[skill].lower()}."
        results.append(SkillResult(skill, LABELS[skill], correct if answered == total else None, answered, total, status, rationale))
    if oral_score is None:
        oral_status, oral_rationale = "unassessed", "Aucune observation orale saisie par l’enseignant."
    else:
        oral_status = ("priority", "developing", "mastered")[oral_score]
        oral_rationale = f"Observation humaine : {oral_score}/2. Cette note ne résulte pas d’une analyse vocale automatique."
    results.append(SkillResult("oral", LABELS["oral"], oral_score, int(oral_score is not None), 1,
                               oral_status, oral_rationale))
    return Diagnostic(tuple(results), tuple(corrections), sum(c["answered"] for c in corrections), len(corrections))


def recommend(diagnostic: Diagnostic, max_activities: int = 3, activities: dict | None = None) -> list[dict]:
    """Ordonne les activités selon les difficultés observées ; pas de profilage caché."""
    if max_activities < 0:
        raise ValueError("max_activities doit être positif ou nul.")
    if max_activities == 0:
        return []
    activities = activities or load_activities()
    order = {"priority": 0, "developing": 1, "mastered": 2, "unassessed": 3}
    ranked = sorted(enumerate(diagnostic.results), key=lambda entry: (order[entry[1].status], entry[0]))
    proposed = []
    for _, score in ranked:
        if score.status not in ("priority", "developing"):
            continue
        activity = activities[score.skill]
        proposed.append({"competence": score.skill, "competence_label": score.label,
                         "statut": STATUSES[score.status], "motif": score.rationale, **activity})
        if len(proposed) >= max_activities:
            break
    return proposed


def load_synthetic_profiles(path: str | Path | None = None) -> list[dict]:
    target = Path(path) if path else ROOT / "data/profils_synthetiques.json"
    container = json.loads(target.read_text(encoding="utf-8"))
    profiles = container["profiles"]
    if len({p["student_id"] for p in profiles}) != len(profiles):
        raise ValueError("Identifiants de profils dupliqués.")
    if any(p.get("type_donnees") != "synthetiques" or not p["student_id"].startswith("SYN-") for p in profiles):
        raise ValueError("Ce tableau de bord n'accepte que les profils synthétiques fournis.")
    return profiles


def group_summary(profiles: list[dict] | None = None) -> dict:
    """Tableau de bord sur données fictives, sans inférence individuelle de niveau CECRL."""
    profiles = profiles if profiles is not None else load_synthetic_profiles()
    totals = {s: {status: 0 for status in STATUSES} for s in SKILLS}
    details = []
    for p in profiles:
        if p.get("type_donnees") != "synthetiques" or not p.get("student_id", "").startswith("SYN-"):
            raise ValueError("Les profils doivent être exclusivement synthétiques.")
        diag = evaluate(p["answers"], p.get("oral_score"))
        for skill in diag.results:
            totals[skill.skill][skill.status] += 1
        details.append({"student_id": p["student_id"],
                        "diagnostic": diag.as_dict(), "recommendations": recommend(diag)})
    return {"notice": "DONNÉES SYNTHÉTIQUES — ne reflètent aucune classe réelle.",
            "n_profiles": len(profiles), "status_totals": totals, "details": details}
