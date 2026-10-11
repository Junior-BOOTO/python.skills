-- EXERCICE 01 : Clients hors États-Unis
-- WHERE filtre les lignes avant toute agrégation.
SELECT CustomerId, FirstName || ' ' || LastName AS Client, Country FROM Customer WHERE Country <> 'USA' ORDER BY Country, Client;

-- EXERCICE 02 : Clients brésiliens
-- Dans cette base, les pays sont écrits en anglais.
SELECT CustomerId, FirstName || ' ' || LastName AS Client, Country FROM Customer WHERE Country = 'Brazil' ORDER BY Client;

-- EXERCICE 03 : Factures des clients brésiliens
-- Le pays du client détermine le filtre ; le pays de facturation est affiché séparément.
SELECT c.FirstName || ' ' || c.LastName AS Client, i.InvoiceId, i.InvoiceDate, i.BillingCountry FROM Customer c JOIN Invoice i ON i.CustomerId=c.CustomerId WHERE c.Country='Brazil' ORDER BY i.InvoiceDate,i.InvoiceId;

-- EXERCICE 04 : Agents de vente
-- Filtrer sur le titre exact présent dans les données.
SELECT EmployeeId, FirstName || ' ' || LastName AS Agent, Title FROM Employee WHERE Title='Sales Support Agent' ORDER BY EmployeeId;

-- EXERCICE 05 : Pays de facturation distincts
-- DISTINCT élimine les répétitions dans le résultat, sans modifier les sources.
SELECT DISTINCT BillingCountry FROM Invoice ORDER BY BillingCountry;

-- EXERCICE 06 : Factures par agent
-- La relation est Invoice → Customer → Employee.
SELECT i.InvoiceId, i.InvoiceDate, e.FirstName || ' ' || e.LastName AS Agent FROM Invoice i JOIN Customer c ON c.CustomerId=i.CustomerId JOIN Employee e ON e.EmployeeId=c.SupportRepId ORDER BY e.EmployeeId,i.InvoiceId;

-- EXERCICE 07 : Détails des factures
-- LEFT JOIN conserve la facture même si un agent n'est pas renseigné.
SELECT i.InvoiceId, i.Total, c.FirstName || ' ' || c.LastName AS Client, i.BillingCountry, e.FirstName || ' ' || e.LastName AS Agent FROM Invoice i JOIN Customer c ON c.CustomerId=i.CustomerId LEFT JOIN Employee e ON e.EmployeeId=c.SupportRepId ORDER BY i.InvoiceId;

-- EXERCICE 08 : Ventes en 2009 et 2011
-- Les années sans facture sont conservées avec zéro. La base actuelle ne couvre pas ces années.
WITH annees(Annee) AS (VALUES ('2009'),('2011')) SELECT a.Annee, COUNT(i.InvoiceId) AS Factures, ROUND(COALESCE(SUM(i.Total),0),2) AS Ventes FROM annees a LEFT JOIN Invoice i ON strftime('%Y',i.InvoiceDate)=a.Annee GROUP BY a.Annee ORDER BY a.Annee;

-- EXERCICE 09 : Lignes de la facture 37
-- COUNT compte les lignes ; SUM(Quantity) compte les unités vendues.
SELECT InvoiceId, COUNT(*) AS Lignes, SUM(Quantity) AS Unites FROM InvoiceLine WHERE InvoiceId=37 GROUP BY InvoiceId;

-- EXERCICE 10 : Lignes par facture
-- GROUP BY produit une ligne par facture.
SELECT InvoiceId, COUNT(*) AS Lignes, SUM(Quantity) AS Unites FROM InvoiceLine GROUP BY InvoiceId ORDER BY InvoiceId;

-- EXERCICE 11 : Morceaux par ligne de facture
-- Le nom est obtenu grâce à la clé TrackId.
SELECT il.InvoiceLineId, il.InvoiceId, t.Name AS Morceau FROM InvoiceLine il JOIN Track t ON t.TrackId=il.TrackId ORDER BY il.InvoiceLineId;

-- EXERCICE 12 : Morceaux et artistes
-- La chaîne Track → Album → Artist évite une jointure supposée directe.
SELECT il.InvoiceLineId, il.InvoiceId, t.Name AS Morceau, ar.Name AS Artiste FROM InvoiceLine il JOIN Track t ON t.TrackId=il.TrackId JOIN Album al ON al.AlbumId=t.AlbumId JOIN Artist ar ON ar.ArtistId=al.ArtistId ORDER BY il.InvoiceLineId;

-- EXERCICE 13 : Nombre de factures par pays
-- Chaque ligne Invoice représente une facture.
SELECT BillingCountry, COUNT(*) AS Factures FROM Invoice GROUP BY BillingCountry ORDER BY Factures DESC,BillingCountry;

-- EXERCICE 14 : Morceaux par playlist
-- LEFT JOIN affiche également les playlists vides.
SELECT p.Name AS Playlist, COUNT(pt.TrackId) AS Morceaux FROM Playlist p LEFT JOIN PlaylistTrack pt ON pt.PlaylistId=p.PlaylistId GROUP BY p.PlaylistId,p.Name ORDER BY Morceaux DESC,p.Name;

-- EXERCICE 15 : Catalogue sans identifiants
-- Choisir explicitement les colonnes évite d'afficher les IDs.
SELECT t.Name AS Morceau, al.Title AS Album, mt.Name AS TypeMedia, g.Name AS Genre, t.Composer, t.Milliseconds, t.Bytes, t.UnitPrice FROM Track t JOIN Album al ON al.AlbumId=t.AlbumId JOIN MediaType mt ON mt.MediaTypeId=t.MediaTypeId LEFT JOIN Genre g ON g.GenreId=t.GenreId ORDER BY Morceau,Album;

-- EXERCICE 16 : Factures et nombre de lignes
-- Ne pas sommer Total après la jointure : il serait répété pour chaque ligne.
SELECT i.InvoiceId, i.InvoiceDate, i.Total, COUNT(il.InvoiceLineId) AS Lignes, COALESCE(SUM(il.Quantity),0) AS Unites FROM Invoice i LEFT JOIN InvoiceLine il ON il.InvoiceId=i.InvoiceId GROUP BY i.InvoiceId,i.InvoiceDate,i.Total ORDER BY i.InvoiceId;

-- EXERCICE 17 : Ventes par agent
-- Sommer les factures à leur granularité originale.
SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS Agent, ROUND(COALESCE(SUM(i.Total),0),2) AS Ventes FROM Employee e LEFT JOIN Customer c ON c.SupportRepId=e.EmployeeId LEFT JOIN Invoice i ON i.CustomerId=c.CustomerId WHERE e.Title='Sales Support Agent' GROUP BY e.EmployeeId,e.FirstName,e.LastName ORDER BY Ventes DESC,e.EmployeeId;

-- EXERCICE 18 : Meilleur agent en 2009
-- Conserver tous les ex æquo ; une absence de données ne permet pas de nommer un gagnant.
WITH ventes AS (SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS Agent, ROUND(SUM(i.Total),2) AS Ventes FROM Employee e JOIN Customer c ON c.SupportRepId=e.EmployeeId JOIN Invoice i ON i.CustomerId=c.CustomerId WHERE strftime('%Y',i.InvoiceDate)='2009' GROUP BY e.EmployeeId,e.FirstName,e.LastName) SELECT * FROM ventes WHERE Ventes=(SELECT MAX(Ventes) FROM ventes);

-- EXERCICE 19 : Meilleur agent en 2010
-- Même méthode, avec un filtre annuel différent.
WITH ventes AS (SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS Agent, ROUND(SUM(i.Total),2) AS Ventes FROM Employee e JOIN Customer c ON c.SupportRepId=e.EmployeeId JOIN Invoice i ON i.CustomerId=c.CustomerId WHERE strftime('%Y',i.InvoiceDate)='2010' GROUP BY e.EmployeeId,e.FirstName,e.LastName) SELECT * FROM ventes WHERE Ventes=(SELECT MAX(Ventes) FROM ventes);

-- EXERCICE 20 : Meilleur agent global
-- Comparer les montants agrégés sans supprimer les ex æquo.
WITH ventes AS (SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS Agent, ROUND(SUM(i.Total),2) AS Ventes FROM Employee e JOIN Customer c ON c.SupportRepId=e.EmployeeId JOIN Invoice i ON i.CustomerId=c.CustomerId GROUP BY e.EmployeeId,e.FirstName,e.LastName) SELECT * FROM ventes WHERE Ventes=(SELECT MAX(Ventes) FROM ventes);

-- EXERCICE 21 : Clients attribués par agent
-- Compter CustomerId et non les factures.
SELECT e.EmployeeId,e.FirstName || ' ' || e.LastName AS Agent,COUNT(c.CustomerId) AS Clients FROM Employee e LEFT JOIN Customer c ON c.SupportRepId=e.EmployeeId WHERE e.Title='Sales Support Agent' GROUP BY e.EmployeeId,e.FirstName,e.LastName ORDER BY Clients DESC,e.EmployeeId;

-- EXERCICE 22 : Ventes totales par pays
-- Le pays de facturation définit ici la dimension géographique.
SELECT BillingCountry,ROUND(SUM(Total),2) AS Ventes FROM Invoice GROUP BY BillingCountry ORDER BY Ventes DESC,BillingCountry;

-- EXERCICE 23 : Morceau le plus acheté en 2013
-- Popularité mesurée en unités ; conserver les ex æquo.
WITH ventes AS (SELECT t.TrackId,t.Name AS Morceau,SUM(il.Quantity) AS Unites FROM Track t JOIN InvoiceLine il ON il.TrackId=t.TrackId JOIN Invoice i ON i.InvoiceId=il.InvoiceId WHERE strftime('%Y',i.InvoiceDate)='2013' GROUP BY t.TrackId,t.Name) SELECT * FROM ventes WHERE Unites=(SELECT MAX(Unites) FROM ventes) ORDER BY TrackId;

-- EXERCICE 24 : Top 5 des morceaux
-- Exactement cinq lignes ; TrackId départage les ex æquo de façon reproductible.
SELECT t.TrackId,t.Name AS Morceau,SUM(il.Quantity) AS Unites FROM Track t JOIN InvoiceLine il ON il.TrackId=t.TrackId GROUP BY t.TrackId,t.Name ORDER BY Unites DESC,t.TrackId LIMIT 5;

-- EXERCICE 25 : Top 3 des artistes
-- Les plus vendus sont classés en unités ; le chiffre d'affaires est fourni séparément.
SELECT ar.ArtistId,ar.Name AS Artiste,SUM(il.Quantity) AS Unites,ROUND(SUM(il.Quantity*il.UnitPrice),2) AS Ventes FROM Artist ar JOIN Album al ON al.ArtistId=ar.ArtistId JOIN Track t ON t.AlbumId=al.AlbumId JOIN InvoiceLine il ON il.TrackId=t.TrackId GROUP BY ar.ArtistId,ar.Name ORDER BY Unites DESC,ar.ArtistId LIMIT 3;

-- EXERCICE 26 : Type de média le plus acheté
-- La popularité correspond à SUM(Quantity), pas au nombre de références du catalogue.
WITH ventes AS (SELECT mt.MediaTypeId,mt.Name AS TypeMedia,SUM(il.Quantity) AS Unites FROM MediaType mt JOIN Track t ON t.MediaTypeId=mt.MediaTypeId JOIN InvoiceLine il ON il.TrackId=t.TrackId GROUP BY mt.MediaTypeId,mt.Name) SELECT * FROM ventes WHERE Unites=(SELECT MAX(Unites) FROM ventes);

