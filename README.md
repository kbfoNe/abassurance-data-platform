# AbAssurance Data Platform

## Presentation 

Ce projet s'inscrit dans le cadre de la transformation numérique
d'AbAssurance et de l'intégration des données issues de l'acquisition
d'AssurePlus.

L'objectif est de mettre en place une plateforme permettant de
consolider et d'exploiter les données issues des deux systèmes
d'information afin de préparer les futurs traitements Data et
d'intelligence artificielle.

Ce repository constitue la base de développement du projet. Il permet
également de structurer le code, de gérer les versions et de définir
les règles de collaboration avec Git.

---

Organisation des branches 

Le projet utilise deux branches principales ainsi que des branches de
travail temporaires.

### `main`

La branche `main` correspond à la version stable du projet.

- Elle contient uniquement les versions validées et fonctionnelles.
- Aucun développement direct n'est réalisé sur cette branche.
- Les modifications sont intégrées après validation.

### `develop`

La branche `develop` correspond à la branche principale de développement.

- Elle permet d'intégrer les développements en cours.
- Les branches de travail sont créées à partir de `develop`.
- Les fonctionnalités validées sont ensuite intégrées dans `develop`.

Branches de travails

Les branches de travail sont temporaires et correspondent à une tâche
précise du projet.

Elles sont créées à partir de `develop` puis intégrées dans `develop`
après validation.

---

convention de nommage 

Le format utilisé est :

`<type>/<nom-de-la-tache>`


|---|---|
| `feature/` | Développement d'une nouvelle fonctionnalité |
| `fix/` | Correction d'un bug |
| `test/` | Ajout ou modification de tests |
| `refactor/` | Amélioration du code sans modification fonctionnelle |
| `docs/` | Création ou modification de documentation |

regle de nommage 

- Les noms de branches sont écrits en minuscules.
- Les mots sont séparés par des tirets `-`.
- Les espaces et les underscores ne sont pas utilisés.
- Une branche correspond à une tâche précise.
- Les développements sont réalisés à partir de `develop`.
- La branche `main` contient uniquement les versions stables.

exemple 

```text
feature/data-cleaning
feature/data-pipeline
feature/prediction-model
fix/data-validation
test/pipeline
docs/architecture
