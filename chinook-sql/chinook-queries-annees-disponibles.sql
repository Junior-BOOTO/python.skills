-- Variante de l'exercice 8
WITH annees(Annee) AS (VALUES ('2021'),('2023')) SELECT a.Annee, COUNT(i.InvoiceId) AS Factures, ROUND(COALESCE(SUM(i.Total),0),2) AS Ventes FROM annees a LEFT JOIN Invoice i ON strftime('%Y',i.InvoiceDate)=a.Annee GROUP BY a.Annee ORDER BY a.Annee;

-- Variante de l'exercice 18
WITH ventes AS (SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS Agent, ROUND(SUM(i.Total),2) AS Ventes FROM Employee e JOIN Customer c ON c.SupportRepId=e.EmployeeId JOIN Invoice i ON i.CustomerId=c.CustomerId WHERE strftime('%Y',i.InvoiceDate)='2021' GROUP BY e.EmployeeId,e.FirstName,e.LastName) SELECT * FROM ventes WHERE Ventes=(SELECT MAX(Ventes) FROM ventes);

-- Variante de l'exercice 19
WITH ventes AS (SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS Agent, ROUND(SUM(i.Total),2) AS Ventes FROM Employee e JOIN Customer c ON c.SupportRepId=e.EmployeeId JOIN Invoice i ON i.CustomerId=c.CustomerId WHERE strftime('%Y',i.InvoiceDate)='2022' GROUP BY e.EmployeeId,e.FirstName,e.LastName) SELECT * FROM ventes WHERE Ventes=(SELECT MAX(Ventes) FROM ventes);

-- Variante de l'exercice 23
WITH ventes AS (SELECT t.TrackId,t.Name AS Morceau,SUM(il.Quantity) AS Unites FROM Track t JOIN InvoiceLine il ON il.TrackId=t.TrackId JOIN Invoice i ON i.InvoiceId=il.InvoiceId WHERE strftime('%Y',i.InvoiceDate)='2025' GROUP BY t.TrackId,t.Name) SELECT * FROM ventes WHERE Unites=(SELECT MAX(Unites) FROM ventes) ORDER BY TrackId;