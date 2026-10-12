# Python et analyse de données · Junior BOOTO Waba
**Apprentissage documenté · Scripts et notebooks · Applications pédagogiques**

Je développe mes compétences en Python et en analyse de données. Ce dépôt distingue les exercices d’apprentissage, un démonstrateur sur données fictives et une structure d’analyse RH dont les données originales ne sont pas disponibles.

[Profil et CV](https://github.com/Junior-BOOTO) · [English profile](https://github.com/Junior-BOOTO/Junior-BOOTO/blob/main/README.en.md) · [Portfolio FLE](https://github.com/Junior-BOOTO/portfolio-fle)

## Projets à examiner

| Projet | Contenu | Limites |
| --- | --- | --- |
| [California Housing — Régression](california-housing-regression/README.md) | Régressions linéaires, Ridge, test géographique et analyse des erreurs. | Valeurs médianes de zones en 1990 ; plafond de cible et estimations négatives signalés. |
| [Mall Customers — Clustering](mall-customer-clustering/README.md) | Comparaison K-means/Ward/DBSCAN, stabilité, export numérique et simulateur. | 200 profils pédagogiques ; groupes exploratoires sans validation commerciale indépendante. |
| [AdventureWorks — SQL avancé](adventureworks-sql/README.md) | 14 exercices calculés, 3 bonus, vues, segmentation et fonctions de fenêtre. | Adaptation SQLite ; retours non calculables et marge standard estimée documentés. |
| [Global Superstore — Tableau de bord](global-superstore-dashboard/README.md) | Filtres interactifs, KPI commerciaux, préparation Python et exports BI. | Données fictives historiques 2011–2014 ; version web, sans flux temps réel. |
| [Wine Quality — ACP](wine-quality-acp/README.md) | Analyse de 6 497 vins, ACP sur 11 variables, graphiques et parcours Python coordonné. | ACP descriptive ; 50,2 % de variance en 2D, sans prédiction ni données clients. |
| [Chinook — SQL et Python](chinook-sql/README.md) | 26 exercices SQL, résultats CSV, rapport et script Python reproductible. | Base de démonstration ; adaptation documentée des années des exercices. |
| [FLE Learning Analytics](fle-learning-analytics/README.md) | Génération de données synthétiques, analyse des quatre compétences, graphique et étude de cas pédagogique. | Démonstration fictive ; aucune efficacité pédagogique réelle mesurée. |
| [Analyse exploratoire des performances](employee-performance-analysis/README.md) | Script, notebook, statistiques descriptives et détection IQR des valeurs atypiques. | CSV original absent ; résultats RH non établis. |

## Mes assistants IA pour les données

[DataCollect, DataAnalyse et DataML](assistants-ia/README.md) : trois assistants spécialisés pour la collecte, l’analyse et le machine learning. Présentations, liens ChatGPT, livrables et limites d’accès. Transmission manuelle entre assistants ; validation sur un projet de démonstration à documenter.

## Bibliothèque de références

[Vingt ouvrages Python, analyse des données et data science](bibliotheque/README.md), organisés par domaine avec des objectifs de lecture et des liens officiels. [Sélection sur mon site](https://junior-booto-fle.juniorbooto.chatgpt.site/bibliographie-python.html).

## Carnets d’apprentissage

| Notebook | Parcours indiqué |
| --- | --- |
| [Bases de Python](Exercices_de_python_les_bases.ipynb) | Exercices de découverte du langage |
| [Pandas](Pandas.ipynb) | Exploration de la manipulation de données |
| [Scikit-learn](sklearn.ipynb) | Exploration des outils d’apprentissage automatique |

La présence d’un notebook ne constitue pas une certification de maîtrise. Les environnements et données nécessaires aux trois carnets restent à préciser.

## Reproduire le démonstrateur FLE

Depuis la racine du dépôt, avec Python 3.10 ou plus récent et un environnement virtuel activé :

```bash
python -m pip install -r fle-learning-analytics/requirements.txt
python fle-learning-analytics/generate_data.py
python fle-learning-analytics/analyze.py
```

Les scripts écrivent les données fictives et les résultats dans le dossier du projet. Ils régénèrent les fichiers de démonstration. [Lire le dictionnaire de données et les limites](fle-learning-analytics/README.md).

## Progression et documentation

- [Formations Python, données et IA](certifications-python-data.md).
- [Modèle de README de projet](templates/README-PYTHON.md).
- Prochaines étapes : documenter les environnements des carnets, préciser la provenance et les droits des données, ajouter des résultats uniquement après exécution vérifiée.
- Les données d’élèves et les données RH confidentielles ne sont pas des ressources publiques de ce portfolio.

### Parcours coordonné exécuté
Le projet [Wine Quality — ACP](wine-quality-acp/README.md) réunit préparation, exploration et réduction de dimension dans un script Python et un dossier partagé. Les résultats et contrôles ont été exécutés ; ce parcours ne contacte pas automatiquement les trois GPT indépendants.
