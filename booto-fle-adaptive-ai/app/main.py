"""Interface Streamlit : quiz A1 + recommandations explicables + profils fictifs."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import streamlit as st
import pandas as pd
from booto_fle.engine import (STATUSES, SKILLS, LABELS, evaluate, group_summary,
                              load_question_bank, load_synthetic_profiles, recommend)

st.set_page_config(page_title="BOOTO FLE Adaptive AI", page_icon="📚", layout="wide")
st.title("📚 BOOTO FLE Adaptive AI — Prototype A1")
st.caption("Grade 4 • Ma journée typique • PYP « Qui nous sommes » • Français langue étrangère")
st.info("Démonstration pédagogique : moteur à règles, pas de machine learning ni diagnostic CECRL certifié. Les profils du tableau enseignant sont fictifs. N'utilisez aucune donnée personnelle réelle.")

bank = load_question_bank()
view = st.sidebar.radio("Espace", ["Apprenant — évaluation formative", "Enseignant — classe fictive", "Méthode et limites"])

if view.startswith("Apprenant"):
    st.subheader("Évaluation formative : ma routine quotidienne")
    st.write("12 questions réparties en quatre compétences. Laissez une question sans réponse si vous ne savez pas ; elle ne sera pas interprétée comme une erreur d'apprentissage.")
    with st.form("quiz"):
        answers = {}
        for ix, q in enumerate(bank["items"], start=1):
            st.markdown(f"**{ix}. {q['question']}**")
            selected = st.radio(f"Réponse à la question {ix}", options=list(range(3)),
                                format_func=lambda i, opt=q["options"]: opt[i],
                                key=f"answer_{q['id']}", index=None,
                                label_visibility="collapsed")
            answers[q["id"]] = selected
        oral = st.selectbox("Observation orale de l'enseignant (facultative)",
                            options=[None, 0, 1, 2],
                            format_func=lambda x: "Non évaluée" if x is None else f"{x}/2",
                            help="0 : critère non démontré ; 1 : partiellement démontré ; 2 : démontré. Cette observation est humaine.")
        submitted = st.form_submit_button("Voir mon diagnostic et mes exercices", type="primary")
    if submitted:
        diagnostic = evaluate(answers, oral_score=oral, bank=bank)
        st.success(f"Questionnaire analysé : {diagnostic.answered}/{diagnostic.total} réponses fournies.")
        st.subheader("Indicateurs « Je peux… »")
        cols = st.columns(2)
        for ix, score in enumerate(diagnostic.results):
            with cols[ix % 2]:
                st.markdown(f"**{score.label} : {STATUSES[score.status]}**")
                st.caption(score.rationale)
        st.subheader("Parcours personnalisé proposé")
        recs = recommend(diagnostic)
        if not recs:
            st.write("Aucune difficulté suffisamment documentée : poursuivre avec des activités d'enrichissement, ou compléter les compétences non évaluées.")
        for pos, rec in enumerate(recs, 1):
            with st.expander(f"{pos}. {rec['titre']} — {rec['minutes']} min", expanded=pos==1):
                st.write("**Pourquoi ?**", rec["motif"])
                st.write("**Consigne :**", rec["consigne"])
                st.write("**Critère de réussite :**", rec["reussite"])
                st.write("**Aide :**", rec["accompagnement"])
                st.write("**Pour aller plus loin :**", rec["approfondissement"])
        with st.expander("Corrigé détaillé et explications"):
            for entry in diagnostic.corrections:
                if entry["correct"] is None:
                    icon, desc = "⚪", "Non répondu"
                elif entry["correct"]:
                    icon, desc = "✅", "Correct"
                else:
                    icon, desc = "🔎", "À revoir"
                st.markdown(f"{icon} **{entry['id']} — {desc}** : {entry['correct_answer']}. {entry['feedback']}")
elif view.startswith("Enseignant"):
    st.subheader("Suivi pédagogique — profils synthétiques uniquement")
    summary = group_summary()
    st.warning(summary["notice"])
    st.metric("Profils fictifs", summary["n_profiles"])
    data = []
    for skill in SKILLS:
        counts = summary["status_totals"][skill]
        data.append({"Compétence": LABELS[skill], "Acquis": counts["mastered"],
                     "En cours": counts["developing"], "À renforcer": counts["priority"],
                     "Non évalué": counts["unassessed"]})
    st.dataframe(data, use_container_width=True, hide_index=True)
    st.bar_chart(pd.DataFrame(data).set_index("Compétence")[["À renforcer"]])
    profiles = load_synthetic_profiles()
    selected = st.selectbox("Explorer un profil entièrement fictif", [p["student_id"] for p in profiles])
    detail = next(d for d in summary["details"] if d["student_id"] == selected)
    st.markdown("**Diagnostic explicable**")
    for score in detail["diagnostic"]["skills"]:
        st.write(f"• {score['label']} — {score['status_label']} : {score['rationale']}")
    st.markdown("**Activités recommandées**")
    for rec in detail["recommendations"]:
        st.write(f"• {rec['titre']} ({rec['minutes']} min) — {rec['motif']}")
else:
    st.subheader("Règles d'analyse et précautions")
    st.markdown("""
**Nature du projet.** Prototype de différenciation pédagogique fondé sur des règles lisibles.
Aucun LLM, reconnaissance vocale ou apprentissage automatique ne décide du parcours.

**Règles de diagnostic.** Chaque compétence écrite comporte trois questions. Quand les trois
sont renseignées : 2 ou 3 bonnes réponses = *acquis sur ces tâches* ; 1 = *en cours* ;
0 = *à renforcer*. Si une question manque : *non évalué*, faute de preuves suffisantes.

**Expression orale.** Seul l'enseignant peut saisir 0, 1 ou 2 selon son observation.
Sans observation, la production orale reste *non évaluée*.

**Adaptation.** Les exercices sont choisis par priorité (à renforcer, puis en cours),
par compétence, dans un catalogue transparent. Le lien entre chaque recommandation et
les réponses observées est toujours indiqué.

**Limites.** Les 12 questions sont textuelles : l'association images/actions et la validation
d'une vraie production orale ne sont pas encore implémentées. La compétence CECRL et
les apprentissages réels ne sont ni certifiés ni mesurés longitudinalement.
Les profils enseignant sont construits artificiellement. Ne pas saisir de noms d'élèves
ou de données personnelles dans cette démonstration.
""")
    st.caption("Auteur : Junior BOOTO Waba • Projet expérimental de portfolio FLE + Python/Data Science")
