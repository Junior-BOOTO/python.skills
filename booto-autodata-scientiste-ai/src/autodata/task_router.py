"""Task hints are advisory; the user must approve task and target."""
import pandas as pd
from .ingestion import DataError

def suggest_task(target: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(target):
        return 'classification' if target.nunique(dropna=True) <= 8 else 'regression'
    return 'classification'

def validate_task(frame: pd.DataFrame, target: str, task: str, exclusions: list[str]):
    if task not in {'classification', 'regression'}:
        raise DataError('Sélectionnez classification ou régression.')
    if target not in frame.columns:
        raise DataError('La colonne cible est absente.')
    if target in exclusions:
        raise DataError('La cible ne peut pas être exclue.')
    if frame[target].isna().any():
        raise DataError('La cible contient des valeurs manquantes. Corrigez-la dans le fichier source.')
    cols = [c for c in frame.columns if c != target and c not in exclusions]
    if not cols:
        raise DataError('Aucune variable explicative ne reste après exclusions.')
    if any(frame[c].isna().all() for c in cols):
        raise DataError('Supprimez explicitement les colonnes entièrement vides via les exclusions.')
    if task == 'regression':
        if not pd.api.types.is_numeric_dtype(frame[target]) or frame[target].nunique() < 5:
            raise DataError('Régression : cible numérique avec au moins 5 valeurs distinctes requise.')
    else:
        if frame[target].nunique() < 2 or frame[target].nunique() > 20:
            raise DataError('Classification : entre 2 et 20 classes distinctes.')
        counts = frame[target].value_counts()
        if (counts < 4).any():
            raise DataError('Chaque classe doit comprendre au moins 4 observations pour la validation.')
    if len(frame) < 24:
        raise DataError('Le projet V1 requiert au moins 24 observations.')
    for c in cols:
        if pd.api.types.is_datetime64_any_dtype(frame[c]):
            raise DataError(f'Date détectée ({c}) : transformez-la en variables explicatives avant entraînement.')
        if frame[c].dtype == 'object':
            # Avoid costly / dubious free-text one-hot encoding.
            avg_len = frame[c].dropna().astype(str).str.len().mean()
            if pd.notna(avg_len) and avg_len > 100:
                raise DataError(f'Colonne de texte libre ({c}) : excluez-la ou préparez-la hors du module tabulaire.')
            if frame[c].nunique(dropna=True) > 80:
                raise DataError(f'Colonne à forte cardinalité ({c}) : excluez-la ou réduisez ses modalités.')
    return cols
