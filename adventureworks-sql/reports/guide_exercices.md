# Guide des exercices — AdventureWorks

SQLite, adaptation commerciale des données officielles Microsoft. Tous les montants sont en UM.

## 1. Ventes par région en 2024

Année demandée présente dans les fichiers officiels utilisés. Revenu hors taxes et fret.

```sql
SELECT Territoire,ROUND(SUM(Revenu),2) AS Revenu2024
FROM v_ventes WHERE OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01'
GROUP BY Territoire ORDER BY Revenu2024 DESC;
```

Résultat exécuté : 10 lignes. Aperçu (au plus cinq lignes) :

| Territoire | Revenu2024 |
| --- | --- |
| Southwest | 9121931.65 |
| Canada | 6231209.96 |
| Northwest | 6018432.58 |
| Australia | 4246450.55 |
| France | 3816543.33 |

## 2. Clients actifs

Actif = au moins une commande dans les 90 derniers jours disponibles. Ancrage sur la base, pas sur la date du jour.

```sql
SELECT CustomerID,DerniereCommande,Commandes,ROUND(DepenseTotale,2) AS DepenseTotale
FROM v_clients_total
WHERE DerniereCommande >= date((SELECT MAX(OrderDate) FROM SalesOrderHeader),'-89 days')
ORDER BY DerniereCommande DESC,CustomerID;
```

Résultat exécuté : 5059 lignes. Aperçu (au plus cinq lignes) :

| CustomerID | DerniereCommande | Commandes | DepenseTotale |
| --- | --- | --- | --- |
| 11078 | 2025-06-29 | 17 | 913.27 |
| 11287 | 2025-06-29 | 27 | 1167.07 |
| 11657 | 2025-06-29 | 2 | 178.96 |
| 11794 | 2025-06-29 | 2 | 77.27 |
| 11927 | 2025-06-29 | 2 | 51.94 |

## 3. Ventes par catégorie

Agrégation de lignes, sans multiplier les sous-totaux des commandes.

```sql
SELECT Categorie,ROUND(SUM(Revenu),2) AS Revenu,SUM(Quantite) AS Quantite
FROM v_ventes GROUP BY Categorie ORDER BY Revenu DESC;
```

Résultat exécuté : 4 lignes. Aperçu (au plus cinq lignes) :

| Categorie | Revenu | Quantite |
| --- | --- | --- |
| Bikes | 94651172.7 | 90268 |
| Components | 11802593.29 | 49044 |
| Clothing | 2120542.52 | 73670 |
| Accessories | 1272072.88 | 61932 |

## 4. Ventes par agent

Les commandes sans agent restent dans une catégorie distincte ; on ne les attribue pas à un employé fictif.

```sql
SELECT COALESCE(CAST(SalesPersonID AS TEXT),'Sans agent attribué') AS Agent,
 ROUND(SUM(Revenu),2) AS Revenu,COUNT(DISTINCT SalesOrderID) AS Commandes
FROM v_ventes GROUP BY SalesPersonID ORDER BY Revenu DESC;
```

Résultat exécuté : 18 lignes. Aperçu (au plus cinq lignes) :

| Agent | Revenu | Commandes |
| --- | --- | --- |
| Sans agent attribué | 29358677.22 | 27659 |
| 276 | 10367007.43 | 418 |
| 277 | 10065803.54 | 473 |
| 275 | 9293903.0 | 450 |
| 289 | 8503338.65 | 348 |

## 5. Top 5 des produits par revenu

Le PDF emploie « rentables » puis précise « revenus générés » : ce classement mesure le revenu, pas un bénéfice.

```sql
SELECT ProductID,Produit,ROUND(SUM(Revenu),2) AS Revenu
FROM v_ventes GROUP BY ProductID,Produit
ORDER BY Revenu DESC,ProductID LIMIT 5;
```

Résultat exécuté : 5 lignes. Aperçu (au plus cinq lignes) :

| ProductID | Produit | Revenu |
| --- | --- | --- |
| 782 | Mountain-200 Black, 38 | 4400592.8 |
| 783 | Mountain-200 Black, 42 | 4009494.76 |
| 779 | Mountain-200 Silver, 38 | 3693678.03 |
| 780 | Mountain-200 Silver, 42 | 3438478.86 |
| 781 | Mountain-200 Silver, 46 | 3434256.94 |

## 6. Ventes par segment client

Segment défini par Customer.StoreID : revendeur si présent, particulier sinon. Il ne s’agit pas d’une segmentation commerciale native plus détaillée.

```sql
SELECT SegmentClient,ROUND(SUM(Revenu),2) AS Revenu,
 COUNT(DISTINCT CustomerID) AS Clients,COUNT(DISTINCT SalesOrderID) AS Commandes
FROM v_ventes GROUP BY SegmentClient ORDER BY Revenu DESC;
```

Résultat exécuté : 2 lignes. Aperçu (au plus cinq lignes) :

| SegmentClient | Revenu | Clients | Commandes |
| --- | --- | --- | --- |
| Revendeur | 80487704.18 | 635 | 3806 |
| Particulier | 29358677.22 | 18484 | 27659 |

## 7. Segmentation par montant dépensé

CUME_DIST classe les clients acheteurs selon leur dépense : bas jusqu’au premier tiers, moyen jusqu’au deuxième, élevé au-delà. Les égalités restent ensemble ; les tailles peuvent différer.

```sql
WITH classement AS (
 SELECT *,CUME_DIST() OVER (ORDER BY DepenseTotale) AS PositionRelative
 FROM v_clients_total
)
SELECT CustomerID,ROUND(DepenseTotale,2) AS DepenseTotale,
 CASE WHEN PositionRelative <= 1.0/3 THEN 'Bas'
      WHEN PositionRelative <= 2.0/3 THEN 'Moyen' ELSE 'Élevé' END AS SegmentDepense
FROM classement ORDER BY DepenseTotale DESC,CustomerID;
```

Résultat exécuté : 19119 lignes. Aperçu (au plus cinq lignes) :

| CustomerID | DepenseTotale | SegmentDepense |
| --- | --- | --- |
| 29818 | 877107.19 | Élevé |
| 29715 | 853849.18 | Élevé |
| 29722 | 841908.77 | Élevé |
| 30117 | 816755.58 | Élevé |
| 29614 | 799277.9 | Élevé |

## 8. Top 10 des clients

Dépense cumulée sur toute la période. Identifiants seulement, sans coordonnées personnelles.

```sql
SELECT CustomerID,Commandes,ROUND(DepenseTotale,2) AS DepenseTotale
FROM v_clients_total ORDER BY DepenseTotale DESC,CustomerID LIMIT 10;
```

Résultat exécuté : 10 lignes. Aperçu (au plus cinq lignes) :

| CustomerID | Commandes | DepenseTotale |
| --- | --- | --- |
| 29818 | 12 | 877107.19 |
| 29715 | 12 | 853849.18 |
| 29722 | 12 | 841908.77 |
| 30117 | 12 | 816755.58 |
| 29614 | 12 | 799277.9 |

## 9. Clients par type de commande

OnlineOrderFlag distingue en ligne et hors ligne. Une commande hors ligne ne prouve pas un achat physique en magasin.

```sql
SELECT CustomerID,MAX(OnlineOrderFlag) AS ACommandeEnLigne,
 MAX(1-OnlineOrderFlag) AS ACommandeHorsLigne,
 CASE WHEN MIN(OnlineOrderFlag) != MAX(OnlineOrderFlag) THEN 'Mixte'
      WHEN MAX(OnlineOrderFlag)=1 THEN 'En ligne' ELSE 'Hors ligne' END AS Canal
FROM SalesOrderHeader GROUP BY CustomerID ORDER BY CustomerID;
```

Résultat exécuté : 19119 lignes. Aperçu (au plus cinq lignes) :

| CustomerID | ACommandeEnLigne | ACommandeHorsLigne | Canal |
| --- | --- | --- | --- |
| 11000 | 1 | 0 | En ligne |
| 11001 | 1 | 0 | En ligne |
| 11002 | 1 | 0 | En ligne |
| 11003 | 1 | 0 | En ligne |
| 11004 | 1 | 0 | En ligne |

## 10. Produits populaires sur les 12 derniers mois

Fenêtre glissante de douze mois jusqu’à la dernière date disponible, inclusive. Popularité = quantités, pas revenu.

```sql
SELECT ProductID,Produit,SUM(Quantite) AS Quantite,ROUND(SUM(Revenu),2) AS Revenu
FROM v_ventes
WHERE date(OrderDate) > date((SELECT MAX(OrderDate) FROM SalesOrderHeader),'-12 months')
GROUP BY ProductID,Produit ORDER BY Quantite DESC,ProductID;
```

Résultat exécuté : 201 lignes. Aperçu (au plus cinq lignes) :

| ProductID | Produit | Quantite | Revenu |
| --- | --- | --- | --- |
| 870 | Water Bottle - 30 oz. | 6119 | 26440.34 |
| 712 | AWC Logo Cap | 4296 | 30542.49 |
| 711 | Sport-100 Helmet, Blue | 3754 | 107067.63 |
| 708 | Sport-100 Helmet, Black | 3750 | 106567.13 |
| 707 | Sport-100 Helmet, Red | 3698 | 107617.99 |

## 11. Ventes par type de produit

Les types sont les catégories réelles Bikes, Components, Clothing et Accessories. On n’invente pas de catégories électronique/vêtements absentes.

```sql
SELECT pc.Name AS TypeProduit,COUNT(DISTINCT v.ProductID) AS ProduitsVendus,
 ROUND(SUM(v.Revenu),2) AS Revenu
FROM v_ventes v JOIN Product p ON p.ProductID=v.ProductID
JOIN ProductSubcategory ps ON ps.ProductSubcategoryID=p.ProductSubcategoryID
JOIN ProductCategory pc ON pc.ProductCategoryID=ps.ProductCategoryID
GROUP BY pc.ProductCategoryID,pc.Name ORDER BY Revenu DESC;
```

Résultat exécuté : 4 lignes. Aperçu (au plus cinq lignes) :

| TypeProduit | ProduitsVendus | Revenu |
| --- | --- | --- |
| Bikes | 97 | 94651172.7 |
| Components | 111 | 11802593.29 |
| Clothing | 34 | 2120542.52 |
| Accessories | 24 | 1272072.88 |

## 12. Ventes par produit et par mois

Douze mois calendaires incluant le dernier mois disponible. Calendrier dense : zéro pour les mois sans vente de chaque produit vendu pendant la fenêtre.

```sql
WITH RECURSIVE calendrier(Mois) AS (
 SELECT date((SELECT MAX(OrderDate) FROM SalesOrderHeader),'start of month','-11 months')
 UNION ALL SELECT date(Mois,'+1 month') FROM calendrier
 WHERE Mois < date((SELECT MAX(OrderDate) FROM SalesOrderHeader),'start of month')
), ventes AS (
 SELECT ProductID,Produit,date(OrderDate,'start of month') AS Mois,SUM(Revenu) AS Revenu
 FROM v_ventes WHERE date(OrderDate) >= (SELECT MIN(Mois) FROM calendrier)
 GROUP BY ProductID,Produit,date(OrderDate,'start of month')
), produits AS (SELECT DISTINCT ProductID,Produit FROM ventes)
SELECT p.ProductID,p.Produit,c.Mois,ROUND(COALESCE(v.Revenu,0),2) AS Revenu
FROM produits p CROSS JOIN calendrier c
LEFT JOIN ventes v ON v.ProductID=p.ProductID AND v.Mois=c.Mois
ORDER BY p.ProductID,c.Mois;
```

Résultat exécuté : 2412 lignes. Aperçu (au plus cinq lignes) :

| ProductID | Produit | Mois | Revenu |
| --- | --- | --- | --- |
| 707 | Sport-100 Helmet, Red | 2024-07-01 | 11458.0 |
| 707 | Sport-100 Helmet, Red | 2024-08-01 | 8718.72 |
| 707 | Sport-100 Helmet, Red | 2024-09-01 | 8584.39 |
| 707 | Sport-100 Helmet, Red | 2024-10-01 | 9580.23 |
| 707 | Sport-100 Helmet, Red | 2024-11-01 | 9461.3 |

## 13. Ventes par région et produit

Agrégation territoriale et produit, avec conservation des valeurs non attribuées.

```sql
SELECT Territoire,ProductID,Produit,ROUND(SUM(Revenu),2) AS Revenu,SUM(Quantite) AS Quantite
FROM v_ventes GROUP BY Territoire,ProductID,Produit
ORDER BY Territoire,Revenu DESC,ProductID;
```

Résultat exécuté : 2446 lignes. Aperçu (au plus cinq lignes) :

| Territoire | ProductID | Produit | Revenu | Quantite |
| --- | --- | --- | --- | --- |
| Australia | 749 | Road-150 Red, 62 | 397187.97 | 111 |
| Australia | 783 | Mountain-200 Black, 42 | 394869.42 | 187 |
| Australia | 779 | Mountain-200 Silver, 38 | 393702.3 | 184 |
| Australia | 751 | Road-150 Red, 48 | 390031.43 | 109 |
| Australia | 753 | Road-150 Red, 56 | 382874.89 | 107 |

## 14. Taux de retour des produits

Non calculable avec ces tables : pas de quantités de retours clients identifiables. Commandes annulées et rebuts de fabrication ne sont pas des retours clients. Une source dédiée avec produit, date, quantité retournée et commande d’origine est nécessaire.

```sql
-- Aucun taux fabriqué. Exercice documenté, sans calcul numérique.
```

Statut : non calculable ; données de retours manquantes.

## 15. Marge standard estimée par produit

Revenu moins quantité × coût standard historique applicable à la date de commande. Ce proxy exclut les autres charges et n’est pas un bénéfice net. Marge laissée NULL pour les produits dont des coûts historiques manquent.

```sql
SELECT ProductID,Produit,ROUND(SUM(Revenu),2) AS Revenu,
 SUM(CASE WHEN CoutUnitaireHistorique IS NULL THEN 1 ELSE 0 END) AS LignesSansCout,
 CASE WHEN COUNT(CoutUnitaireHistorique)=COUNT(*) THEN ROUND(SUM(MargeStandardEstimee),2) END AS MargeStandardEstimee,
 CASE WHEN COUNT(CoutUnitaireHistorique)=COUNT(*) AND SUM(Revenu)>0
      THEN ROUND(SUM(MargeStandardEstimee)/SUM(Revenu),4) END AS TauxMargeStandard
FROM v_ventes GROUP BY ProductID,Produit
ORDER BY MargeStandardEstimee DESC,ProductID;
```

Résultat exécuté : 266 lignes. Aperçu (au plus cinq lignes) :

| ProductID | Produit | Revenu | LignesSansCout | MargeStandardEstimee | TauxMargeStandard |
| --- | --- | --- | --- | --- | --- |
| 782 | Mountain-200 Black, 38 | 4400592.8 | 0 | 872822.12 | 0.1983 |
| 783 | Mountain-200 Black, 42 | 4009494.76 | 0 | 863800.75 | 0.2154 |
| 779 | Mountain-200 Silver, 38 | 3693678.03 | 0 | 829132.41 | 0.2245 |
| 784 | Mountain-200 Black, 46 | 3309673.22 | 0 | 808088.34 | 0.2442 |
| 781 | Mountain-200 Silver, 46 | 3434256.94 | 0 | 793957.25 | 0.2312 |

## 16. Bonus : cumul et moyenne mobile mensuels

CTE récursive pour les mois, SUM cumulée et AVG sur trois mois. Le calendrier est dense : une fenêtre de trois lignes représente bien trois mois.

```sql
WITH RECURSIVE calendrier(Mois) AS (
 SELECT date((SELECT MIN(OrderDate) FROM SalesOrderHeader),'start of month')
 UNION ALL SELECT date(Mois,'+1 month') FROM calendrier
 WHERE Mois < date((SELECT MAX(OrderDate) FROM SalesOrderHeader),'start of month')
), dense AS (
 SELECT c.Mois,COALESCE(v.Revenu,0) AS Revenu FROM calendrier c
 LEFT JOIN v_ventes_mensuelles v ON v.Mois=strftime('%Y-%m',c.Mois)
)
SELECT Mois,ROUND(Revenu,2) AS Revenu,
 ROUND(SUM(Revenu) OVER (ORDER BY Mois ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW),2) AS Cumul,
 ROUND(AVG(Revenu) OVER (ORDER BY Mois ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) AS MoyenneMobile3M,
 COUNT(*) OVER (ORDER BY Mois ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS MoisDansFenetre
FROM dense ORDER BY Mois;
```

Résultat exécuté : 38 lignes. Aperçu (au plus cinq lignes) :

| Mois | Revenu | Cumul | MoyenneMobile3M | MoisDansFenetre |
| --- | --- | --- | --- | --- |
| 2022-05-01 | 517737.44 | 517737.44 | 517737.44 | 1 |
| 2022-06-01 | 2001278.97 | 2519016.4 | 1259508.2 | 2 |
| 2022-07-01 | 1668510.5 | 4187526.9 | 1395842.3 | 3 |
| 2022-08-01 | 1326138.11 | 5513665.01 | 1665309.19 | 3 |
| 2022-09-01 | 2836409.61 | 8350074.62 | 1943686.07 | 3 |

## 17. Bonus : top produits par région

DENSE_RANK garde les ex æquo. Trois rangs peuvent donc contenir plus de trois produits.

```sql
WITH totaux AS (
 SELECT Territoire,ProductID,Produit,SUM(Revenu) AS Revenu
 FROM v_ventes GROUP BY Territoire,ProductID,Produit
), rangs AS (
 SELECT *,DENSE_RANK() OVER (PARTITION BY Territoire ORDER BY Revenu DESC) AS Rang
 FROM totaux
)
SELECT Territoire,ProductID,Produit,ROUND(Revenu,2) AS Revenu,Rang
FROM rangs WHERE Rang<=3 ORDER BY Territoire,Rang,ProductID;
```

Résultat exécuté : 30 lignes. Aperçu (au plus cinq lignes) :

| Territoire | ProductID | Produit | Revenu | Rang |
| --- | --- | --- | --- | --- |
| Australia | 749 | Road-150 Red, 62 | 397187.97 | 1 |
| Australia | 783 | Mountain-200 Black, 42 | 394869.42 | 2 |
| Australia | 779 | Mountain-200 Silver, 38 | 393702.3 | 3 |
| Canada | 782 | Mountain-200 Black, 38 | 735839.95 | 1 |
| Canada | 783 | Mountain-200 Black, 42 | 642039.84 | 2 |

## 18. Bonus : clientes et clients sans commande

LEFT JOIN : inclusion explicite des clients de la table Customer sans achat. À distinguer de la segmentation des acheteurs de l’exercice 7.

```sql
SELECT c.CustomerID FROM Customer c
LEFT JOIN SalesOrderHeader h ON h.CustomerID=c.CustomerID
WHERE h.SalesOrderID IS NULL ORDER BY c.CustomerID;
```

Résultat exécuté : 701 lignes. Aperçu (au plus cinq lignes) :

| CustomerID |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
