

"""Tests unitaires du nettoyage des données de sinistres."""

import pandas as pd
import pytest

from src.src.pipeline import clean_data


def test_clean_data_separates_accepted_and_rejected_claims(tmp_path):
    """Vérifie la séparation des sinistres acceptés et rejetés."""

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    data = pd.DataFrame({
        "estimated_amount": [1500, None, -200, 800, 600],
        "fraud_score": [0.2, 0.5, 0.3, None, 0.1],
    })

    data.to_csv(input_file, index=False)

    accepted, rejected = clean_data(input_file, output_file)

    assert len(accepted) == 2
    assert len(rejected) == 3
    assert accepted["estimated_amount"].ge(0).all()
    assert accepted["fraud_score"].notna().all()

    assert "MONTANT_MANQUANT" in rejected["rejection_reason"].values
    assert "MONTANT_NEGATIF" in rejected["rejection_reason"].values
    assert "SCORE_FRAUDE_MANQUANT" in rejected["rejection_reason"].values

    assert output_file.exists()

    rejected_file = tmp_path / "claims_clean_rejected.csv"
    assert rejected_file.exists()


def test_clean_data_raises_error_when_required_column_is_missing(tmp_path):
    """Vérifie le contrôle des colonnes obligatoires."""

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    pd.DataFrame({
        "estimated_amount": [1200],
    }).to_csv(input_file, index=False)

    with pytest.raises(ValueError, match="fraud_score"):
        clean_data(input_file, output_file)


def test_clean_data_accepts_valid_claims(tmp_path):
    """Vérifie qu'un sinistre valide est accepté."""

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    pd.DataFrame({
        "estimated_amount": [1200],
        "fraud_score": [0.2],
    }).to_csv(input_file, index=False)

    accepted, rejected = clean_data(input_file, output_file)

    assert len(accepted) == 1
    assert len(rejected) == 0
    assert accepted.iloc[0]["estimated_amount"] == 1200
