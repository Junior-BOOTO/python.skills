"""Local-only tabular import. Never calls remote endpoints."""
from io import BytesIO
from pathlib import Path
import pandas as pd

MAX_BYTES = 5 * 1024 * 1024
MAX_ROWS = 30000
MAX_COLS = 80

class DataError(ValueError):
    """Recoverable user-facing data validation error."""

def validate_frame(frame: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        raise DataError('Fichier vide ou sans observations utilisables.')
    if frame.shape[0] > MAX_ROWS or frame.shape[1] > MAX_COLS:
        raise DataError(f'Limite V1 : {MAX_ROWS} lignes et {MAX_COLS} colonnes.')
    if frame.columns.isna().any() or any(str(c).strip()=='' for c in frame.columns):
        raise DataError('Les noms de colonnes doivent être renseignés.')
    frame = frame.copy()
    frame.columns = [str(c).strip() for c in frame.columns]
    if len(frame.columns) != len(set(frame.columns)):
        raise DataError('Des colonnes portent le même nom.')
    return frame

def read_upload(raw: bytes, filename: str) -> pd.DataFrame:
    if not raw or len(raw) > MAX_BYTES:
        raise DataError('Fichier vide ou dépassant 5 Mo.')
    ext = Path(filename).suffix.lower()
    try:
        if ext == '.csv':
            data = pd.read_csv(BytesIO(raw), encoding='utf-8-sig', low_memory=False)
        elif ext == '.xlsx':
            data = pd.read_excel(BytesIO(raw), engine='openpyxl')
        else:
            raise DataError('Formats acceptés : CSV UTF-8 et XLSX.')
        return validate_frame(data)
    except DataError:
        raise
    except Exception as exc:
        raise DataError('Lecture impossible : vérifiez le format, l’encodage UTF-8 et le contenu du fichier.') from exc
