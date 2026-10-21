from pathlib import Path
import pandas as pd
from booto_nlp.ingest import load_csv
from booto_nlp.classifier import train_classifier
from booto_nlp.pipeline import analyze_documents

ROOT = Path(__file__).resolve().parents[1]

def test_corpus_shape():
    df = load_csv(str(ROOT / 'data/sample/corpus_300_demo.csv'))
    assert len(df) == 300
    assert df.groupby('language').size().to_dict() == {'en': 100, 'es': 100, 'fr': 100}
    assert df.category.nunique() == 3

def test_train_and_predict():
    df = load_csv(str(ROOT / 'data/sample/corpus_300_demo.csv'))
    result = train_classifier(df)
    assert result.test_size == 60
    assert 0 <= result.metrics['macro_f1'] <= 1
    out = analyze_documents(pd.DataFrame({'document_id':['A','B'], 'text': ['The students read a new textbook in school.','']}), result)
    assert out.document_id.tolist() == ['A','B']
    assert out.processing_status.tolist() == ['ok','empty_text']
    assert out.predicted_category.iloc[0] in {'education','technology','environment'}
    assert out.predicted_category.iloc[1] == ''
