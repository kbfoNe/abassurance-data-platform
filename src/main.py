
"""Point d'entrée de la plateforme AbAssurance Data Platform."""

import argparse

from pathlib import Path

from src.src.pipeline import clean_data


def main():
    """Exécute le nettoyage des données de sinistres."""

    parser = argparse.ArgumentParser(
        description="Pipeline de traitement des sinistres."
    )

    parser.add_argument(
        "--input",
        default="data/raw/claims.csv",
        help="Chemin du fichier CSV source."
    )

    parser.add_argument(
        "--output",
        default="data/processed/claims_clean.csv",
        help="Chemin du fichier CSV nettoyé."
    )

    args = parser.parse_args()

    try:
        accepted, rejected = clean_data(
            args.input,
            args.output
        )

        print("\nTraitement terminé.")
        print(f"Fichier généré : {Path(args.output)}")
        print(f"Sinistres acceptés : {len(accepted)}")
        print(f"Sinistres rejetés : {len(rejected)}")

    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
