"""Lecture et validation de corpus CSV UTF-8."""
from __future__ import annotations
import io
import pandas as pd

REQUIRED = "text"


def load_csv(source: str | io.BytesIO) -> pd.DataFrame:
    """Charge un CSV. Les erreurs sont répercutées avec un message explicite."""
    try:
        df = pd.read_csv(source, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    except (UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise ValueError("Le CSV doit être lisible et encodé en UTF-8.") from exc
    return validate_corpus(df)


def validate_corpus(df: pd.DataFrame) -> pd.DataFrame:
    """Exige une colonne text ; marque les textes vides, sans les supprimer."""
    if REQUIRED not in df.columns:
        raise ValueError("La colonne obligatoire 'text' est absente du fichier.")
    if df.empty:
        raise ValueError("Le fichier ne contient aucun document.")
    result = df.copy()
    result["text"] = result["text"].fillna("").astype(str)
    if "document_id" not in result:
        result.insert(0, "document_id", [str(i) for i in range(1, len(result) + 1)])
    else:
        result["document_id"] = result["document_id"].astype(str)
    result["processing_status"] = result["text"].map(lambda x: "ok" if x.strip() else "empty_text")
    return result
