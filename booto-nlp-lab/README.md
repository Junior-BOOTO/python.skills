# BOOTO NLP LAB — Version 1.0 (prototype technique)

**Multilingual Text Analyzer | Français · English · Español**

> **État : prototype initial, pas une V1 validée.** Ce dépôt fournit le socle technique et une démonstration expérimentale. Les seuils du cahier des charges ne sont pas encore certifiés sur un jeu de données réel indépendant.

## Objectif
Importer des textes CSV, contrôler leur qualité, détecter leur langue (FR/EN/ES), extraire des mots-clés, classer les documents (éducation, technologie, environnement), comparer leur similarité TF-IDF et exporter les résultats.

## Démarrage (Windows / macOS / Linux)

Exécuter avec **Python 3.11 ou 3.12** :

```bash
python -m venv .venv
# Windows PowerShell : .venv\Scripts\Activate.ps1
# macOS / Linux : source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app/main.py
```

Le navigateur ouvre l'application Streamlit. Charger `data/sample/corpus_300_demo.csv` pour découvrir le fonctionnement.

Pour une démonstration sans Streamlit (Python + pandas + scikit-learn) :

```bash
python scripts/run_demo.py
```

## Format du CSV

Une colonne `text` est **obligatoire** ; `document_id`, `language`, `category` sont facultatives (ces deux dernières désignent des étiquettes de référence). Encodage UTF-8, 5 Mo maximum dans l'interface. Les langues hors FR/EN/ES ne sont pas prises en charge.

```csv
document_id,text
1,"Les élèves étudient les langues à l'école."
2,"Software engineers build secure systems."
3,"El bosque necesita protección y conservación."
```

## Statut des fonctions

| Fonction | État du prototype |
|---|---|
| CSV, validation des champs, gestion d'erreurs | Implémenté |
| Détection linguistique | `langid` si disponible, sinon heuristique de démonstration (non certifiée) |
| Normalisation, tokenisation, mots vides | Implémenté |
| Lemmatisation par modèles linguistiques | Non implémentée (étape suivante) |
| Extraction de mots-clés TF-IDF | Implémenté |
| Classification supervisée TF-IDF + régression logistique | Implémenté, entraîné sur données synthétiques |
| Similarité cosinus TF-IDF | Implémenté, **non sémantique translingue** |
| Dashboard et export CSV | Implémenté via Streamlit (non testé ici) |
| Validation externe 95 % langue / macro-F1 >= 0,75 | **À réaliser sur corpus indépendant** |

## Données

Le jeu `data/sample/corpus_300_demo.csv` contient **300 textes synthétiques construits uniquement pour faire fonctionner la démonstration** : 100 FR / 100 EN / 100 ES, répartis entre trois thèmes. Les formulations artificielles et motifs répétitifs rendent les scores artificiellement optimistes ; **ne pas utiliser ces scores comme mesure de performance réelle**. Aucun texte réel d'élève n'est inclus.

## Structure

```text
app/main.py                Tableau de bord Streamlit
src/booto_nlp/             Traitements réutilisables
data/sample/               Corpus synthétique de démonstration
scripts/run_demo.py        Exécution locale en ligne de commande
tests/                     Tests automatiques
docs/                      Architecture, protocole d'évaluation, cahier des charges
```

## Architecture, évaluation et publication

Lire `docs/ARCHITECTURE.md`, `docs/PLAN_DE_TESTS.md` et `docs/CAHIER_DES_CHARGES_V1.md`.

Pour mettre ce prototype dans un nouveau dépôt GitHub dédié : `docs/GUIDE_PUBLICATION_GITHUB.md`. Le statut des vérifications et les travaux restant à effectuer sont dans `docs/ETAT_ET_PROCHAINES_ETAPES.md`.

## Déploiement Streamlit Community Cloud

Le code du prototype est **préparé pour le déploiement**, mais aucune URL publique d'application n'est encore validée. Consultez [le guide de déploiement](docs/DEPLOIEMENT_STREAMLIT.md) ; dépôt `Junior-BOOTO/python.skills`, branche `main`, point d'entrée `booto-nlp-lab/app/main.py`, Python 3.11. Les dépendances cloud sont déclarées dans `app/requirements.txt`. Les tests automatiques du dépôt monorepo sont définis à la racine, sous `.github/workflows/booto-nlp-lab-tests.yml`.

## Confidentialité et licences

Pas de transmission automatique à une API distante par le cœur applicatif. Ne pas charger de données personnelles sans droits et protections adéquats. Vérifier les licences des jeux de données externes. **Licence du projet à déterminer avant publication publique.**

## Auteur / portefeuille

Projet de portfolio de **Junior BOOTO Waba** — Pôle Python & Data Science ; les futures extensions FLE constituent un autre module du laboratoire.
