
"""Pipeline de nettoyage des données de sinistres."""

from pathlib import Path

import pandas as pd


def clean_data(input_file, output_file):
    """
    Nettoie les données de sinistres.

    Sépare les sinistres acceptés et rejetés et indique
    le motif de rejet de chaque ligne non conforme.
    """
    input_file = Path(input_file)
    output_file = Path(output_file)

    required_columns = {
        "estimated_amount",
        "fraud_score",
        "is_fraud",
    }

    data = pd.read_csv(input_file)

    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(
            "Colonnes obligatoires manquantes : "
            + ", ".join(sorted(missing_columns))
        )

    data["rejection_reason"] = ""

    # Vérification des montants
    missing_amount = data["estimated_amount"].isna()
    negative_amount = data["estimated_amount"] < 0

    # Vérification du score de fraude
    missing_score = data["fraud_score"].isna()
    invalid_score = (
        data["fraud_score"].notna()
        & ~data["fraud_score"].between(0, 1)
    )

    # Vérification de la classification
    missing_label = data["is_fraud"].isna()
    invalid_label = (
        data["is_fraud"].notna()
        & ~data["is_fraud"].isin([0, 1])
    )

    checks = [
        (missing_amount, "MONTANT_MANQUANT"),
        (negative_amount, "MONTANT_NEGATIF"),
        (missing_score, "SCORE_FRAUDE_MANQUANT"),
        (invalid_score, "SCORE_FRAUDE_INVALIDE"),
        (missing_label, "CLASSIFICATION_MANQUANTE"),
        (invalid_label, "CLASSIFICATION_INVALIDE"),
    ]

    for condition, reason in checks:
        data.loc[condition, "rejection_reason"] += (
            reason + ";"
        )

    rejected = data[data["rejection_reason"] != ""].copy()
    accepted = data[data["rejection_reason"] == ""].copy()

    rejected["rejection_reason"] = (
        rejected["rejection_reason"].str.rstrip(";")
    )

    accepted = accepted.drop(columns=["rejection_reason"])

    output_file.parent.mkdir(parents=True, exist_ok=True)

    accepted.to_csv(output_file, index=False)

    rejected_file = output_file.with_name(
        f"{output_file.stem}_rejected{output_file.suffix}"
    )
    rejected.to_csv(rejected_file, index=False)

    return accepted, rejected
