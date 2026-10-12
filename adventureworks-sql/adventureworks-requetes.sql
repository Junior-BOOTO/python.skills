-- 1. Ventes par région en 2024
-- Année demandée présente dans les fichiers officiels utilisés. Revenu hors taxes et fret.
SELECT Territoire,ROUND(SUM(Revenu),2) AS Revenu2024
FROM v_ventes WHERE OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01'
GROUP BY Territoire ORDER BY Revenu2024 DESC;

-- 2. Clients actifs
-- Actif = au moins une commande dans les 90 derniers jours disponibles. Ancrage sur la base, pas sur la date du jour.
SELECT CustomerID,DerniereCommande,Commandes,ROUND(DepenseTotale,2) AS DepenseTotale
FROM v_clients_total
WHERE DerniereCommande >= date((SELECT MAX(OrderDate) FROM SalesOrderHeader),'-89 days')
ORDER BY DerniereCommande DESC,CustomerID;

-- 3. Ventes par catégorie
-- Agrégation de lignes, sans multiplier les sous-totaux des commandes.
SELECT Categorie,ROUND(SUM(Revenu),2) AS Revenu,SUM(Quantite) AS Quantite
FROM v_ventes GROUP BY Categorie ORDER BY Revenu DESC;

-- 4. Ventes par agent
-- Les commandes sans agent restent dans une catégorie distincte ; on ne les attribue pas à un employé fictif.
SELECT COALESCE(CAST(SalesPersonID AS TEXT),'Sans agent attribué') AS Agent,
 ROUND(SUM(Revenu),2) AS Revenu,COUNT(DISTINCT SalesOrderID) AS Commandes
FROM v_ventes GROUP BY SalesPersonID ORDER BY Revenu DESC;

-- 5. Top 5 des produits par revenu
-- Le PDF emploie « rentables » puis précise « revenus générés » : ce classement mesure le revenu, pas un bénéfice.
SELECT ProductID,Produit,ROUND(SUM(Revenu),2) AS Revenu
FROM v_ventes GROUP BY ProductID,Produit
ORDER BY Revenu DESC,ProductID LIMIT 5;

-- 6. Ventes par segment client
-- Segment défini par Customer.StoreID : revendeur si présent, particulier sinon. Il ne s’agit pas d’une segmentation commerciale native plus détaillée.
SELECT SegmentClient,ROUND(SUM(Revenu),2) AS Revenu,
 COUNT(DISTINCT CustomerID) AS Clients,COUNT(DISTINCT SalesOrderID) AS Commandes
FROM v_ventes GROUP BY SegmentClient ORDER BY Revenu DESC;

-- 7. Segmentation par montant dépensé
-- CUME_DIST classe les clients acheteurs selon leur dépense : bas jusqu’au premier tiers, moyen jusqu’au deuxième, élevé au-delà. Les égalités restent ensemble ; les tailles peuvent différer.
WITH classement AS (
 SELECT *,CUME_DIST() OVER (ORDER BY DepenseTotale) AS PositionRelative
 FROM v_clients_total
)
SELECT CustomerID,ROUND(DepenseTotale,2) AS DepenseTotale,
 CASE WHEN PositionRelative <= 1.0/3 THEN 'Bas'
      WHEN PositionRelative <= 2.0/3 THEN 'Moyen' ELSE 'Élevé' END AS SegmentDepense
FROM classement ORDER BY DepenseTotale DESC,CustomerID;

-- 8. Top 10 des clients
-- Dépense cumulée sur toute la période. Identifiants seulement, sans coordonnées personnelles.
SELECT CustomerID,Commandes,ROUND(DepenseTotale,2) AS DepenseTotale
FROM v_clients_total ORDER BY DepenseTotale DESC,CustomerID LIMIT 10;

-- 9. Clients par type de commande
-- OnlineOrderFlag distingue en ligne et hors ligne. Une commande hors ligne ne prouve pas un achat physique en magasin.
SELECT CustomerID,MAX(OnlineOrderFlag) AS ACommandeEnLigne,
 MAX(1-OnlineOrderFlag) AS ACommandeHorsLigne,
 CASE WHEN MIN(OnlineOrderFlag) != MAX(OnlineOrderFlag) THEN 'Mixte'
      WHEN MAX(OnlineOrderFlag)=1 THEN 'En ligne' ELSE 'Hors ligne' END AS Canal
FROM SalesOrderHeader GROUP BY CustomerID ORDER BY CustomerID;

-- 10. Produits populaires sur les 12 derniers mois
-- Fenêtre glissante de douze mois jusqu’à la dernière date disponible, inclusive. Popularité = quantités, pas revenu.
SELECT ProductID,Produit,SUM(Quantite) AS Quantite,ROUND(SUM(Revenu),2) AS Revenu
FROM v_ventes
WHERE date(OrderDate) > date((SELECT MAX(OrderDate) FROM SalesOrderHeader),'-12 months')
GROUP BY ProductID,Produit ORDER BY Quantite DESC,ProductID;

-- 11. Ventes par type de produit
-- Les types sont les catégories réelles Bikes, Components, Clothing et Accessories. On n’invente pas de catégories électronique/vêtements absentes.
SELECT pc.Name AS TypeProduit,COUNT(DISTINCT v.ProductID) AS ProduitsVendus,
 ROUND(SUM(v.Revenu),2) AS Revenu
FROM v_ventes v JOIN Product p ON p.ProductID=v.ProductID
JOIN ProductSubcategory ps ON ps.ProductSubcategoryID=p.ProductSubcategoryID
JOIN ProductCategory pc ON pc.ProductCategoryID=ps.ProductCategoryID
GROUP BY pc.ProductCategoryID,pc.Name ORDER BY Revenu DESC;

-- 12. Ventes par produit et par mois
-- Douze mois calendaires incluant le dernier mois disponible. Calendrier dense : zéro pour les mois sans vente de chaque produit vendu pendant la fenêtre.
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

-- 13. Ventes par région et produit
-- Agrégation territoriale et produit, avec conservation des valeurs non attribuées.
SELECT Territoire,ProductID,Produit,ROUND(SUM(Revenu),2) AS Revenu,SUM(Quantite) AS Quantite
FROM v_ventes GROUP BY Territoire,ProductID,Produit
ORDER BY Territoire,Revenu DESC,ProductID;

-- 14. Taux de retour des produits
-- Non calculable avec ces tables : pas de quantités de retours clients identifiables. Commandes annulées et rebuts de fabrication ne sont pas des retours clients. Une source dédiée avec produit, date, quantité retournée et commande d’origine est nécessaire.
-- Aucun taux fabriqué. Exercice documenté, sans calcul numérique.

-- 15. Marge standard estimée par produit
-- Revenu moins quantité × coût standard historique applicable à la date de commande. Ce proxy exclut les autres charges et n’est pas un bénéfice net. Marge laissée NULL pour les produits dont des coûts historiques manquent.
SELECT ProductID,Produit,ROUND(SUM(Revenu),2) AS Revenu,
 SUM(CASE WHEN CoutUnitaireHistorique IS NULL THEN 1 ELSE 0 END) AS LignesSansCout,
 CASE WHEN COUNT(CoutUnitaireHistorique)=COUNT(*) THEN ROUND(SUM(MargeStandardEstimee),2) END AS MargeStandardEstimee,
 CASE WHEN COUNT(CoutUnitaireHistorique)=COUNT(*) AND SUM(Revenu)>0
      THEN ROUND(SUM(MargeStandardEstimee)/SUM(Revenu),4) END AS TauxMargeStandard
FROM v_ventes GROUP BY ProductID,Produit
ORDER BY MargeStandardEstimee DESC,ProductID;

-- 16. Bonus : cumul et moyenne mobile mensuels
-- CTE récursive pour les mois, SUM cumulée et AVG sur trois mois. Le calendrier est dense : une fenêtre de trois lignes représente bien trois mois.
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

-- 17. Bonus : top produits par région
-- DENSE_RANK garde les ex æquo. Trois rangs peuvent donc contenir plus de trois produits.
WITH totaux AS (
 SELECT Territoire,ProductID,Produit,SUM(Revenu) AS Revenu
 FROM v_ventes GROUP BY Territoire,ProductID,Produit
), rangs AS (
 SELECT *,DENSE_RANK() OVER (PARTITION BY Territoire ORDER BY Revenu DESC) AS Rang
 FROM totaux
)
SELECT Territoire,ProductID,Produit,ROUND(Revenu,2) AS Revenu,Rang
FROM rangs WHERE Rang<=3 ORDER BY Territoire,Rang,ProductID;

-- 18. Bonus : clientes et clients sans commande
-- LEFT JOIN : inclusion explicite des clients de la table Customer sans achat. À distinguer de la segmentation des acheteurs de l’exercice 7.
SELECT c.CustomerID FROM Customer c
LEFT JOIN SalesOrderHeader h ON h.CustomerID=c.CustomerID
WHERE h.SalesOrderID IS NULL ORDER BY c.CustomerID;