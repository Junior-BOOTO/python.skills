# BOOTO NLP LAB — statut de mise en publication

**Date : 21 octobre 2026**

## Vérifications réalisées localement

- `python -m pytest -q` : **13 tests réussis** (environnement Python 3.13.5 du prototype).
- `python scripts/run_demo.py` : exécuté avec **300 textes synthétiques**.
- Présence vérifiée : documentation, interface Streamlit, modules Python, jeu de données, workflow GitHub Actions.

## Points ouverts avant validation d'une V1 complète

- **Pas de dépôt GitHub créé ni de contenu publié à cette date.**
- L'interface Streamlit n'a pas été exécutée dans l'environnement de préparation (dépendance absente).
- L'évaluation de la détection linguistique avec `langid` reste à exécuter.
- Les scores de classification obtenus sur données synthétiques sont **non généralisables**.
- Lemmatisation absente du prototype.
- Licence du projet : à choisir avant d'autoriser explicitement la réutilisation.
- Les critères d'acceptation du cahier des charges demandent encore une validation indépendante.

## Séquence recommandée

1. Créer le dépôt GitHub dédié en mode privé et envoyer les sources.
2. Faire exécuter les tests via GitHub Actions.
3. Exécuter l'interface Streamlit sur un poste disposant des dépendances complètes.
4. Construire un corpus réel autorisé, puis évaluer le modèle sur des données indépendantes.
5. Définir la licence, la présentation du projet et le niveau de visibilité public.
6. Ajouter la référence du dépôt dans les sections Python & Data Science du portfolio.
