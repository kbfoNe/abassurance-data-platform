
"""Nettoyage et contrôle qualité des données de sinistres."""

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = ["estimated_amount", "fraud_score"]


def clean_data(input_file, output_file):
    """Nettoie les sinistres et conserve les motifs de rejet."""

    input_path = Path(input_file)
    output_path = Path(output_file)
    rejected_path = output_path.with_name(
        f"{output_path.stem}_rejected.csv"
    )

    if not input_path.exists():
        raise FileNotFoundError(
            f"Fichier source introuvable : {input_path}"
        )

    df = pd.read_csv(input_path)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Colonnes obligatoires manquantes : {missing_columns}"
        )

    df["rejection_reason"] = ""

    # Vérification des montants manquants ou négatifs.
    missing_amount = df["estimated_amount"].isna()
    negative_amount = df["estimated_amount"] < 0

    df.loc[missing_amount, "rejection_reason"] = "MONTANT_MANQUANT"
    df.loc[negative_amount, "rejection_reason"] = "MONTANT_NEGATIF"

    # Détection des doublons.
    duplicates = df.duplicated(keep="first")
    df.loc[
        duplicates & df["rejection_reason"].eq(""),
        "rejection_reason"
    ] = "DOUBLON"

    # Séparation des données acceptées et rejetées.
    rejected = df[df["rejection_reason"] != ""].copy()
    accepted = df[df["rejection_reason"] == ""].copy()

    # Remplacement du score de fraude manquant.
    accepted["fraud_score"] = (
        accepted["fraud_score"].fillna(0)
    )

    # Création des dossiers de sortie.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Export des résultats.
    accepted.drop(columns=["rejection_reason"]).to_csv(
        output_path, index=False
    )
    rejected.to_csv(rejected_path, index=False)

    print(f"Sinistres acceptés : {len(accepted)}")
    print(f"Sinistres rejetés : {len(rejected)}")

    return accepted, rejected


if __name__ == "__main__":
    clean_data(
        "data/raw/claims.csv",
        "data/processed/claims_clean.csv"
    )

