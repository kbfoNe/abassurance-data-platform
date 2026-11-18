
"""Pipeline de nettoyage des données de sinistres."""

from pathlib import Path

import pandas as pd


def clean_data(input_file, output_file):
    """
    Nettoie les données de sinistres.

    Sépare les données acceptées et rejetées.
    Ajoute un motif pour chaque rejet.
    """
    input_file = Path(input_file)
    output_file = Path(output_file)

    required_columns = {"estimated_amount", "fraud_score"}

    data = pd.read_csv(input_file)

    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(
            f"Colonnes obligatoires manquantes : {', '.join(sorted(missing_columns))}"
        )

    data["rejection_reason"] = ""

    missing_amount = data["estimated_amount"].isna()
    negative_amount = data["estimated_amount"] < 0
    missing_score = data["fraud_score"].isna()

    data.loc[missing_amount, "rejection_reason"] = "MONTANT_MANQUANT"

    data.loc[
        ~missing_amount & negative_amount,
        "rejection_reason"
    ] = "MONTANT_NEGATIF"

    data.loc[
        ~missing_amount & ~negative_amount & missing_score,
        "rejection_reason"
    ] = "SCORE_FRAUDE_MANQUANT"

    rejected = data[data["rejection_reason"] != ""].copy()
    accepted = data[data["rejection_reason"] == ""].copy()

    accepted = accepted.drop(columns=["rejection_reason"])

    output_file.parent.mkdir(parents=True, exist_ok=True)
    accepted.to_csv(output_file, index=False)

    rejected_file = output_file.with_name(
        f"{output_file.stem}_rejected{output_file.suffix}"
    )
    rejected.to_csv(rejected_file, index=False)

    return accepted, rejected
