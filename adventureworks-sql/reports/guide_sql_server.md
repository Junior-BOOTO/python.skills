# Portée et migration vers SQL Server

## Ce qui a été exécuté
Les analyses ont été exécutées sur **SQLite**, après import de neuf tables commerciales des fichiers officiels Microsoft à un commit fixé. La granularité, les références et les montants sont vérifiés. Aucun serveur SQL Server n’était disponible ; aucune exécution T-SQL n’est revendiquée.

## Installer la base native
Utiliser la procédure Microsoft : https://learn.microsoft.com/sql/samples/adventureworks-install-configure. La sauvegarde AdventureWorks2025 ou le script officiel d’installation permettent de travailler dans SQL Server. Les sauvegardes d’autres versions peuvent couvrir d’autres dates : vérifier MIN(OrderDate) et MAX(OrderDate) avant de comparer des résultats.

## Adapter les requêtes
Les jointures, `SUM`, `COUNT(DISTINCT ...)`, les CTE et fonctions de fenêtre suivent les mêmes principes. Il faut adapter :

| SQLite | SQL Server |
|---|---|
| `SalesOrderHeader` | `Sales.SalesOrderHeader` |
| `SalesOrderDetail` | `Sales.SalesOrderDetail` |
| `Customer`, `SalesTerritory`, `SalesPerson` | schéma `Sales` |
| `Product`, `ProductCategory`, `ProductSubcategory`, `ProductCostHistory` | schéma `Production` |
| `TerritoryGroup` dans l’import | `Sales.SalesTerritory.[Group]` |
| `date(OrderDate)` | `CAST(OrderDate AS date)` |
| `strftime('%Y-%m',OrderDate)` | `CONVERT(char(7),OrderDate,120)` |
| `date(x,'-89 days')` | `DATEADD(day,-89,CAST(x AS date))` |
| `LIMIT 5` | `SELECT TOP (5) ... ORDER BY ...` |
| `WITH RECURSIVE` | `;WITH` pour une CTE récursive |
| `date(x,'+1 month')` | `DATEADD(month,1,x)` |
| `CAST(id AS TEXT)` | `CAST(id AS varchar(30))` |

Le calendrier mensuel peut utiliser `DATEFROMPARTS(YEAR(OrderDate),MONTH(OrderDate),1)` et `DATEADD`. Pour une récursion supérieure à 100 mois, prévoir une limite `MAXRECURSION` adaptée.

Conserver le calcul de revenu sur les **lignes**, la catégorie « sans agent », les commandes distinctes, les dates de coûts inclusives et le traitement explicite des coûts absents. Ne pas additionner `SubTotal` de la commande après une jointure avec ses lignes. Les coûts standards et les champs calculés natifs ne doivent pas être interprétés comme des coûts réels de toutes les charges.
