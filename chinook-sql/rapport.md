# Chinook — 26 exercices SQL exécutés
Auteur du projet : Junior BOOTO Waba.
## Portée et provenance
Exercices inspirés de « Data Analysis Projects », Natacha Njongwa Yepnga / LeCoinStat, projet 5. Requêtes écrites et exécutées dans SQLite.
Source : https://github.com/lerocha/chinook-database/blob/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql
Blob GitHub : 299610dc69f04a2b16b3a2e45bd2af82ed2872a2.
Chinook est une base de démonstration : ventes générées et clients/employés fictifs. Aucun résultat commercial réel.
## Résultats vérifiés
- 412 factures ; 59 clients ; 3503 morceaux.
- Ventes : 2328.60 unités monétaires ; panier moyen : 5.65.
- Pays en tête : USA (523.06).
- Agent en tête : Jane Peacock (833.04).
- Période : 2021-01-01 au 2025-12-22.
## Adaptation des exercices
Les exercices 8, 18, 19 et 23 demandent 2009, 2010, 2011 ou 2013. Ces années sont absentes de cette version. Le fichier principal conserve les filtres demandés ; les résultats vides ou nuls ne prouvent pas une absence historique de ventes. Un second fichier contient les variantes 2021/2023, 2021, 2022 et 2025. Les années ne sont pas changées silencieusement.
Les classements en unités et en chiffre d'affaires sont distingués. Les ex æquo sont conservés pour les gagnants ; les tops de cinq ou trois lignes utilisent l'identifiant comme départage explicite.
## Contrôles
Intégrité SQLite et clés étrangères vérifiées. Total des factures égal à celui des lignes ; sommes par agent et pays réconciliées au total. 26 requêtes exécutées, 26 CSV générés, plus quatre variantes annuelles.
## Limites
Les données ne permettent pas d'estimer bénéfice ou marge : aucun coût de revient n'est fourni. Une différence entre agents peut refléter leur portefeuille ; elle ne démontre pas leur performance causale.
Machine learning non utilisé : ce projet porte sur SQL et des rapports descriptifs.
