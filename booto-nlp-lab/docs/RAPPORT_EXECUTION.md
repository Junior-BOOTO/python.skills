# Rapport d'exécution local — 21 octobre 2026

- Environnement : Python 3.13.5, Linux.
- Commande : `python -m pytest -q`.
- Résultat : **13 tests réussis** (tests de programmation et de cohérence des données synthétiques).
- Démonstration CLI : exécutée sur 300 textes **synthétiques**.
- Mesure macro-F1 du classifieur sur ces textes artificiels : 1,00 ; **ne démontre aucune performance sur des textes réels** (risque de surévaluation par motifs répétitifs).
- Modules `langid` et `streamlit` : non disponibles dans l'environnement de test ; interface graphique et détection `langid` non exécutées.
- Tests d'acceptation finaux : **non réalisés**.
