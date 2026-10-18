# Appliquer cinq ouvrages aux projets Python et data

**Junior BOOTO Waba · Mis à jour le 18 octobre 2026**

Ce guide transforme cinq références de lecture en pratiques concrètes pour le portfolio. C’est une synthèse originale et un parcours d’application : il ne reproduit pas les livres. Les projets cités existaient déjà dans le dépôt; ce guide ne prétend pas qu’ils ont été réalisés à partir de ces ouvrages.

## Les cinq références

| Ouvrage | Apport à travailler | Projets du dépôt où l’appliquer |
| --- | --- | --- |
| *Think Like a Data Analyst*, version MEAP 2 | Cadrer une question, formuler une hypothèse, choisir une mesure et présenter une conclusion utile. | [Superstore — Analyse bivariée](../superstore-bivariate/README.md), [Wine Quality — ACP](../wine-quality-acp/README.md) |
| *Data Analysis with Python* — Bernd Klein | Pratiquer NumPy, pandas, Matplotlib, la lecture de fichiers, les regroupements et le traitement des valeurs manquantes. | [Superstore — Analyse bivariée](../superstore-bivariate/README.md), [Document-to-Data Lab](../document-to-data-lab/README.md) |
| *Data Analysis and Decision Making*, 4e édition — S. Christian Albright, Wayne L. Winston et Christopher J. Zappe | Consolider les distributions, les relations entre variables, l’inférence, la régression, les séries temporelles, la décision et la simulation. | [Superstore — Analyse bivariée](../superstore-bivariate/README.md), [BikeDemand](../bike-demand/README.md), [Prévision des ventes](../sales-time-series/README.md) |
| *Data Pipelines Pocket Reference* — James Densmore | Documenter ingestion, transformations, contrôles de qualité, orchestration et suivi d’un pipeline réutilisable. | [Document-to-Data Lab](../document-to-data-lab/README.md), [BikeDemand](../bike-demand/README.md) |
| *Learn SQLite with Python in 24 Hours for Beginners* — S. Basu | Relier les bases SQLite aux requêtes et analyses reproductibles en Python. | [Chinook — SQL et Python](../chinook-sql/README.md), [Document-to-Data Lab](../document-to-data-lab/README.md) |

Voir les notices complètes et les liens d’accès dans [la bibliothèque de références](README.md).

## Parcours d’analyse à réutiliser

1. **Poser une question précise.** Définir la population, l’unité observée, la période, le résultat étudié et la décision que l’analyse pourrait éclairer.
2. **Établir la provenance.** Décrire la source, sa date, ses conditions d’utilisation, ses unités et ses limites. Conserver la source brute séparément et noter son empreinte quand c’est utile.
3. **Contrôler les données.** Vérifier les types, les clés, les dates, les unités, les doublons et les valeurs manquantes. Expliquer chaque correction et garder les anomalies importantes traçables.
4. **Explorer avant de conclure.** Examiner les effectifs, les distributions, les taux et les relations adaptées à la question. Indiquer les dénominateurs et éviter de traiter les lignes répétées comme des observations indépendantes sans justification.
5. **Choisir une méthode proportionnée.** Distinguer description, association, inférence et prédiction. Pour un modèle, établir une référence simple et une séparation d’évaluation appropriée. Une corrélation ou une différence observée ne démontre pas à elle seule une cause.
6. **Communiquer une preuve.** Relier chaque conclusion à un tableau, un graphique ou une mesure calculée; dire ce que les données permettent et ne permettent pas d’affirmer.
7. **Rendre le travail reprenable.** Documenter l’environnement, les commandes, les transformations, les résultats vérifiés et les limites. Étiqueter les données synthétiques et exclure les données confidentielles.

## Mise en pratique dans le dépôt

- Dans **Superstore**, vérifier que les taux utilisent le bon dénominateur, comparer les mesures d’association et garder les conclusions descriptives.
- Dans **Document-to-Data Lab**, prolonger la provenance déjà documentée par des contrôles de validation explicites, des étapes rejouables et un suivi des anomalies, en s’inspirant du parcours sur les pipelines.
- Dans **Chinook**, relier les requêtes SQL et les jointures à un accès SQLite depuis Python, puis documenter les résultats et les limites de la base de démonstration.
- Dans **BikeDemand** et **sales-time-series**, comparer une méthode à une référence et respecter l’ordre temporel de l’évaluation.
- Dans **Document-to-Data Lab**, relier chaque résultat à sa source et rendre visibles les lignes acceptées, rejetées et à examiner.

Ces exemples montrent comment le parcours peut guider une relecture ou une amélioration. Ils ne signifient pas que les projets ont tous été reconstruits à partir de ces livres.

## Droits et attribution

Le dépôt publie ici des notices bibliographiques, des liens d’accès et cette synthèse originale. Il ne redistribue pas les PDF fournis, leurs chapitres, leurs tableaux ni leurs exemples sous copyright. Pour les exercices, écrire une implémentation originale et citer toute source de données ou d’inspiration.