"""Interface web de prédiction des fraudes."""

import streamlit as st
import pandas as pd

from src.src.prediction import train_prediction_model

st.set_page_config(page_title="AbAssurance", page_icon="🛡️")

st.title("🛡️ AbAssurance Data Platform")
st.subheader("Détection du risque de fraude")

st.write("Analysez un sinistre pour estimer son risque de fraude.")

amount = st.number_input("Montant estimé (€)", min_value=0.0, value=1000.0)
score = st.slider("Score de fraude", 0.0, 1.0, 0.5)

if st.button("Analyser le sinistre"):
    try:
        model, accuracy = train_prediction_model(
            "data/processed/claims_clean.csv"
        )

        prediction = model.predict(
            pd.DataFrame([{
                "estimated_amount": amount,
                "fraud_score": score
            }])
        )[0]

        if prediction == 1:
            st.error("Risque de fraude détecté.")
        else:
            st.success("Aucun risque de fraude détecté.")

        st.caption(f"Précision du modèle sur le jeu de test : {accuracy:.0%}")

    except Exception as error:
        st.warning(f"Impossible d'effectuer la prédiction : {error}")
