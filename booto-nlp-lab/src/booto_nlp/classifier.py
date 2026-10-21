"""Classification supervisée avec séparation train/test et pipeline anti-fuite."""
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from .features import make_vectorizer

@dataclass
class ClassificationResult:
    model: Pipeline
    metrics: dict
    test_size: int


def train_classifier(df: pd.DataFrame, seed: int = 42) -> ClassificationResult:
    if not {"text", "category"}.issubset(df.columns):
        raise ValueError("Entraînement : colonnes 'text' et 'category' obligatoires.")
    usable = df[df["text"].astype(str).str.strip().ne("") & df["category"].astype(str).str.strip().ne("")].copy()
    if usable["category"].nunique() < 2 or usable["category"].value_counts().min() < 3:
        raise ValueError("Au moins deux catégories et trois exemples par catégorie sont nécessaires.")
    # Stratifier par (langue, catégorie) si chaque combinaison a au moins deux exemples.
    strata = usable["category"].astype(str)
    if "language" in usable:
        pairs = usable["language"].astype(str) + "/" + strata
        if pairs.value_counts().min() >= 2:
            strata = pairs
    X_train, X_test, y_train, y_test = train_test_split(
        usable["text"].tolist(), usable["category"].tolist(),
        test_size=0.2, random_state=seed, stratify=strata,
    )
    pipeline = Pipeline([
        ("tfidf", make_vectorizer()),
        ("classifier", LogisticRegression(max_iter=2000, random_state=seed)),
    ])
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    labels = sorted(usable["category"].unique().tolist())
    return ClassificationResult(model=pipeline, test_size=len(X_test), metrics={
        "accuracy": float(accuracy_score(y_test, predictions)),
        "macro_f1": float(f1_score(y_test, predictions, average="macro", zero_division=0)),
        "labels": labels,
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=labels).tolist(),
        "report": classification_report(y_test, predictions, labels=labels, zero_division=0, output_dict=True),
    })
