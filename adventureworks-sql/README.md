# AdventureWorks — SQL avancé et rapports commerciaux
**Junior BOOTO Waba · Projet 8 · SQL et Python**

15 exercices documentés : **14 analyses exécutées**, un exercice de retours non calculable avec les tables disponibles, et **3 bonus exécutés**. Jointures, CTE, vues, calendrier récursif, segmentation, classements et fenêtres cumulées/mobiles.

## Résultats vérifiés
- 31 465 commandes et 121 317 lignes de vente.
- Période : 30 mai 2022 au 29 juin 2025. L’année 2024 demandée dans l’exercice 1 est disponible.
- Revenu des lignes, hors taxes et fret : **109 846 381,40 UM**.
- Intégrité SQLite, clés étrangères, granularité des jointures, formules des lignes et réconciliation des totaux vérifiées.

## Reproduire
Python 3.11 ou plus, bibliothèque standard uniquement. SQLite doit prendre en charge les fonctions de fenêtre (version 3.25 ou plus).
```sh
python collecter.py
python construire.py
python definir_requetes.py
python executer.py
```
La collecte télécharge les fichiers du dépôt officiel Microsoft à un commit fixé et vérifie leurs empreintes Git. Internet est nécessaire au premier lancement. Les relances utilisent les fichiers bruts conservés.

Les requêtes peuvent ensuite être explorées avec DB Browser for SQLite en ouvrant `collected/AdventureWorks_commercial.sqlite`. Installer les vues avant les requêtes n’est pas nécessaire après `construire.py`, qui le fait déjà.

## Lire le projet
- [Requêtes SQL](adventureworks-requetes.sql) et [vues](vues.sql)
- [Guide détaillé avec aperçus](reports/guide_exercices.md)
- [Rapport et limites](reports/rapport.md)
- [Résultats CSV](analysis/)
- [Guide SQL Server](reports/guide_sql_server.md)
- [Sources fixées](sources.json), [contrôles](reports/controles.json) et [manifeste](manifest.json)

## Périmètre exact
Les sources sont les fichiers d’installation **OLTP** officiels AdventureWorks. Neuf tables sont importées avec leurs colonnes commerciales utiles. Ce sous-ensemble SQLite n’est pas une installation intégrale d’AdventureWorks ni une sauvegarde SQL Server. Les requêtes livrées et exécutées utilisent le dialecte SQLite.

Le revenu est la somme des lignes remisées (`LineTotal`), distincte des taxes et frais de transport. La marge de l’exercice 15 est estimée à partir du **coût standard historique** applicable ; elle n’est pas un bénéfice net. 64 lignes n’ont pas de coût historique correspondant : les produits concernés ne reçoivent pas de marge totale trompeusement complète.

L’exercice 14 ne dispose pas de données de retours clients exploitables. Un taux nul ne serait pas justifié ; le calcul est marqué non disponible. Les annulations ou rebuts ne sont pas utilisés comme substituts.

## Attribution
Microsoft, `microsoft/sql-server-samples`, licence MIT incluse. Toutes les données de cette base sont fictives. Source fixée et empreintes dans `sources.json` et `reports/empreintes_sources.json`.

Inspiration : *Data Analysis Projects*, Natacha Njongwa Yepnga / LeCoinStat, projet 8. Le PDF original n’est pas redistribué. Aucune formation de modèle prédictif n’est nécessaire pour cette analyse SQL.
