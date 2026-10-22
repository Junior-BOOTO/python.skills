"""Streamlit demonstration — no microphone, no automatic pronunciation rating."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import streamlit as st
import streamlit.components.v1 as components
from phonofle import DEFAULT_PAIRS, load_pairs, build_quiz, evaluate, teacher_observation

st.set_page_config(page_title="PhonoFLE AI · /y/ et /u/", page_icon="🎧", layout="wide")

LABELS = {
    "FR": {
        "title": "PhonoFLE AI · Laboratoire d'écoute",
        "subtitle": "Français langue étrangère · A1 · /y/ (« u ») et /u/ (« ou »)",
        "start": "Lancer mon parcours", "restart": "Recommencer",
        "question": "Quel mot entends-tu ?", "listen": "▶ Écouter", "slow": "◌ Lentement",
        "next": "Question suivante", "end": "Voir le bilan", "result": "Bilan de discrimination auditive",
        "target": "Mot entendu", "correct": "Bonne réponse", "wrong": "À retravailler",
        "oral": "Grille orale · remplie par l'enseignant", "download": "Télécharger un bilan anonyme JSON",
    },
    "ES": {
        "title": "PhonoFLE AI · Laboratorio auditivo",
        "subtitle": "Francés como lengua extranjera · A1 · /y/ (« u ») y /u/ (« ou »)",
        "start": "Empezar mi recorrido", "restart": "Repetir",
        "question": "¿Qué palabra escuchas?", "listen": "▶ Escuchar", "slow": "◌ Más lento",
        "next": "Siguiente pregunta", "end": "Ver resultados", "result": "Resultados de discriminación auditiva",
        "target": "Palabra escuchada", "correct": "Respuesta correcta", "wrong": "Practicar de nuevo",
        "oral": "Rúbrica oral · completada por el docente", "download": "Descargar resultados anónimos JSON",
    },
}

@st.cache_data
def available_pairs():
    return load_pairs(DEFAULT_PAIRS)


def reset_quiz():
    st.session_state.quiz = build_quiz(available_pairs(), count=10, seed=42)
    st.session_state.answers = []
    st.session_state.current = 0


def speak_widget(word: str, label: str, slow_label: str):
    # The text is embedded in a browser-side button. No microphone or upload is used.
    safe_word = json.dumps(word, ensure_ascii=False)
    safe_label = json.dumps(label, ensure_ascii=False)
    safe_slow = json.dumps(slow_label, ensure_ascii=False)
    html = f"""<!DOCTYPE html><html lang=\"fr\"><head><meta charset=\"utf-8\"></head>
    <body style=\"margin:0;font-family:system-ui\">
    <button id=\"normal\" style=\"padding:10px 18px;background:#245db4;color:white;border:0;border-radius:10px;cursor:pointer\"></button>
    <button id=\"slow\" style=\"padding:10px 18px;background:#e5f5f8;color:#155b76;border:0;border-radius:10px;cursor:pointer\"></button>
    <div id=\"state\" style=\"font-size:11px;color:#6a7085;margin-top:6px\"></div>
    <script>
    const word={safe_word};
    document.getElementById('normal').textContent={safe_label};
    document.getElementById('slow').textContent={safe_slow};
    function say(rate) {{
      if(!('speechSynthesis' in window)) {{document.getElementById('state').textContent='Synthèse vocale indisponible';return;}}
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(word);utter.lang='fr-FR';utter.rate=rate;
      const frenchVoices = window.speechSynthesis.getVoices().filter(v=>v.lang.toLowerCase().startsWith('fr'));
      if(frenchVoices.length) utter.voice=frenchVoices[0];
      window.speechSynthesis.speak(utter);
      if(!frenchVoices.length)document.getElementById('state').textContent='Voix FR non confirmée — vérifier la prononciation avec un enseignant.';
    }}
    document.getElementById('normal').onclick=()=>say(.88);
    document.getElementById('slow').onclick=()=>say(.7);
    </script></body></html>"""
    components.html(html, height=95)


lang = st.sidebar.selectbox("Langue de l'interface / Idioma", ["FR", "ES"])
labels = LABELS[lang]
st.title(labels["title"])
st.caption(labels["subtitle"])
st.info("Prototype pédagogique : la sélection de mots est évaluée automatiquement, **mais pas la prononciation**. La voix synthétique dépend du navigateur ; aucun son n'est enregistré.")
st.warning("N'utilisez pas de données nominatives d'élèves. Aucun microphone ni service de reconnaissance vocale n'est activé.")

left, right = st.columns(2)
with left:
    st.markdown("### /y/ — « u »")
    st.write("Langue haute et **vers l'avant** ; lèvres arrondies.  Exemples : **tu, rue, jus, vu**.")
with right:
    st.markdown("### /u/ — « ou »")
    st.write("Langue haute et **vers l'arrière** ; lèvres arrondies.  Exemples : **tout, roue, joue, vous**.")

if "quiz" not in st.session_state:
    reset_quiz()

st.divider()
st.subheader("🎧 Diagnostic — 10 questions")
if st.button(labels["restart"], key="restart"):
    reset_quiz()
    st.rerun()

quiz = st.session_state.quiz
idx = st.session_state.current
answers = st.session_state.answers
if idx < len(quiz):
    q = quiz[idx]
    st.progress(idx / len(quiz), text=f"{idx+1}/{len(quiz)}")
    st.markdown(f"### {labels['question']}")
    speak_widget(q.target, labels["listen"], labels["slow"])
    answered = len(answers) > idx
    c1, c2 = st.columns(2)
    for col, option in zip((c1, c2), q.options):
        with col:
            if st.button(option, key=f"pick_{idx}_{option}", disabled=answered, use_container_width=True):
                st.session_state.answers.append(option)
                st.rerun()
    if answered:
        choice = answers[idx]
        if choice == q.answer:
            st.success(f"{labels['correct']} ✓ — {labels['target']} : {q.answer} {q.target_ipa}")
        else:
            st.error(f"{labels['wrong']} — {labels['target']} : {q.answer} {q.target_ipa}")
        if st.button(labels["end"] if idx == len(quiz)-1 else labels["next"], type="primary"):
            st.session_state.current += 1
            st.rerun()
else:
    report = evaluate(quiz, answers)
    st.success(f"{labels['result']} : **{report['correct']}/{report['total']}** ({report['accuracy_percent']} %)")
    cols = st.columns(2)
    for col, code in zip(cols, ("y", "u")):
        points = report["per_sound"][code]
        with col:
            st.metric(f"/{code}/", f"{points['correct']} / {points['total']}")
    for recommendation in report["recommendations"]:
        st.write("• " + recommendation)
    safe_report = {k: v for k, v in report.items() if k != "responses"}
    safe_report["details"] = report["responses"]
    safe_report["project"] = "PhonoFLE AI V1 — diagnostic anonyme, sans audio"
    st.download_button(labels["download"], data=json.dumps(safe_report, indent=2, ensure_ascii=False).encode("utf-8"),
                       file_name="phonofle_bilan_anonyme.json", mime="application/json")

st.divider()
with st.expander(labels["oral"]):
    st.write("**0** = pas encore · **1** = avec aide · **2** = autonome. Résultat manuel, séparé du score d'écoute.")
    c1, c2, c3 = st.columns(3)
    with c1:
        mouth = st.selectbox("Placement / Posición", [0, 1, 2])
    with c2:
        repeat = st.selectbox("Mots / Palabras", [0, 1, 2])
    with c3:
        phrase = st.selectbox("Phrase / Frase", [0, 1, 2])
    obs = teacher_observation({"mouth_position": mouth, "word_repetition": repeat, "short_phrase": phrase})
    st.caption(f"Observation humaine : {obs['points']} / {obs['maximum']} — aucun score vocal automatique")

st.caption("BOOTO AI & DATA INNOVATION LAB · Junior BOOTO Waba · Objectifs A1 indicatifs ; pas de certification CECRL ni de validation clinique de la parole.")
