"""Tests du pipeline et du modèle de prédiction."""

import pandas as pd
import pytest

from src.src.pipeline import clean_data
from src.src.prediction import train_prediction_model


def test_clean_data_separates_claims(tmp_path):
    data = pd.DataFrame({
        "estimated_amount": [1200, None, -200, 800],
        "fraud_score": [0.2, 0.5, 0.3, None],
        "is_fraud": [0, 1, 0, 0]
    })

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "clean.csv"
    data.to_csv(input_file, index=False)

    accepted, rejected = clean_data(input_file, output_file)

    assert len(accepted) == 1
    assert len(rejected) == 3
    assert (tmp_path / "clean.csv").exists()
    assert (tmp_path / "clean_rejected.csv").exists()
    assert "MONTANT_MANQUANT" in rejected["rejection_reason"].values
    assert "MONTANT_NEGATIF" in rejected["rejection_reason"].values
    assert "SCORE_FRAUDE_MANQUANT" in rejected["rejection_reason"].values


def test_clean_data_rejects_invalid_fraud_score(tmp_path):
    data = pd.DataFrame({
        "estimated_amount": [1000],
        "fraud_score": [1.5],
        "is_fraud": [1]
    })

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "clean.csv"
    data.to_csv(input_file, index=False)

    accepted, rejected = clean_data(input_file, output_file)

    assert len(accepted) == 0
    assert len(rejected) == 1
    assert "SCORE_FRAUDE_INVALIDE" in rejected.iloc[0]["rejection_reason"]


def test_clean_data_raises_error_if_column_missing(tmp_path):
    data = pd.DataFrame({
        "estimated_amount": [1000],
        "fraud_score": [0.5]
    })

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "clean.csv"
    data.to_csv(input_file, index=False)

    with pytest.raises(ValueError):
        clean_data(input_file, output_file)


def test_prediction_model_training(tmp_path):
    data = pd.DataFrame({
        "estimated_amount": [
            100, 200, 300, 400, 500,
            600, 700, 800, 900, 1000
        ],
        "fraud_score": [
            0.1, 0.2, 0.15, 0.3, 0.25,
            0.8, 0.9, 0.85, 0.95, 0.75
        ],
        "is_fraud": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    })

    input_file = tmp_path / "claims.csv"
    data.to_csv(input_file, index=False)

    model, accuracy = train_prediction_model(input_file)

    assert model is not None
    assert 0 <= accuracy <= 1

 
