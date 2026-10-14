# Python et analyse de données · Junior BOOTO Waba
**Apprentissage documenté · Scripts et notebooks · Applications pédagogiques**

Je développe mes compétences en Python et en analyse de données. Ce dépôt réunit des projets exécutés et documentés sur des données publiques ou fictives, un démonstrateur pédagogique FLE et une structure d’analyse RH dont les données originales ne sont pas disponibles.

[Profil et CV](https://github.com/Junior-BOOTO) · [English profile](https://github.com/Junior-BOOTO/Junior-BOOTO/blob/main/README.en.md) · [Portfolio FLE](https://github.com/Junior-BOOTO/portfolio-fle)

## Projets à examiner

| Projet | Contenu | Limites |
| --- | --- | --- |
| [MessageLens — NLP explicable](messagelens/README.md) | Spam SMS, groupes de similarité, contributions des mots et inférence navigateur ; 17 tests. | Anglais historique : 166/178 spams détectés, 13 faux positifs ; pas preuve de fraude. |
| [SourceWatch — veille documentée](sourcewatch/README.md) | RSS Python Insider, provenance, classement explicable, snapshots ; 25 tests locaux. | 20 entrées réelles sur 50 ; comparaison de changements fictifs, sans veille permanente. |
| [Document-to-Data Lab — extraction et qualité](document-to-data-lab/README.md) | Tableaux PDF/CSV, provenance, anomalies et totaux par devise ; 22 tests locaux. | Démo fictive : 9 lignes, 5 acceptées ; OCR absent, PDF texte à bordures. |
| [Bitcoin DataLab — collecte et prévision](bitcoin-datalab/README.md) | Historique Bitstamp, contrôles qualité, Ridge et forêt, test chronologique et modèles exportés. | 1 967 jours (2021–mai 2026) ; Ridge moins bon que cours inchangé sur test. |
| [API météo Bogotá — Analyse et modèle](api-open-meteo/README.md) | Collecte HTTP, contrôles, analyse et modèle Ridge à J+1, parcours coordonné reproductible. | Réanalyse ERA5 2025 ; MAE test 0,340 °C, pas validation de prévision opérationnelle. |
| [Superstore — Analyse bivariée](superstore-bivariate/README.md) | Tableaux croisés, distributions et corrélations entre catégories, marchés, remises et bénéfices. | Données fictives ; associations descriptives, sans conclusion causale. |
| [Prévision des ventes — Séries temporelles](sales-time-series/README.md) | Références saisonnières, SARIMA, validation glissante et test chronologique. | 48 mois fictifs ; prolongement 2015 non évalué, pas prévision actuelle. |
| [Défaut de paiement — Classification](credit-default-classification/README.md) | Régression logistique, calibration et compromis de seuil sur résultats agrégés. | Historique Taïwan 2005 ; aucune décision individuelle de crédit. |
| [California Housing — Régression](california-housing-regression/README.md) | Régressions linéaires, Ridge, test géographique et analyse des erreurs. | Valeurs médianes de zones en 1990 ; plafond de cible et estimations négatives signalés. |
| [Mall Customers — Clustering](mall-customer-clustering/README.md) | Comparaison K-means/Ward/DBSCAN, stabilité, export numérique et simulateur. | 200 profils pédagogiques ; groupes exploratoires sans validation commerciale indépendante. |
| [AdventureWorks — SQL avancé](adventureworks-sql/README.md) | 14 exercices calculés, 3 bonus, vues, segmentation et fonctions de fenêtre. | Adaptation SQLite ; retours non calculables et marge standard estimée documentés. |
| [Global Superstore — Tableau de bord](global-superstore-dashboard/README.md) | Filtres interactifs, KPI commerciaux, préparation Python et exports BI. | Données fictives historiques 2011–2014 ; version web, sans flux temps réel. |
| [Wine Quality — ACP](wine-quality-acp/README.md) | Analyse de 6 497 vins, ACP sur 11 variables, graphiques et parcours Python coordonné. | ACP descriptive ; 50,2 % de variance en 2D, sans prédiction ni données clients. |
| [Chinook — SQL et Python](chinook-sql/README.md) | 26 exercices SQL, résultats CSV, rapport et script Python reproductible. | Base de démonstration ; adaptation documentée des années des exercices. |
| [FLE Learning Analytics](fle-learning-analytics/README.md) | Génération de données synthétiques, analyse des quatre compétences, graphique et étude de cas pédagogique. | Démonstration fictive ; aucune efficacité pédagogique réelle mesurée. |
| [Analyse exploratoire des performances](employee-performance-analysis/README.md) | Script, notebook, statistiques descriptives et détection IQR des valeurs atypiques. | CSV original absent ; résultats RH non établis. |

## Mes assistants IA pour les données

[Python Project Studio, DataLab Coordinateur, DataCollect, DataAnalyse et DataML](assistants-ia/README.md) : cinq assistants pour concevoir des projets Python, collecter, analyser et modéliser. Python Project Studio accompagne code, tests et documentation. DataLab Coordinateur réutilise les fichiers entre trois rôles dans une même session ; il ne contacte pas automatiquement les GPT indépendants. Présentations publiques, liens ChatGPT et limites d’accès documentés : les assistants restent soumis à leurs droits de partage.

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


### BikeDemand : prévision calendaire des locations de vélos
[Code, données dérivées et modèle](bike-demand/) · [Résultats sur le site](https://junior-booto-fle.juniorbooto.chatgpt.site/bike-demand.html)

17 379 observations UCI (2011–2012). Collecte, analyse et modèle exécutés dans un pipeline commun. MAE test 72,35 locations/h contre 79,79 pour la référence (−9,3 %). Prévision J+1 à partir du calendrier connu ; prototype historique, aucune connexion automatique entre GPTs indépendants.


### AfriFlow Explain : explorer les parcours et expliquer les alertes
[Code, tests et modèles](afriflow-explain/) · [Démonstration interactive](https://junior-booto-fle.juniorbooto.chatgpt.site/afriflow-explain.html)

11 775 transferts et 1 800 dossiers synthétiques. À budget égal (36 alertes sur 360 dossiers test), l’approche avec parcours repère 19 des 42 scénarios injectés, contre 3 pour les résumés de transactions ; 17 faux positifs subsistent. Chronologie, preuves par opération et couverture des horodatages visibles. Aucune banque connectée, aucun partenariat et aucune performance bancaire réelle revendiquée.


### Portfolio File Guardian : organiser sans perdre les originaux
[Code, documentation et tests](portfolio-file-guardian/) · [Présentation et rapport](https://junior-booto-fle.juniorbooto.chatgpt.site/portfolio-file-guardian.html)

Inventaire SHA-256, simulation par défaut, catégories configurables et organisation par copie avec journal de restauration. Démonstration sur 8 fichiers synthétiques : un groupe de doublons exacts, une collision de nom aux contenus distincts, 8 copies vérifiées puis retirées et tous les originaux conservés. 20 tests de comportement réussis localement sous Linux ; prototype local, sans synchronisation cloud ni suppression automatique des doublons.


### Portfolio Evidence Hub : chaque constat relié à une preuve
[Code, documentation et tests](portfolio-evidence-hub/) · [Tableau de bord](https://junior-booto-fle.juniorbooto.chatgpt.site/portfolio-evidence-hub.html)

Audit en lecture seule de trois projets réels : inventaire GitHub figé au commit audité, résultats CI attribués, concordance locale et observations HTTP datées. 24 contrôles : 13 vérifiés, 1 absence selon la règle, 9 à vérifier et 1 différence de fins de ligne expliquée. 20 tests du Hub réussis localement. Rapport historique, sans score d’expertise ni actualisation automatique.


### FLE Resource Studio : une ressource, trois chemins pour apprendre
[Code, catalogue et API locale](fle-resource-studio/) · [Studio interactif](https://junior-booto-fle.juniorbooto.chatgpt.site/fle-resource-studio.html)

Cinq thèmes FLE A1, 50 entrées de glossaire FR/ES/EN, trois aides différenciées et 45 combinaisons vérifiées. Fiches enseignant/apprenant, corrigés et critères observables ; 20 tests locaux réussis. Lecture vocale facultative selon navigateur, aucune bande-son enregistrée. Vidéos candidates à revoir, aucune efficacité en classe revendiquée.


### Transfer Cost Observatory : expliquer le montant reçu après les frais
[Code, paramètres et tests](transfer-cost-observatory/) · [Tableau de bord](https://junior-booto-fle.juniorbooto.chatgpt.site/transfer-cost-observatory.html)

27 scénarios sur USD→COP, USD→CDF et USD→ZAR, à budget total égal. Calculs Decimal : frais source, marge de change, frais réception, reliquat et arrondis ; 20 tests locaux réussis. Taux et tarifs entièrement fictifs : la tentative de collecte a reçu HTTP 403, aucun cours actuel, offre bancaire ou conseil individuel n’est revendiqué.
