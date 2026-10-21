# Guide de publication GitHub — BOOTO NLP LAB

**Préparation du 21 octobre 2026 — dépôt cible : `Junior-BOOTO/BOOTO-NLP-LAB`.**

## 1. État de publication

Le dépôt `Junior-BOOTO/BOOTO-NLP-LAB` **n'existait pas lors de la vérification** du 21 octobre 2026. Les fichiers ont été préparés localement ; **aucune publication sur GitHub n'a été effectuée**.

Le nom conseillé est **BOOTO-NLP-LAB**. Description recommandée :

> Multilingual NLP & Data Science laboratory | Python, machine learning and interactive text analytics (French · English · Spanish). Experimental prototype.

Sujets GitHub recommandés : `python`, `nlp`, `data-science`, `machine-learning`, `streamlit`, `multilingual`, `text-classification`, `portfolio`.

## 2. Créer un dépôt vide

1. Connectez-vous sur GitHub avec le compte `Junior-BOOTO`.
2. Cliquez sur **New repository**.
3. Nom : `BOOTO-NLP-LAB`.
4. Pour tester avant exposition publique, choisissez **Private** initialement ; vous pourrez modifier la visibilité ensuite.
5. Ne préremplissez pas le dépôt avec un README, `.gitignore` ou une licence : les fichiers sont déjà inclus dans le dossier local, sauf la licence, qui reste à choisir.
6. Validez **Create repository**.

## 3. Publier avec Git (depuis l'ordinateur)

Après avoir extrait le ZIP, ouvrez un terminal dans le dossier contenant `README.md` (le dossier `BOOTO-NLP-LAB`), puis exécutez :

```bash
git init
git branch -M main
git add .
git commit -m "Initialize BOOTO NLP LAB V1 experimental prototype"
git remote add origin https://github.com/Junior-BOOTO/BOOTO-NLP-LAB.git
git push -u origin main
```

**Prérequis :** Git est installé, et l'authentification au compte GitHub est configurée. Si la branche a déjà été initialisée ou si le dossier contient un dépôt Git, vérifiez `git status` et `git remote -v` avant de réutiliser les commandes. Ne forcez pas une publication sur un dépôt qui contient déjà des travaux.

**Alternative :** utiliser GitHub Desktop : *File > Add local repository* (ou *Create repository* dans le dossier), puis *Publish repository*. GitHub ne décompresse pas automatiquement un fichier ZIP envoyé comme un fichier unique.

## 4. Vérifications après mise en ligne

- Vérifier la présence de `README.md`, `app/main.py`, `src/booto_nlp/`, `tests/`, `docs/` et `data/sample/`.
- Vérifier dans **Actions** que le workflow `Tests Python` réussit.
- Installer localement les dépendances de `requirements.txt` et lancer l'interface Streamlit.
- Ne pas annoncer les seuils de 95 % ou de macro-F1 ≥ 0,75 comme atteints sur données réelles avant validation indépendante.
- Choisir une **licence explicite** avant de permettre la réutilisation par des tiers.
- Vérifier qu'aucun secret, donnée sensible ou fichier personnel n'a été publié.

## 5. Présentation dans le portfolio

**Titre :** BOOTO NLP LAB — Multilingual Text Analyzer (V1 — prototype)

**Description française :**

> Prototype d'application Python pour explorer des corpus textuels en français, anglais et espagnol. Il comprend import CSV, contrôle des données, détection linguistique expérimentale, extraction TF-IDF, classification thématique, similarité et tableau de bord Streamlit. Un corpus synthétique de 300 textes et des tests automatiques documentent la démonstration ; les performances sur données réelles restent à mesurer.

**English description:**

> Experimental Python application for multilingual text analytics in French, English and Spanish. Features include CSV ingestion, exploratory language detection, TF-IDF keyword extraction, topic classification, cosine similarity, and a Streamlit dashboard. The 300-text synthetic demo and automated tests are provided; real-world performance has not yet been validated.

**Descripción en español:**

> Prototipo experimental en Python para analizar textos en francés, inglés y español. Incluye importación CSV, detección exploratoria de idiomas, extracción de palabras clave con TF-IDF, clasificación temática, similitud coseno y panel interactivo con Streamlit. Incluye 300 textos sintéticos y pruebas automatizadas; su rendimiento con datos reales todavía no está validado.

L'ajout au profil GitHub et au site web s'effectuera **après** création effective du dépôt et vérification de son contenu.
