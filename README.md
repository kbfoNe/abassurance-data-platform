# AbAssurance Data Platform

## 1. Présentation du projet

Ce projet s'inscrit dans le cadre de la transformation numérique d'AbAssurance et de l'intégration des données issues de l'acquisition d'AssurePlus.

L'objectif est de mettre en place une plateforme permettant de consolider et d'exploiter les données issues des deux systèmes d'information afin de préparer les futurs traitements Data et d'intelligence artificielle.

Ce dépôt constitue la base de développement du projet. Il permet de structurer le code source, de gérer les versions et de définir les règles de collaboration avec Git.

## 2. Organisation des branches Git

Le projet utilise deux branches principales ainsi que des branches de travail temporaires.

### `main`

La branche `main` correspond à la version stable du projet.

- Elle contient les versions validées et fonctionnelles.
- Aucun développement direct n'est réalisé sur cette branche.
- Les modifications sont intégrées après validation.

### `develop`

La branche `develop` constitue la branche principale de développement.

- Elle centralise les développements en cours.
- Les branches de travail sont créées à partir de `develop`.
- Les fonctionnalités validées sont ensuite intégrées dans `develop`.

### Branches de travail

Les branches de travail sont temporaires et correspondent à une tâche précise du projet.

Elles sont créées à partir de `develop`, puis intégrées après vérification.

## 3. Convention de nommage

Le format utilisé est :

`<type>/<nom-de-la-tache>`

| Préfixe | Utilisation |
|---|---|
| `feature/` | Développement d'une fonctionnalité |
| `fix/` | Correction d'un bug |
| `test/` | Ajout ou modification de tests |
| `refactor/` | Amélioration du code |
| `docs/` | Modification de la documentation |

### Règles de nommage

- Les noms sont écrits en minuscules.
- Les mots sont séparés par des tirets.
- Les espaces et les underscores ne sont pas utilisés.
- Une branche correspond à une tâche précise.
- Les développements sont réalisés à partir de `develop`.

Exemples :

```text
feature/data-cleaning
feature/data-pipeline
feature/prediction-model
fix/data-validation
test/pipeline
docs/architecture
```

## 4. Structure du projet

```text
abassurance-data-platform/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── data/
│   ├── raw/
│   │   └── claims.csv
│   └── processed/
│
├── src/
│   ├── src/
│   │   ├── __init__.py
│   │   └── pipeline.py
│   └── main.py
│
├── tests/
│   └── test_main.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## 5. Fonctionnement du pipeline de nettoyage

Le pipeline assure le nettoyage et le contrôle qualité des données de sinistres.

Les principales étapes sont :

1. Lecture du fichier CSV source avec Pandas.
2. Vérification de la présence des colonnes obligatoires.
3. Détection des montants manquants ou négatifs.
4. Vérification de la présence et de la validité des scores de fraude.
5. Vérification de la classification des sinistres.
6. Séparation des données acceptées et rejetées.
7. Attribution d'un motif de rejet à chaque ligne non conforme.
8. Export des résultats dans deux fichiers CSV distincts.

Les données rejetées sont conservées avec leur motif de rejet afin de faciliter leur analyse et leur correction.

## 6. Technologies utilisées

| Technologie | Rôle |
|---|---|
| Python | Développement du pipeline |
| Pandas | Manipulation et nettoyage des données |
| Scikit-learn | Bibliothèque prévue pour les modèles de machine learning |
| Pytest | Tests unitaires |
| Pytest-cov | Mesure de la couverture des tests |
| Pylint | Analyse statique et qualité du code |
| Git et GitHub | Gestion des versions et collaboration |
| GitHub Actions | Automatisation des tests |

## 7. Installation

Prérequis : Python 3.10 ou supérieur.

Installer les dépendances depuis la racine du projet :

```bash
pip install -r requirements.txt
```

## 8. Exécution du pipeline

Depuis la racine du dépôt :

```bash
python -m src.main
```

Il est également possible de préciser les chemins des fichiers :

```bash
python -m src.main --input data/raw/claims.csv --output data/processed/claims_clean.csv
```

Le pipeline génère deux fichiers :

- `claims_clean.csv` : données acceptées.
- `claims_clean_rejected.csv` : données rejetées avec leurs motifs.

## 9. Tests et qualité du code

Les tests unitaires sont exécutés avec :

```bash
pytest -v
```

Pour mesurer la couverture des tests :

```bash
pytest --cov=src.src.pipeline --cov-report=term-missing
```

Pour analyser la qualité du code :

```bash
pylint src/
```

Les tests vérifient notamment :

- La séparation des sinistres acceptés et rejetés.
- Le rejet des scores de fraude invalides.
- La gestion des colonnes obligatoires manquantes.

## 10. Intégration continue

Le projet utilise GitHub Actions pour automatiser l'exécution des tests Python.

Le workflow permet de vérifier automatiquement le bon fonctionnement du code lors des événements configurés, notamment les mises à jour et les pull requests.

Cette automatisation contribue à détecter les erreurs avant l'intégration des modifications.

## 11. Gestion des versions

Les développements sont réalisés sur des branches dédiées. Après vérification et validation, les modifications sont intégrées dans `develop`, puis dans `main` lors d'une livraison stable.

Cette organisation facilite le suivi des modifications, la maintenance et la collaboration.
