"""Local-only tabular import. Never calls remote endpoints."""
from io import BytesIO, StringIO
import csv
from zipfile import ZipFile
import numpy as np
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
    numeric = frame.select_dtypes(include='number')
    if np.isinf(numeric.to_numpy(dtype=float)).any():
        raise DataError('Des valeurs numériques infinies sont présentes. Corrigez-les avant analyse.')
    return frame

def read_upload(raw: bytes, filename: str) -> pd.DataFrame:
    if not raw or len(raw) > MAX_BYTES:
        raise DataError('Fichier vide ou dépassant 5 Mo.')
    ext = Path(filename).suffix.lower()
    try:
        if ext == '.csv':
            text = raw.decode('utf-8-sig')
            try:
                delimiter = csv.Sniffer().sniff(text[:8192], delimiters=',;\t|').delimiter
            except csv.Error:
                delimiter = ','
            header = next(csv.reader(StringIO(text), delimiter=delimiter))
            names = [name.strip() for name in header]
            if not all(names) or len(names) != len(set(names)):
                raise DataError('Les en-têtes CSV doivent être renseignés et uniques.')
            data = pd.read_csv(StringIO(text), sep=delimiter, low_memory=False)
        elif ext == '.xlsx':
            # XLSX is compressed: cap decompressed size before openpyxl allocates it.
            with ZipFile(BytesIO(raw)) as archive:
                if sum(item.file_size for item in archive.infolist()) > 40 * 1024 * 1024:
                    raise DataError('Le classeur décompressé dépasse la limite de 40 Mo.')
            data = pd.read_excel(BytesIO(raw), engine='openpyxl')
        else:
            raise DataError('Formats acceptés : CSV UTF-8 et XLSX.')
        return validate_frame(data)
    except DataError:
        raise
    except Exception as exc:
        raise DataError('Lecture impossible : vérifiez le format, l’encodage UTF-8 et le contenu du fichier.') from exc
