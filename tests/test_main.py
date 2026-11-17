
"""Tests unitaires du nettoyage des données de sinistres."""

import pandas as pd

from src.src.pipeline import clean_data


def test_clean_data_removes_invalid_claims(tmp_path):
    """Vérifie le traitement des montants manquants et négatifs."""
    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    data = pd.DataFrame({
        "estimated_amount": [1500, None, -200, 800],
        "fraud_score": [0.2, 0.5, None, None],
    })
    data.to_csv(input_file, index=False)

    result = clean_data(input_file, output_file)

    assert len(result) == 2
    assert (result["estimated_amount"] >= 0).all()
    assert result["fraud_score"].isna().sum() == 0
    assert output_file.exists()


def test_clean_data_rejects_missing_amount(tmp_path):
    """Vérifie qu'un sinistre sans montant n'est pas conservé."""
    input_file = tmp_path / "claims.csv"
    output_file = tmp_path / "claims_clean.csv"

    data = pd.DataFrame({
        "estimated_amount": [None, 1200],
        "fraud_score": [0.4, 0.2],
    })
    data.to_csv(input_file, index=False)

    result = clean_data(input_file, output_file)

    assert len(result) == 1
    assert result.iloc[0]["estimated_amount"] == 1200
