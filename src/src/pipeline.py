import pandas as pd


def clean_data(input_file, output_file):
    """Nettoie les données de sinistres et sauvegarde le résultat."""

    df = pd.read_csv(input_file)

    # Suppression des lignes sans montant
    df = df.dropna(subset=["estimated_amount"])

    # Remplacement des valeurs manquantes du score de fraude
    df["fraud_score"] = df["fraud_score"].fillna(0)

    # Suppression des montants négatifs
    df = df[df["estimated_amount"] >= 0]

    # Sauvegarde des données nettoyées
    df.to_csv(output_file, index=False)

    return df


if __name__ == "__main__":
    clean_data(
        "data/raw/claims.csv",
        "data/processed/claims_clean.csv"
    )
