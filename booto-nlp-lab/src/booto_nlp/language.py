"""Détection multilingue : langid si disponible, méthode simplifiée sinon.

IMPORTANT : la méthode simplifiée est un secours pédagogique, pas un modèle validé.
"""
from __future__ import annotations
from .preprocess import tokenize

MARKERS = {
  "fr": {"les", "des", "dans", "une", "avec", "nous", "pour", "sur", "qui", "est", "élèves", "français", "apprentissage", "école", "sont", "leur", "leurs", "des"},
  "en": {"the", "and", "with", "from", "students", "software", "are", "is", "school", "learning", "environment", "technology", "this", "for", "will", "their", "these"},
  "es": {"los", "las", "del", "con", "para", "estudiantes", "escuela", "aprendizaje", "medio", "ambiente", "tecnología", "son", "una", "que", "estas", "este"},
}


def detect_language(text: str) -> tuple[str, str]:
    """Renvoie (code ISO ou 'unknown', méthode)."""
    if len(tokenize(text, remove_stopwords=False)) < 4:
        return "unknown", "too_short"
    try:
        import langid
    except ImportError:
        tokens = tokenize(text, remove_stopwords=False)
        scores = {lang: sum(t in markers for t in tokens) for lang, markers in MARKERS.items()}
        best = max(scores, key=scores.get)
        winners = [k for k, v in scores.items() if v == scores[best]]
        return (best if scores[best] >= 2 and len(winners) == 1 else "unknown"), "heuristic_demo"
    language, _score = langid.classify(text)
    return (language if language in ("fr", "en", "es") else "unknown"), "langid"
