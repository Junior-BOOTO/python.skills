# Cahier des charges — BOOTO NLP LAB V1

**21 octobre 2026 | Version de cadrage initiale**

## Mission

Concevoir un analyseur de textes interactif et reproductible pour le français, l'anglais et l'espagnol, destiné aux analystes, chercheurs, enseignants et évaluateurs techniques du portfolio.

## Fonctionnalités obligatoires

- F01 : import UTF-8 CSV (colonne `text`), aperçu, gestion des textes vides.
- F02 : détecter le français, l'anglais, l'espagnol ou signaler `unknown`.
- F03 : normaliser et tokeniser, filtrer les mots vides, puis lemmatiser selon modèle disponible.
- F04 : extraire 10 mots-clés TF-IDF.
- F05 : classifier en éducation, technologie et environnement.
- F06 : identifier 3 textes similaires à partir du cosinus TF-IDF.
- F07 : présenter répartition langues, thèmes et indicateurs de qualité.
- F08 : exporter un CSV comprenant ID, original, prédictions, statut.
- F09 : gérer les erreurs de fichiers et modèles.
- F10 : documenter entraînement/test, métriques et reproductibilité.

## Contraintes

Python 3.11–3.12, interface Streamlit, environnement local compatible avec 8 Go de RAM, sans GPU requis ; outils libres ou gratuits ; limitation fichiers UI 5 Mo et pas de transmission des documents à une API tierce.

## Critères de réussite visés

- Import de 300 documents courts.
- Exactitude de détection linguistique >= 95 % sur 60 textes indépendants.
- Classification macro-F1 >= 0,75 sur test indépendant.
- Trois voisins textuels accessibles ; 10 mots-clés affichés.
- Export valide et gestion des erreurs.
- Analyse de 300 textes <=2 000 caractères en moins de 30 s (modèles déjà chargés, PC 8 Go).
- Tests obligatoires verts ; installation et métriques reproductibles.

**Important** : ce cahier des charges décrit les objectifs de validation de V1. Le code présent dans le dépôt est pour l'instant un **prototype préparatoire** ; il n'atteint pas automatiquement l'ensemble des critères ci-dessus.
