"""Vectorisation et extraction des mots-clés par TF-IDF."""
from __future__ import annotations
from sklearn.feature_extraction.text import TfidfVectorizer
from .preprocess import normalize, tokenize, STOP_WORDS


def make_vectorizer() -> TfidfVectorizer:
    # On conserve les accents et les mots outils ici pour éviter une sélection de stopwords monolingue.
    return TfidfVectorizer(strip_accents=None, lowercase=True, ngram_range=(1, 2),
                           min_df=1, max_features=20000, sublinear_tf=True)


def top_keywords(texts: list[str], n: int = 10) -> list[tuple[str, float]]:
    # Suppression des mots-outils les plus courants des trois langues pour la visualisation.
    ignored = set().union(*STOP_WORDS.values())
    cleaned = [" ".join(t for t in tokenize(text, remove_stopwords=False)
                        if len(t) >= 3 and t not in ignored) for text in texts]
    valid = [text for text in cleaned if text.strip()]
    if not valid:
        return []
    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 1), min_df=1,
                                 max_features=20000, sublinear_tf=True)
    matrix = vectorizer.fit_transform(valid)
    means = matrix.mean(axis=0).A1
    terms = vectorizer.get_feature_names_out()
    indices = sorted(range(len(terms)), key=lambda i: (-means[i], terms[i]))[:n]
    return [(str(terms[i]), round(float(means[i]), 6)) for i in indices]
