# Python et analyse de données · Junior BOOTO Waba
**Apprentissage documenté · Scripts et notebooks · Applications pédagogiques**

Je développe mes compétences en Python et en analyse de données. Ce dépôt distingue les exercices d’apprentissage, un démonstrateur sur données fictives et une structure d’analyse RH dont les données originales ne sont pas disponibles.

[Profil et CV](https://github.com/Junior-BOOTO) · [English profile](https://github.com/Junior-BOOTO/Junior-BOOTO/blob/main/README.en.md) · [Portfolio FLE](https://github.com/Junior-BOOTO/portfolio-fle)

## Projets à examiner

| Projet | Contenu | Limites |
| --- | --- | --- |
| [FLE Learning Analytics](fle-learning-analytics/README.md) | Génération de données synthétiques, analyse des quatre compétences, graphique et étude de cas pédagogique. | Démonstration fictive ; aucune efficacité pédagogique réelle mesurée. |
| [Analyse exploratoire des performances](employee-performance-analysis/README.md) | Script, notebook, statistiques descriptives et détection IQR des valeurs atypiques. | CSV original absent ; résultats RH non établis. |

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
