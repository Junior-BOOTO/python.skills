"""Read-only tabular profiling."""
import pandas as pd
from .ingestion import validate_frame

def profile(frame: pd.DataFrame) -> dict:
    df = validate_frame(frame)
    return {
        'rows': int(len(df)), 'columns': int(len(df.columns)),
        'duplicates': int(df.duplicated().sum()),
        'missing_cells': int(df.isna().sum().sum()),
        'missing_percent': round(float(df.isna().to_numpy().mean() * 100), 2),
        'all_missing_columns': [str(c) for c in df.columns[df.isna().all()]],
        'column_details': [
            {'colonne': str(c), 'type': str(df[c].dtype),
             'manquants': int(df[c].isna().sum()),
             'manquants_%': round(float(df[c].isna().mean()*100),1),
             'distincts': int(df[c].nunique(dropna=True))}
            for c in df.columns
        ],
    }
