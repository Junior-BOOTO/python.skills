"""Similarité lexicale TF-IDF (pas de compréhension sémantique multilingue)."""
from __future__ import annotations
from sklearn.metrics.pairwise import cosine_similarity
from .features import make_vectorizer


def nearest_documents(texts: list[str], document_index: int, k: int = 3) -> list[tuple[int, float]]:
    if not (0 <= document_index < len(texts)):
        raise IndexError("Index de document invalide.")
    if len(texts) <= 1 or not any(t.strip() for t in texts):
        return []
    vectorizer = make_vectorizer()
    matrix = vectorizer.fit_transform(texts)
    sim = cosine_similarity(matrix[document_index], matrix).ravel()
    scored = [(i, round(float(score), 6)) for i, score in enumerate(sim) if i != document_index]
    return sorted(scored, key=lambda row: (-row[1], row[0]))[:max(0, k)]
