# BOOTO FLE Adaptive AI — V1 (prototype pédagogique)

**FLE + Python · Grade 4 · A1 · PYP « Qui nous sommes »**

> **Prototype original de différenciation formative, basé sur des règles explicites.** Ce projet ne constitue pas un modèle d'apprentissage automatique, un diagnostic CECRL certifié ou une efficacité pédagogique démontrée. Les douze profils du tableau de bord sont **entièrement synthétiques**.

## Problème et proposition

Les élèves de FLE de niveau A1 ne maîtrisent pas tous les mêmes éléments d'une leçon sur « Ma journée typique ». L'enseignant a besoin de relier les traces observées à des exercices ciblés, tout en comprenant **pourquoi** un exercice est conseillé.

**BOOTO FLE Adaptive AI V1** analyse les réponses à 12 questions de routine quotidienne réparties entre **vocabulaire**, **verbes pronominaux avec je**, **connecteurs temporels** et **heures à/vers**. Le système intègre facultativement une **observation orale saisie par un enseignant**. Il propose ensuite jusqu'à trois micro-activités de remédiation, avec raison explicite, durée, étayage et critère de réussite.

## Fonctions effectivement implémentées

| Fonction | V1 |
| --- | --- |
| Quiz formatif de 12 QCM en français | ✓ |
| Diagnostic pour 4 compétences écrites | ✓ — 3 questions par compétence |
| Saisie facultative d'une observation orale | ✓ — humaine, non automatique |
| Recommandations ciblées et explicables | ✓ — moteur de règles |
| Parcours de différenciation : aide et enrichissement | ✓ — catalogue de cinq micro-activités |
| Corrigé détaillé | ✓ |
| Tableau de bord enseignant sur 12 profils fictifs | ✓ |
| Traitement local, sans base nominative ni API externe | ✓ |
| Évaluation orale automatique | **Non** |
| Reconnaissance vocale, images interactives, analyse de production écrite | **Non** |
| Apprentissage automatique, adaptation en continu, validation réelle | **Non** |

## Démonstration immédiate sans installation

**[Ouvrir `demo/BOOTO_FLE_Adaptive_AI_Demo.html`](demo/BOOTO_FLE_Adaptive_AI_Demo.html)** dans un navigateur local après extraction du ZIP. Cette page autonome contient une démonstration interactive en JavaScript du même principe de règles : questionnaire, recommandations et tableau de bord sur profils synthétiques. Elle ne nécessite ni Python ni connexion Internet. **La logique applicative de référence reste le moteur Python** ; la démonstration HTML dispose d'une implémentation autonome de ces règles pour faciliter la présentation dans un portfolio.

## Installation et lancement

Python **3.11 ou 3.12** recommandé. Ouvrir un terminal **dans ce dossier**.

```bash
python -m venv .venv
# Windows PowerShell : .venv\Scripts\Activate.ps1
# macOS/Linux : source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app/main.py
```

L'interface s'ouvre dans le navigateur local. Elle propose trois espaces : **Apprenant**, **Enseignant — classe fictive**, **Méthode et limites**.

Pour tester uniquement le moteur **sans installer Streamlit**, depuis la racine du projet :

```bash
python scripts/run_demo.py
```

Pour lancer les tests (pytest requis) :

```bash
python -m pip install pytest
python -m pytest -q
```

## Décisions pédagogiques et critères « Je peux… »

- **Je peux** reconnaître les activités de ma routine et comprendre leur signification.
- **Je peux** construire des phrases courtes avec « je me lève », « je me prépare » et « je me couche ».
- **Je peux** organiser ma journée avec « le matin », « ensuite » et « enfin ».
- **Je peux** indiquer une heure exacte avec « à » ou approximative avec « vers ».
- **Je peux** présenter ma journée en trois phrases et donner une heure — **observé par l'enseignant**, non noté automatiquement.

Une compétence écrite est qualifiée **« acquis (sur ces tâches) »** pour 2 ou 3 bonnes réponses sur 3, **« en cours »** pour 1/3 et **« à renforcer »** pour 0/3. Une compétence avec au moins une réponse manquante est **« non évaluée »** et aucune conclusion de niveau n'en est tirée. Il s'agit de **règles de démonstration**, pas de seuils officiels du CECRL.

Les activités proposées suivent les besoins détectés (à renforcer avant en cours), avec une explication inspectable.

## Structure du code

```text
app/main.py                      Interface Streamlit
src/booto_fle/engine.py          Validation, diagnostic, recommandations, agrégations
data/quiz_routine_a1.json        12 questions originales A1
data/activities_a1.json          5 micro-activités différenciées
data/profils_synthetiques.json   12 profils fictifs explicitement signalés
scripts/run_demo.py             Démonstration sans interface
tests/test_engine.py             Tests de non-régression
pyproject.toml                  Configuration pytest
docs/CAHIER_DES_CHARGES_V1.md   Objectifs, public, critères de réussite
docs/ARCHITECTURE.md            Architecture et décisions techniques
docs/ETHIQUE_ET_VALIDATION.md   Précautions, validation, limites
```

## Confidentialité et intégrité des résultats

Aucune identité d'élève réel n'est nécessaire ou acceptée par le tableau de bord de classe fictive. Les réponses du quiz sont évaluées au cours de la session Streamlit ; elles ne sont pas sauvegardées dans un fichier ou envoyées à une API par le code de ce projet. Un hébergement tiers, s'il est utilisé ultérieurement, aurait ses propres conditions et journaux : **ne pas entrer de données personnelles dans une démonstration publique**.

Les supports images permettant d'associer six activités à des photos, la validation orale et le suivi longitudinal demandent une **phase 2** de conception et une évaluation pédagogique indépendante.

## Auteur et statut

**Junior BOOTO Waba** — Enseignement du FLE, ingénierie pédagogique, Python & Data Science. Prototype de portfolio, daté du **21 octobre 2026**. Licence de redistribution **à définir avant publication externe**.
