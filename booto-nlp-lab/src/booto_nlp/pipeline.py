"""Analyse des textes et association des résultats aux identifiants."""
from __future__ import annotations
import pandas as pd
from .ingest import validate_corpus
from .language import detect_language
from .classifier import ClassificationResult


def analyze_documents(df: pd.DataFrame, classifier: ClassificationResult) -> pd.DataFrame:
    result = validate_corpus(df)
    result["predicted_language"] = "unknown"
    result["language_method"] = ""
    result["predicted_category"] = ""
    for idx in result.index:
        if result.at[idx, "processing_status"] != "ok":
            continue
        lang, method = detect_language(result.at[idx, "text"])
        result.at[idx, "predicted_language"] = lang
        result.at[idx, "language_method"] = method
    indices = result.index[result["processing_status"].eq("ok")]
    if len(indices):
        result.loc[indices, "predicted_category"] = classifier.model.predict(result.loc[indices, "text"].tolist())
    return result
