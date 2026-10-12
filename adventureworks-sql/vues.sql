-- Adaptation SQLite des tables commerciales officielles ; montants en UM.
CREATE VIEW v_ventes AS
SELECT h.SalesOrderID,h.OrderDate,h.CustomerID,h.SalesPersonID,h.OnlineOrderFlag,
 d.SalesOrderDetailID,d.ProductID,p.Name AS Produit,d.OrderQty AS Quantite,
 d.LineTotal AS Revenu,COALESCE(t.Name,'Non attribué') AS Territoire,
 COALESCE(pc.Name,'Non classé') AS Categorie,
 CASE WHEN c.StoreID IS NOT NULL THEN 'Revendeur' ELSE 'Particulier' END AS SegmentClient,
 ch.StandardCost AS CoutUnitaireHistorique,
 CASE WHEN ch.StandardCost IS NOT NULL THEN d.LineTotal-d.OrderQty*ch.StandardCost END AS MargeStandardEstimee
FROM SalesOrderDetail d
JOIN SalesOrderHeader h ON h.SalesOrderID=d.SalesOrderID
JOIN Product p ON p.ProductID=d.ProductID
JOIN Customer c ON c.CustomerID=h.CustomerID
LEFT JOIN ProductSubcategory ps ON ps.ProductSubcategoryID=p.ProductSubcategoryID
LEFT JOIN ProductCategory pc ON pc.ProductCategoryID=ps.ProductCategoryID
LEFT JOIN SalesTerritory t ON t.TerritoryID=h.TerritoryID
LEFT JOIN ProductCostHistory ch ON ch.ProductID=d.ProductID
 AND date(h.OrderDate)>=date(ch.StartDate)
 AND (ch.EndDate IS NULL OR date(h.OrderDate)<=date(ch.EndDate));

CREATE VIEW v_ventes_mensuelles AS
SELECT strftime('%Y-%m',OrderDate) AS Mois,SUM(Revenu) AS Revenu
FROM v_ventes GROUP BY strftime('%Y-%m',OrderDate);

CREATE VIEW v_clients_total AS
SELECT CustomerID,SUM(Revenu) AS DepenseTotale,COUNT(DISTINCT SalesOrderID) AS Commandes,
 MAX(date(OrderDate)) AS DerniereCommande FROM v_ventes GROUP BY CustomerID;
