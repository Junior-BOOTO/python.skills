"""Interface expérimentale Streamlit de BOOTO NLP LAB."""
from __future__ import annotations
import sys
from pathlib import Path
import io
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
import plotly.express as px
import streamlit as st
from booto_nlp.ingest import load_csv
from booto_nlp.classifier import train_classifier
from booto_nlp.pipeline import analyze_documents
from booto_nlp.features import top_keywords
from booto_nlp.similarity import nearest_documents

st.set_page_config(page_title="BOOTO NLP LAB", page_icon="🧠", layout="wide")
st.title("BOOTO NLP LAB — Multilingual Text Analyzer")
st.caption("Prototype expérimental FR · EN · ES | Données synthétiques d'entraînement ; aucune validation externe réalisée")
st.warning("Les prédictions sont expérimentales. N'interprétez pas leurs scores comme une précision garantie sur des données réelles.")

@st.cache_resource
def example_model():
    path = ROOT / "data" / "sample" / "corpus_300_demo.csv"
    training = load_csv(str(path))
    return train_classifier(training)

try:
    trained = example_model()
except Exception as exc:
    st.error(f"Modèle de démonstration indisponible : {exc}")
    st.stop()

st.sidebar.markdown("### Corpus")
uploaded = st.sidebar.file_uploader("Importer un CSV (UTF-8, colonne text)", type=["csv"])
if uploaded is None:
    st.info("Aucun fichier chargé. Démonstration avec 300 textes synthétiques.")
    corpus = load_csv(str(ROOT / "data" / "sample" / "corpus_300_demo.csv"))
else:
    if uploaded.size > 5 * 1024 * 1024:
        st.error("Fichier trop volumineux : limite 5 Mo.")
        st.stop()
    try:
        corpus = load_csv(io.BytesIO(uploaded.getvalue()))
    except (ValueError, UnicodeDecodeError) as exc:
        st.error(str(exc))
        st.stop()

results = analyze_documents(corpus, trained)
col1, col2, col3 = st.columns(3)
col1.metric("Documents", len(results))
col2.metric("Textes analysables", int((results.processing_status == "ok").sum()))
col3.metric("Documents signalés", int((results.processing_status != "ok").sum()))

valid = results[results.processing_status == "ok"].copy()
st.subheader("Données et résultats")
st.dataframe(results, use_container_width=True, hide_index=True)
if not valid.empty:
    lang_tab, cat_tab, keywords_tab, similar_tab = st.tabs(["Langues", "Thèmes", "Mots-clés", "Similarité"])
    with lang_tab:
        freq = valid.predicted_language.value_counts().rename_axis("Langue").reset_index(name="Documents")
        st.plotly_chart(px.bar(freq, x="Langue", y="Documents", title="Langue détectée"), use_container_width=True)
        if (valid.language_method == "heuristic_demo").any():
            st.warning("Détection par heuristique de secours : installer 'langid' pour utiliser le classifieur prévu.")
    with cat_tab:
        freq = valid.predicted_category.value_counts().rename_axis("Catégorie").reset_index(name="Documents")
        st.plotly_chart(px.bar(freq, x="Catégorie", y="Documents", title="Catégories prédites"), use_container_width=True)
    with keywords_tab:
        language = st.selectbox("Langue", ["Toutes"] + sorted(valid.predicted_language.unique().tolist()))
        subset = valid if language == "Toutes" else valid[valid.predicted_language == language]
        keys = top_keywords(subset.text.tolist(), n=10)
        st.dataframe(pd.DataFrame(keys, columns=["Terme", "Score TF-IDF moyen"]), hide_index=True)
    with similar_tab:
        idx = st.number_input("Index d'un texte analysable (à partir de 0)", min_value=0, max_value=len(valid) - 1, step=1)
        matches = nearest_documents(valid.text.tolist(), int(idx), k=3)
        st.dataframe(pd.DataFrame([{"index": i, "similarité": score, "texte": valid.iloc[i].text} for i, score in matches]), hide_index=True)

st.download_button("Exporter les résultats CSV", data=results.to_csv(index=False).encode("utf-8-sig"),
                   file_name="booto_nlp_resultats.csv", mime="text/csv")
with st.expander("Évaluation interne sur corpus synthétique — non généralisable"):
    st.json({"accuracy": trained.metrics["accuracy"], "macro_f1": trained.metrics["macro_f1"],
             "taille_jeu_test": trained.test_size, "matrice_confusion": trained.metrics["confusion_matrix"]})
