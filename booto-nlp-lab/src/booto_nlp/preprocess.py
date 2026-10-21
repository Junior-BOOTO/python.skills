"""Prétraitement simple, conservant les accents et le texte original."""
from __future__ import annotations
import re
import unicodedata

PATTERN = re.compile(r"[^\W\d_]+", re.UNICODE)

STOP_WORDS = {
    "fr": {"le", "la", "les", "un", "une", "des", "de", "du", "et", "est", "dans", "pour", "sur", "avec", "que", "qui", "nous", "au", "aux", "à", "en"},
    "en": {"the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "is", "are", "we", "our", "that", "this"},
    "es": {"el", "la", "los", "las", "un", "una", "de", "del", "y", "en", "con", "para", "que", "es", "son", "por", "al", "se", "una"},
}


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", str(text)).strip().split())


def tokenize(text: str, language: str | None = None, remove_stopwords: bool = True) -> list[str]:
    terms = PATTERN.findall(normalize(text).lower())
    if remove_stopwords:
        stop = STOP_WORDS.get(language or "", set())
        terms = [t for t in terms if t not in stop]
    return terms
