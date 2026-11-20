
"""Application web AbAssurance de détection des fraudes."""

import streamlit as st
import pandas as pd

from src.src.prediction import train_prediction_model

st.set_page_config(
    page_title="AbAssurance Data Platform",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AbAssurance Data Platform")
st.header("Détection du risque de fraude")

st.write("Analysez un sinistre pour estimer son risque de fraude.")

amount = st.number_input(
    "Montant estimé (€)",
    min_value=0.0,
    value=1000.0
)

score = st.slider(
    "Score de fraude",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01
)

if st.button("Analyser le sinistre"):

    try:
        # Entraînement sur les données brutes contenant les deux classes.
        model, accuracy = train_prediction_model(
            "data/raw/claims.csv"
        )

        # Prédiction du risque de fraude.
        claim = pd.DataFrame([{
            "estimated_amount": amount,
            "fraud_score": score
        }])

        prediction = model.predict(claim)[0]

        if prediction == 1:
            st.error("⚠️ Risque de fraude détecté.")
        else:
            st.success("✅ Aucun risque de fraude détecté.")

        st.metric(
            "Précision du modèle",
            f"{accuracy:.0%}"
        )

    except (FileNotFoundError, ValueError, KeyError) as error:
        st.error(f"Erreur lors de l'analyse : {error}")

