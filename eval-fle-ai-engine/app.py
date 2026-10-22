"""BOOTO Éval'FLE AI Engine · application Streamlit — prototype V1."""
from __future__ import annotations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
import streamlit as st
from evalfle import generate_exam, build_pdf, build_docx, grade_answers, overview

st.set_page_config(page_title="BOOTO Éval'FLE AI Engine",page_icon='📘',layout='wide')
st.markdown('''<style>
.block-container {max-width:1140px;padding-top:2rem}
.hero {padding:1.4rem 1.5rem;border-radius:20px;background:linear-gradient(115deg,#123b70,#087d92 61%,#7750ad);color:white;margin-bottom:1.3rem}
.hero h1{margin:0;color:white;font-size:2.2rem}
.hero p{color:#f3fbff;margin:.6rem 0 0}
.caption{font-size:.83rem;color:#536b83}
</style>''',unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>📘 BOOTO Éval’FLE AI Engine</h1><p>Évaluations scolaires structurées · FLE A1 · Grille de correction · Exports Word & PDF</p></div>',unsafe_allow_html=True)
st.caption('Prototype de génération à partir d’une banque éditoriale ; pas de modèle génératif d’IA, pas de certification CECRL, aucune donnée élève conservée.')

with st.sidebar:
    st.header('Préparer une évaluation')
    grade=st.selectbox('Classe',options=(4,5),format_func=lambda g:f'Grade {g}')
    number=st.select_slider('Nombre de questions',options=[12,15,30],value=30)
    variant=st.number_input('Numéro de variante (reproductible)',min_value=1,max_value=9999,value=1,step=1)
    st.info('Chaque variante mélange l’ordre des questions et des réponses tout en conservant la correction correspondante.')
    st.markdown('**V1 : exemples illustratifs** — les thèmes doivent être vérifiés au regard de votre progression annuelle.')

questions=generate_exam(grade=grade,n=number,seed=variant)
key=f'G{grade}_N{number}_V{variant}'

left,mid,right=st.columns(3)
left.metric('Questions',len(questions))
mid.metric('Domaines évalués',len(overview(questions)))
right.metric('Points possibles',len(questions))

st.subheader('Téléchargement des sujets et des corrigés')
with st.spinner('Préparation des fichiers…'):
    try:
        student_pdf=build_pdf(questions,teacher=False)
        teacher_pdf=build_pdf(questions,teacher=True)
        student_docx=build_docx(questions,teacher=False)
        teacher_docx=build_docx(questions,teacher=True)
    except Exception as exc:
        st.error(f'Impossible de préparer les exports : {exc}')
        st.stop()

name=f'evalfle_grade{grade}_{number}q_v{variant}'
c1,c2,c3,c4=st.columns(4)
c1.download_button('📄 Sujet PDF',student_pdf,f'{name}_eleve.pdf',mime='application/pdf',use_container_width=True)
c2.download_button('📝 Sujet Word',student_docx,f'{name}_eleve.docx',mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',use_container_width=True)
c3.download_button('✅ Corrigé PDF',teacher_pdf,f'{name}_corrige.pdf',mime='application/pdf',use_container_width=True)
c4.download_button('📋 Corrigé Word',teacher_docx,f'{name}_corrige.docx',mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',use_container_width=True)

preview,criteria,correction,about=st.tabs(['🧾 Questionnaire','🎯 Critères « Je peux… »','📊 Correction anonyme','🔒 Méthode & limites'])
with preview:
    st.markdown('**Consigne :** coche une réponse parmi A, B, C et D pour chaque question. Le corrigé est accessible dans les fichiers enseignant.')
    for i,q in enumerate(questions,1):
        st.markdown(f'**{i}. {q.question}**')
        st.write('  ·  '.join(f'{letter}. {opt}' for letter,opt in zip('ABCD',q.choices)))
        st.caption(f'Domaine : {q.category}')
        st.divider()
with criteria:
    for row in overview(questions):
        st.markdown(f"### {row['category']} · {row['count']} questions")
        st.write(row['criterion'])
    st.info('Il s’agit d’indicateurs pédagogiques observables dans ce questionnaire, et non de descripteurs CECRL officiels ou de validation de compétences orales.')
with correction:
    st.markdown('Cette correction est **non nominative**. Elle reste dans votre session Streamlit et ne constitue pas un dossier élève.')
    with st.form(f'corr-{key}'):
        choices={}
        for i,q in enumerate(questions,1):
            val=st.selectbox(f'{i}. {q.question}',options=['—','A','B','C','D'],key=f'ans-{key}-{i}')
            if val!='—':choices[i]=val
        submit=st.form_submit_button('Calculer les résultats par domaine')
        if submit:
            result=grade_answers(questions,choices)
            st.success(f"{result['correct']} / {result['total']} bonnes réponses (absence = 0 point).")
            st.table([{'Domaine':cat,'Réponses justes':f"{r['correct']}/{r['total']}"} for cat,r in result['per_category'].items()])
            st.caption('Aucune étiquette « acquis » ou « niveau CECRL certifié » n’est inférée automatiquement de cette note.')
with about:
    st.markdown('''
**Fonctionnement V1.** Banque originale de 60 questions à quatre propositions (30 par grade), répartition équilibrée entre trois thèmes, mélange déterministe, vérification de réponse, export de documents imprimables.

**Périmètre actuel.** Grade 4 : maison, paysages et journée typique. Grade 5 : droits et devoirs, écoresponsabilité et communication quotidienne. Les trois périodes et les progressions officielles ne sont pas encore importées : les thèmes ci-dessus sont une **banque de démonstration**.

**Limites.** Aucun modèle de langage, aucune création automatique de nouvelles questions, aucun diagnostic officiel de niveau A1/A2. Un QCM sans support sonore ne permet pas d’évaluer directement l’expression orale, la compréhension orale ou la production écrite. Toute utilisation sommative requiert la relecture et l’approbation de l’enseignant.

**Confidentialité.** Aucune connexion API, aucun téléchargement de liste d’élèves, aucun enregistrement de réponses par le code de l'application. Un fournisseur d’hébergement peut néanmoins conserver des journaux techniques.
''')
    st.link_button('Consulter les trois projets précédents', 'https://github.com/Junior-BOOTO/python.skills', use_container_width=True)
st.divider()
st.caption('© 2026 Junior BOOTO Waba · BOOTO AI & DATA INNOVATION LAB · Éval’FLE AI Engine V1 — prototype')
