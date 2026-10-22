"""BOOTO Correcteur FLE AI — prototype d'assistance à la rétroaction écrite."""
from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
import streamlit as st
from correcteur_fle import analyze,review_suggestions,THEMES,to_pdf,to_docx,to_text
from correcteur_fle.engine import MAX_CHARS

st.set_page_config(page_title='BOOTO Correcteur FLE | Studio A1', page_icon='🖊️',layout='wide')
st.markdown('''<style>
.block-container{max-width:1100px;padding-top:1.8rem}
.hero{background:linear-gradient(111deg,#153a73 10%,#078b98 57%,#7255b7);border-radius:21px;padding:1.5rem 1.7rem;color:white;margin-bottom:1rem}
.hero h1{color:white;margin:0;font-size:clamp(1.7rem,3vw,2.7rem)}.hero p{color:#f1fafe;margin:.65rem 0 0}
small, .muted{color:#527188}
</style>''',unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🖊️ BOOTO Correcteur FLE</h1><p>Repérer · Expliquer · Valider · Exporter — Productions écrites A1</p></div>',unsafe_allow_html=True)
st.caption('V1 : moteur de règles transparent et limité. Pas de correction générale du français ni de modèle de langage. La validation humaine est indispensable.')
EXAMPLES={
    'routine':'le matin je se leve a sept heures. ensuite je va a l ecole et je manges.',
    'ecologie':'je doit protege les arbre. nous doit recycler les dechets.'
}
with st.sidebar:
    st.header('Préparer la révision')
    theme=st.selectbox('Thème pédagogique',list(THEMES),format_func=lambda x:THEMES[x])
    st.info('Utilisez des textes fictifs ou anonymisés. Ne saisissez aucun nom d’élève ou information personnelle.')
    st.markdown('**Activités visées** : Grade 4 — routine ; Grade 5 — écologie et droits/devoirs.')
    st.markdown('**Statut** : prototype non évalué en classe, suggestions révisables.')
if st.session_state.get('theme_key')!=theme:
    st.session_state['theme_key']=theme
    st.session_state['draft_text']=EXAMPLES[theme]
text=st.text_area('Production écrite à analyser (fictive ou anonymisée)',key='draft_text',height=150,max_chars=MAX_CHARS)
if not text.strip():
    st.info('Saisissez quelques phrases pour explorer les suggestions.')
    st.stop()
try:result=analyze(text,theme)
except ValueError as error:
    st.error(str(error));st.stop()
col1,col2,col3=st.columns(3)
col1.metric('Caractères',len(text))
col2.metric('Suggestions ciblées',len(result.suggestions))
col3.metric('Validation','Enseignant')
st.info(result.observation)
col_orig,col_prop=st.columns(2)
with col_orig:
    st.subheader('Texte original')
    st.write(text)
with col_prop:
    st.subheader('Proposition automatique')
    st.write(result.preview)
st.subheader('Examiner les pistes de correction')
st.caption('Chaque suggestion est désactivable. Le texte révisé et les exports ne contiennent que les propositions que vous retenez.')
selected=set()
for i,s in enumerate(result.suggestions):
    with st.container(border=True):
        left,right=st.columns([2,3])
        with left:
            value=st.checkbox(f'Accepter la piste {i+1}',value=True,key=f'sel-{theme}-{text}-{i}-{s.ident}')
            st.markdown(f'**{s.original}** → **{s.proposal}**')
            st.caption(s.category)
        with right:
            st.write(s.explanation)
            st.caption('Critère : '+s.criterion)
        if value:selected.add(i)
st.subheader('Texte révisé — après validation')
revised=review_suggestions(text,result.suggestions,selected)
st.code(revised,language=None)
notes=st.text_area('Observation facultative de l’enseignant (aucune note automatique)',placeholder='Ce qui est réussi, la priorité de remédiation, la prochaine activité...',max_chars=900,height=100)
st.markdown('#### Exporter la rétroaction')
try:
    txt=to_text(result,selected,notes).encode('utf-8-sig')
    word=to_docx(result,selected,notes)
    pdf=to_pdf(result,selected,notes)
except Exception as exc:
    st.error(f'La génération du retour a rencontré une erreur : {exc}');st.stop()
c1,c2,c3=st.columns(3)
c1.download_button('📄 Fiche PDF',pdf,'retour_correcteur_fle.pdf',mime='application/pdf',use_container_width=True)
c2.download_button('📝 Fiche Word',word,'retour_correcteur_fle.docx',mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',use_container_width=True)
c3.download_button('📃 Retour TXT',txt,'retour_correcteur_fle.txt',mime='text/plain',use_container_width=True)
with st.expander('Méthode, limites et confidentialité'):
    st.markdown('''La V1 repère uniquement **quelques formulations préprogrammées** sur la routine quotidienne et l’écoresponsabilité. Elle n’évalue pas la qualité globale, la créativité, l’argumentation, le niveau CECRL ou l’intention de l’apprenant. Les propositions doivent être examinées par l’enseignant, qui peut les refuser. Aucun compte, base de données, stockage de textes ou appel à une API tierce n’est inclus dans le code ; l’hébergement lui-même peut produire des journaux techniques. **Ne saisissez pas de données personnelles d’élèves dans la version publique.**''')
st.divider()
st.caption('© 2026 Junior BOOTO Waba · BOOTO AI & DATA INNOVATION LAB · V1 expérimentale')
