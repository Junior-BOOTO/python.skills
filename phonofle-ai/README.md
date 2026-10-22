# PhonoFLE AI V1 · Écouter, distinguer, mieux prononcer

**BOOTO AI & DATA INNOVATION LAB**  

[![PhonoFLE AI — tests](https://github.com/Junior-BOOTO/python.skills/actions/workflows/phonofle-ai-tests.yml/badge.svg)](https://github.com/Junior-BOOTO/python.skills/actions/workflows/phonofle-ai-tests.yml)

**Vérification GitHub Actions du 22 octobre 2026 :** [exécution réussie](https://github.com/Junior-BOOTO/python.skills/actions/runs/39715399071) — tests Python, syntaxe et test de démarrage Streamlit sur Python 3.11 sous Ubuntu. Ces tests ne remplacent ni les essais phonétiques avec apprenants ni une validation sur des voix réelles.

[Voir la présentation trilingue du laboratoire](https://github.com/Junior-BOOTO/portfolio-fle/blob/main/projets/booto-ai-lab/index.html) — page HTML publiée sur GitHub, mais non encore intégrée au site professionnel externe.


**Auteur : Junior BOOTO Waba** · Français langue étrangère · A1 · PYP / cours privés

> **Statut : prototype pédagogique fonctionnel, non déployé et non validé en classe.** Le mot « AI » désigne ici la vision du laboratoire, pas une reconnaissance vocale déjà opérationnelle. Le moteur V1 utilise des règles explicites et des réponses de discrimination auditive. **Aucune évaluation automatique de la prononciation.**

## Quel problème résout le prototype ?

Pour des apprenants du français, distinguer **/y/** (« u ») et **/u/** (« ou ») à l'oral peut nécessiter des activités progressives. PhonoFLE AI V1 propose des oppositions phonologiques (paires minimales), une écoute de mots via la synthèse vocale du navigateur, un quiz de dix questions, une analyse des confusions, des conseils articulatoires et une grille d'observation orale complétée par l'enseignant. Il s'agit d'un outil **formatif** et non d'un diagnostic clinique.

### Ce qui fonctionne dans V1

- **11 paires minimales** relues au niveau orthographique et transcrites en API/IPA ; **10 questions** équilibrées entre /y/ et /u/.
- Démonstration HTML autonome avec interface **française et espagnole**, voix du navigateur, écoute ralentie, feedback, graphiques de réussite et export JSON anonyme.
- Moteur Python déterministe : génération d'un parcours, calcul des erreurs par phonème, recommandations explicables, évaluation manuelle de l'oral en 3 critères.
- Application Streamlit expérimentale, code disponible mais **démarrage Streamlit non validé dans ce présent environnement**.
- **28 tests unitaires réussis** sur le moteur et vérification de la syntaxe JavaScript avec Node.js (tests effectués lors de la création du pack).

### Ce qui n'est PAS implémenté

- Pas de microphone, enregistrement audio, reconnaissance automatique de parole ou analyse acoustique.
- Pas de note automatique de production orale ni de classification de l'accent.
- Pas de modèle de Machine Learning entraîné ; les recommandations sont des règles transparentes.
- Pas de collecte de données personnelles ni de compte élève ; la session HTML fonctionne en mémoire du navigateur.
- Pas de garantie sur l'accent de la voix de synthèse ; pour une évaluation sérieuse, valider les stimuli sonores avec un enseignant.

## Démarrage rapide : version HTML (sans Python)

Ouvrir **`demo/phonofle_ai_demo.html`** dans un navigateur récent. Cliquer sur **Commencer**. Activer une voix française dans le système/navigateur si elle n'est pas disponible. Certains navigateurs ou environnements restreignent les fonctions vocales en local : dans ce cas, l'enseignant peut lire les mots, ou le fichier peut être servi par un serveur local.

## Démarrage de la version Python

```bash
cd PhonoFLE_AI_V1
python -m venv .venv
# Windows PowerShell : .venv\Scripts\Activate.ps1
# macOS / Linux : source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app/main.py
```

Démonstration en ligne de commande sans Streamlit (bibliothèque standard Python) :

```bash
python scripts/run_demo.py
```

## Structure du projet

```text
app/main.py                   Prototype Streamlit
src/phonofle/engine.py        Diagnostic explicable et grille orale
data/minimal_pairs.json       Corpus didactique de 11 oppositions /y/–/u/
demo/phonofle_ai_demo.html    Démonstration interactive sans serveur
tests/test_engine.py          28 tests unitaires du moteur
tests/browser_smoke.py        Test navigateur facultatif (Playwright)
docs/                        Cahier des charges, protocole, feuille de route
scripts/run_demo.py           Exemple CLI sans données d'élèves
```

## Critères observables « Je peux… »

- **Je peux** entendre la différence entre /y/ et /u/ dans des mots isolés.
- **Je peux** choisir le bon mot après une écoute guidée.
- **Je peux** répéter quelques mots en appliquant une aide articulatoire.

Le quiz mesure les deux premiers en situation guidée ; le troisième nécessite **l'observation d'un enseignant**. Ces critères s'inspirent de l'approche actionnelle, mais les scores n'ont pas valeur de certification CECRL.

## Limites méthodologiques et confidentialité

La voix vient de l'API **Web Speech / SpeechSynthesis** du navigateur : la présence d'une voix française, la prononciation, et le recours éventuel à un service distant dépendent de l'appareil et du fournisseur de voix. **Le prototype ne transmet pas volontairement les réponses à un serveur**, mais ne garantit pas que le moteur vocal du navigateur soit strictement hors ligne. Ne pas utiliser de données ou d'enregistrements d'élèves dans cette V1. Le fichier exporté contient les réponses aux dix items et aucun identifiant nominatif.

Le HTML n'exige aucune bibliothèque externe ; les pictogrammes sont de simples formes SVG dessinées pour le projet. Les tests fonctionnels du navigateur et la validité des stimulations auditives nécessitent encore une revue sur des appareils courants. Aucune licence de redistribution n'est accordée par défaut : à définir avant une publication sous licence libre.

## Documentation

[**Cahier des charges**](docs/CAHIER_DES_CHARGES_V1.md) · [**Protocole pédagogique et de validation**](docs/PROTOCOL_EVALUATION.md) · [**Feuille de route**](docs/FEUILLE_DE_ROUTE.md)

### Référence technique

[MDN · SpeechSynthesis](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis) · [MDN · `speak()`](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/speak)
