import io
import pandas as pd
import pytest
from booto_nlp.ingest import load_csv, validate_corpus

def test_import():
    df = load_csv(io.BytesIO(b'text,language\n"Bonjour a tous",fr\n"Hello everyone",en\n'))
    assert len(df) == 2 and 'document_id' in df

def test_missing_column():
    with pytest.raises(ValueError, match='text'):
        validate_corpus(pd.DataFrame({'other': ['a']}))

def test_empty_line_is_flagged():
    df = validate_corpus(pd.DataFrame({'text': ['bonjour', '  ']}))
    assert df.processing_status.tolist() == ['ok', 'empty_text']
