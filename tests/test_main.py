

 
"""Tests unitaires du pipeline de nettoyage des sinistres."""

import pandas as pd
import pytest

from src.src.pipeline import clean_data


def test_clean_data_separates_accepted_and_rejected_claims(tmp_path):
    """Vérifie la séparation des sinistres acceptés et rejetés."""

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    data = pd.DataFrame({
        "estimated_amount": [1200, None, -200, 800],
        "fraud_score": [0.2, 0.5, 0.3, None],
        "is_fraud": [0, 1, 0, 0],
    })

    data.to_csv(input_file, index=False)

    accepted, rejected = clean_data(input_file, output_file)

    assert len(accepted) == 1
    assert len(rejected) == 3

    assert accepted.iloc[0]["estimated_amount"] == 1200

    assert set(rejected["rejection_reason"]) == {
        "MONTANT_MANQUANT",
        "MONTANT_NEGATIF",
        "SCORE_FRAUDE_MANQUANT",
    }

    assert output_file.exists()

    rejected_file = tmp_path / "claims_clean_rejected.csv"
    assert rejected_file.exists()


def test_clean_data_rejects_invalid_fraud_score(tmp_path):
    """Vérifie le rejet d'un score de fraude hors limites."""

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    data = pd.DataFrame({
        "estimated_amount": [1500],
        "fraud_score": [1.5],
        "is_fraud": [1],
    })

    data.to_csv(input_file, index=False)

    accepted, rejected = clean_data(input_file, output_file)

    assert len(accepted) == 0
    assert len(rejected) == 1
    assert rejected.iloc[0]["rejection_reason"] == "SCORE_FRAUDE_INVALIDE"


def test_clean_data_raises_error_when_column_is_missing(tmp_path):
    """Vérifie qu'une colonne obligatoire manquante provoque une erreur."""

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    data = pd.DataFrame({
        "estimated_amount": [1200],
        "fraud_score": [0.2],
    })

    data.to_csv(input_file, index=False)

    with pytest.raises(ValueError, match="Colonnes obligatoires manquantes"):
        clean_data(input_file, output_file)
