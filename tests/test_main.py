

"""Tests unitaires du nettoyage des données de sinistres."""

import pandas as pd
import pytest

from src.src.pipeline import clean_data


def test_clean_data_separates_accepted_and_rejected_claims(tmp_path):
    """Vérifie la séparation des sinistres acceptés et rejetés."""
    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    data = pd.DataFrame({
        "estimated_amount": [1500, None, -200, 800],
        "fraud_score": [0.2, 0.5, 0.4, None],
    })

    data.to_csv(input_file, index=False)

    accepted, rejected = clean_data(input_file, output_file)

    assert len(accepted) == 1
    assert len(rejected) == 3

    assert accepted["estimated_amount"].iloc[0] == 1500
    assert accepted["fraud_score"].iloc[0] == 0.2

    assert "MONTANT_MANQUANT" in rejected["rejection_reason"].values
    assert "MONTANT_NEGATIF" in rejected["rejection_reason"].values
    assert "SCORE_FRAUDE_MANQUANT" in rejected["rejection_reason"].values

    assert output_file.exists()
    assert (tmp_path / "claims_clean_rejected.csv").exists()


def test_clean_data_rejects_invalid_fraud_score(tmp_path):
    """Vérifie le rejet d'un score de fraude hors limites."""
    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    pd.DataFrame({
        "estimated_amount": [1200, 900],
        "fraud_score": [1.5, 0.3],
    }).to_csv(input_file, index=False)

    accepted, rejected = clean_data(input_file, output_file)

    assert len(accepted) == 1
    assert len(rejected) == 1
    assert rejected.iloc[0]["rejection_reason"] == "SCORE_FRAUDE_INVALIDE"


def test_clean_data_raises_error_when_required_column_is_missing(tmp_path):
    """Vérifie le contrôle des colonnes obligatoires."""
    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    pd.DataFrame({
        "estimated_amount": [1200],
    }).to_csv(input_file, index=False)

    with pytest.raises(ValueError, match="fraud_score"):
        clean_data(input_file, output_file)


def test_clean_data_raises_error_when_file_does_not_exist(tmp_path):
    """Vérifie la gestion d'un fichier source absent."""
    input_file = tmp_path / "inexistant.csv"
    output_file = tmp_path / "claims_clean.csv"

    with pytest.raises(FileNotFoundError):
        clean_data(input_file, output_file)
