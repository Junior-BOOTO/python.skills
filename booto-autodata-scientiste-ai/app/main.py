"""BOOTO AutoData V1 Streamlit UI — batch local analysis only."""
from pathlib import Path
import sys
import logging
import pandas as pd
import streamlit as st
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from autodata.ingestion import read_upload,DataError
from autodata.quality import profile
from autodata.collection import collect
from autodata.task_router import suggest_task, validate_task
from autodata.training import run_experiment
from autodata.demo import make_demo
from autodata.reports import provenance, export_zip

st.set_page_config(page_title='BOOTO AutoData Scientiste AI',page_icon='🧠',layout='wide')
st.markdown("""<style>
.stApp{background:linear-gradient(150deg,#f4fcff,#f8f7ff 55%,#f0fffc);color:#11324d}
.block-container{max-width:1200px;padding-top:2rem}
h1,h2,h3{color:#124e84}.stButton button[kind="primary"]{background:linear-gradient(100deg,#137aab,#048f91,#6448ac);border:0;color:white}
.hero{padding:1.6rem;border:1px solid #cde8f2;border-radius:20px;background:linear-gradient(115deg,#e4f8ff,#e5fff9,#f4eaff)}
.small{color:#547189;font-size:.91rem}
</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🧠 BOOTO AutoData Scientiste AI</h1><p><b>De la donnée au modèle — avec des choix compréhensibles et contrôlés.</b></p><span class="small">V1 expérimentale · CSV / Excel · Diagnostic · Analyse · Classification / Régression · Rapport · Python</span></div>',unsafe_allow_html=True)
st.info('Prototype technique : données fictives recommandées. Ne téléversez pas de données personnelles, financières ou scolaires sensibles sur un hébergement public.')

choice=st.radio('01 · Source des données',['Démonstration — classification','Démonstration — régression','Importer CSV / XLSX','Collecter API / URL publique'],horizontal=True)
try:
    collection_metadata = None
    if choice == 'Collecter API / URL publique':
        st.caption('Collecte à la demande : API JSON ou CSV public direct, sans connexion. Les sites avec authentification et les pages HTML nécessitent un connecteur distinct.')
        with st.form('public_collection'):
            source_url = st.text_input('URL HTTPS publique', placeholder='https://exemple.org/api/donnees')
            source_format = st.selectbox('Format de la source', ['json', 'csv'])
            records_path = st.text_input('Chemin des observations JSON (facultatif)', help='Exemple : data.results. Laissez vide pour une liste d’objets à la racine.')
            pages = st.number_input('Nombre de pages à collecter', min_value=1, max_value=5, value=1)
            page_parameter = st.text_input('Paramètre de pagination (si plusieurs pages)', placeholder='page')
            first_page = st.number_input('Première page', min_value=0, value=1)
            permitted = st.checkbox('La source est publique et autorise cette collecte ; l’URL ne contient aucune donnée personnelle ni clé secrète.')
            submitted = st.form_submit_button('Collecter les données')
        if submitted:
            st.session_state.pop('exp_source_key', None)
            st.session_state.pop('collected_data', None)
            if not permitted:
                raise DataError('Confirmez les conditions de collecte avant de continuer.')
            with st.spinner('Collecte et structuration des données…'):
                collected, metadata = collect(source_url, source_format, records_path, int(pages), page_parameter, int(first_page))
                st.session_state['collected_data'] = (collected, metadata)
        if 'collected_data' not in st.session_state:
            st.stop()
        df, collection_metadata = st.session_state['collected_data']
        raw = df.to_csv(index=False).encode('utf-8')
        label = 'collecte_publique_normalisee.csv'
        is_demo = False
        st.success(f'Collecte terminée : {len(df)} observations, {len(df.columns)} colonnes.')
        st.caption('Seules les pages demandées ont été collectées. Les données restent dans cette session ; aucune collecte récurrente n’est programmée.')
        with st.expander('Traçabilité de la collecte'):
            st.json(collection_metadata)
        st.download_button('Télécharger les données collectées (CSV)', raw, file_name=label, mime='text/csv')
    elif choice=='Importer CSV / XLSX':
        f=st.file_uploader('Choisissez un CSV UTF-8 (virgule, point-virgule, tabulation) ou XLSX (5 Mo maximum)',type=['csv','xlsx'])
        if f is None:
            st.stop()
        raw=f.getvalue();label=f.name;df=read_upload(raw,label);is_demo=False
    else:
        kind='classification' if 'classification' in choice else 'regression'
        df=make_demo(kind);raw=df.to_csv(index=False).encode('utf-8');label=f'demo_{kind}_synthetique.csv';is_demo=True
    p=profile(df)
    st.subheader('02 · Comprendre la qualité des données')
    cols=st.columns(4)
    for c,k,v in zip(cols,['Observations','Colonnes','Doublons','Cellules manquantes'],[p['rows'],p['columns'],p['duplicates'],p['missing_cells']]): c.metric(k,v)
    st.dataframe(df.head(20),hide_index=True,use_container_width=True)
    with st.expander('Voir le diagnostic détaillé',expanded=False):
        st.dataframe(pd.DataFrame(p['column_details']),hide_index=True,use_container_width=True)
        if p['all_missing_columns']: st.warning('Colonnes entièrement vides : '+', '.join(p['all_missing_columns']))
    st.subheader('03 · Exploration descriptive')
    nums=df.select_dtypes(include='number')
    if not nums.empty:
        st.dataframe(nums.describe().round(2),use_container_width=True)
        selected_num=st.selectbox('Variable numérique à explorer',nums.columns.tolist())
        values = df[selected_num].dropna()
        distribution = values.value_counts(bins=12).sort_index() if not values.empty else pd.Series(dtype=int)
        chart = pd.DataFrame({'intervalle': [str(k) for k in distribution.index], 'effectif': distribution.values})
        st.bar_chart(chart.set_index('intervalle'))
    st.subheader('04 · Décider avant de modéliser')
    target=st.selectbox('Variable cible à prédire',df.columns.tolist(),index=len(df.columns)-1)
    hint=suggest_task(df[target]);st.caption('Suggestion automatique indicative : '+hint+'. Le choix final vous appartient.')
    task=st.radio('Tâche supervisée', ['classification','regression'],index=0 if hint=='classification' else 1,horizontal=True)
    default_exclusions=p['all_missing_columns']
    exclusions=st.multiselect('Colonnes explicatives à exclure (identifiants, fuite, variables sensibles)',[c for c in df.columns if c!=target],default=[c for c in default_exclusions if c!=target])
    if df[target].nunique()==len(df) and task=='classification':st.warning('Une classe par ligne : vérifiez votre cible, qui pourrait être un identifiant.')
    st.warning('Avant validation, vérifiez les identifiants, variables postérieures au résultat, dates/séries temporelles, consentement et autorisations.')
    remove_dupes=st.checkbox('Je demande explicitement de supprimer les lignes strictement identiques avant la séparation train/test.',value=False)
    approved=st.checkbox('Je confirme la cible, la tâche et les colonnes retenues ; mes données sont autorisées pour cette analyse.',value=False)
    configuration_valid = True
    try:
        validate_task(df, target, task, exclusions)
    except DataError as exc:
        configuration_valid = False
        st.warning(str(exc))
        st.caption('Classification : prédire une catégorie. Régression : prédire un nombre. Pour changer de démonstration, utilisez la source des données en haut de page.')
    if st.button('▶ Analyser et entraîner',type='primary',disabled=not approved or not configuration_valid):
        with st.spinner('Calcul des modèles (validation croisée uniquement sur entraînement)…'):
            result=run_experiment(df,target,task,exclusions,remove_duplicates=remove_dupes)
            st.session_state['exp_result']=result
            st.session_state['exp_prov']=provenance(raw,label)
            if collection_metadata is not None:
                st.session_state['exp_prov']['collection'] = collection_metadata
            st.session_state['exp_quality']=p
            st.session_state['exp_source_key']=(label,st.session_state['exp_prov']['sha256'],target,task,tuple(exclusions),remove_dupes)
    key=(label,provenance(raw,label)['sha256'],target,task,tuple(exclusions),remove_dupes)
    if st.session_state.get('exp_source_key') == key:
        r=st.session_state['exp_result']
        st.subheader('05 · Résultats calculés et interprétation')
        st.success(f"Modèle retenu : {r['best_model']} — choisi sur validation croisée, sans consulter le test.")
        st.caption(r['method'])
        st.dataframe(pd.DataFrame(r['comparison_cv']).drop(columns=['score_validation_train']),use_container_width=True,hide_index=True)
        st.markdown('**Mesures sur le jeu de test réservé**')
        st.dataframe(pd.DataFrame(r['test_metrics']).T,use_container_width=True)
        if r['confusion']:
            st.caption('Matrice de confusion du meilleur modèle')
            st.dataframe(pd.DataFrame(r['confusion']['matrix'],index=r['confusion']['labels'],columns=r['confusion']['labels']))
        for w in r['warnings']:st.caption('• '+w)
        with st.expander('Examiner les prédictions du jeu de test'):
            st.dataframe(r['predictions'], hide_index=True, use_container_width=True)
            if r['task'] == 'regression':
                st.scatter_chart(r['predictions'], x='valeur_reelle', y='prediction')
                residuals = r['predictions'].assign(residu=lambda d: d['valeur_reelle'] - d['prediction'])
                st.scatter_chart(residuals, x='prediction', y='residu')
                st.caption('Résidu = valeur réelle − prédiction. Une structure visible peut révéler des erreurs systématiques.')
        st.subheader('06 · Rapport exportable')
        include_source=st.checkbox('Inclure explicitement les données d’origine dans le ZIP (déconseillé pour données sensibles)',value=False)
        st.download_button('⬇ Télécharger rapport HTML + manifeste (ZIP)',
            data=export_zip(r,p,st.session_state['exp_prov'],raw if include_source else None,label),
            file_name='booto_autodata_rapport_v1.zip',mime='application/zip')
        st.caption('Le code du projet est disponible sur GitHub. Aucune donnée n’est enregistrée dans une base par notre code. Un hébergeur tiers peut conserver ses propres journaux.')
except DataError as exc:
    st.error(str(exc))
except Exception:
    logging.getLogger(__name__).error('Échec du traitement AutoData ; détails masqués pour protéger les données.')
    st.error('Une erreur technique s’est produite. Consultez le journal technique local et vérifiez le schéma du fichier.')
    # Do not expose stack traces or raw sensitive values to a public user.
    st.stop()
