import pandas as pd
import streamlit as st
from engine import demo,run,order_quantity,validate
st.set_page_config(page_title='BOOTO Demand & Stock Lab',layout='wide')
st.title('BOOTO Demand & Stock Lab')
st.caption('Junior BOOTO Waba · Prototype de portfolio · Prévisions hebdomadaires et simulation de stock')
st.info('Démonstration synthétique par défaut. Aucun gain commercial réel mesuré.')
f=st.file_uploader('CSV : date, product, sales — une ligne par produit et semaine',type='csv')
try:
    df=validate(pd.read_csv(f) if f else demo())
    pred,metrics=run(df)
    product=st.selectbox('Produit',pred['product'].unique())
    history=df[df['product']==product].copy();history['date']=pd.to_datetime(history['date'])
    future=pred[pred['product']==product]
    st.line_chart(pd.concat([history.set_index('date')['sales'].rename('Historique'),future.set_index('date')['forecast'].rename('Prévision')],axis=1))
    st.subheader('Évaluation sur les 12 dernières semaines')
    st.dataframe(pd.DataFrame([{k:v for k,v in m.items() if k!='validation_mae'} for m in metrics]))
    st.caption('MAE en unités/semaine. Sélection sur 12 semaines antérieures au test ; prévisions à quatre semaines, avec réentraînement à chaque origine. Le modèle ne gagne pas nécessairement face à la moyenne des quatre dernières semaines.')
    st.subheader('Simulation du réapprovisionnement pour quatre semaines')
    stock=st.number_input('Stock disponible',min_value=0,value=100)
    incoming=st.number_input('Livraisons déjà prévues sur la période',min_value=0,value=0)
    buffer=st.number_input('Réserve supplémentaire choisie (unités)',min_value=0,value=20)
    demand=float(future.forecast.sum())
    st.metric('Demande prévue sur quatre semaines',round(demand,1))
    st.metric('Quantité indicative à commander',order_quantity(demand,stock,incoming,buffer))
    st.caption('Formule : plafond(max(0, demande + réserve − stock − livraisons)). Hypothèse de disponibilité à temps ; délais, coûts et ruptures intra-période non modélisés. La réserve est un scénario utilisateur, pas un intervalle de confiance.')
    st.download_button('Télécharger les prévisions CSV',pred.to_csv(index=False),'forecast.csv','text/csv')
except (ValueError,TypeError,KeyError) as exc:
    st.error(str(exc))
