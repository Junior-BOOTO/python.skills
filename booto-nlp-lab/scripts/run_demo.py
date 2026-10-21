"""Démo en console du pipeline principal, sans interface Streamlit."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from booto_nlp.ingest import load_csv
from booto_nlp.classifier import train_classifier
from booto_nlp.pipeline import analyze_documents
from booto_nlp.features import top_keywords

if __name__ == "__main__":
    corpus = load_csv(str(ROOT / "data" / "sample" / "corpus_300_demo.csv"))
    model = train_classifier(corpus)
    result = analyze_documents(corpus.head(5), model)
    print("Démonstration sur données SYNTHÉTIQUES — résultats non validés sur données réelles")
    print("Corpus :", len(corpus), "documents")
    print("5 premières prédictions :")
    print(result[["document_id", "predicted_language", "predicted_category"]].to_string(index=False))
    print("Mots-clés :", top_keywords(corpus.text.tolist(), n=5))
    print("Macro-F1 (synthétique, non généralisable) :", round(model.metrics["macro_f1"], 3))
