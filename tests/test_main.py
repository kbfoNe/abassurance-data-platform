
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
        "fraud_score": [0.2, 0.5, None, None],
    })

    data.to_csv(input_file, index=False)

    accepted, rejected = clean_data(input_file, output_file)

    assert len(accepted) == 2
    assert len(rejected) == 2

    assert (accepted["estimated_amount"] >= 0).all()
    assert accepted["fraud_score"].isna().sum() == 0

    assert output_file.exists()

    rejected_reasons = rejected["rejection_reason"].tolist()

    assert "MONTANT_MANQUANT" in rejected_reasons
    assert "MONTANT_NEGATIF" in rejected_reasons


def test_clean_data_rejects_missing_amount_with_reason(tmp_path):
    """Vérifie le rejet d'un sinistre sans montant."""

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    data = pd.DataFrame({
        "estimated_amount": [None, 1200],
        "fraud_score": [0.4, 0.2],
    })

    data.to_csv(input_file, index=False)

    accepted, rejected = clean_data(input_file, output_file)

    assert len(accepted) == 1
    assert len(rejected) == 1

    assert (
        rejected.iloc[0]["rejection_reason"]
        == "MONTANT_MANQUANT"
    )

    rejected_file = tmp_path / "claims_clean_rejected.csv"

    assert rejected_file.exists()


def test_clean_data_raises_error_when_required_column_is_missing(tmp_path):
    """Vérifie le contrôle des colonnes obligatoires."""

    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    data = pd.DataFrame({
        "estimated_amount": [1200],
    })

    data.to_csv(input_file, index=False)

    with pytest.raises(ValueError, match="fraud_score"):
        clean_data(input_file, output_file)

