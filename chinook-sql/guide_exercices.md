# Guide SQL — Chinook

Chaque exercice contient la requête, son explication et un aperçu des résultats. Les CSV complets sont dans resultats/.

## 1. Clients hors États-Unis

WHERE filtre les lignes avant toute agrégation.

```sql
SELECT CustomerId, FirstName || ' ' || LastName AS Client, Country FROM Customer WHERE Country <> 'USA' ORDER BY Country, Client;
```

Résultat : 46 lignes. Aperçu :

| CustomerId | Client | Country |
| --- | --- | --- |
| 56 | Diego Gutiérrez | Argentina |
| 55 | Mark Taylor | Australia |
| 7 | Astrid Gruber | Austria |
| 8 | Daan Peeters | Belgium |
| 11 | Alexandre Rocha | Brazil |

## 2. Clients brésiliens

Dans cette base, les pays sont écrits en anglais.

```sql
SELECT CustomerId, FirstName || ' ' || LastName AS Client, Country FROM Customer WHERE Country = 'Brazil' ORDER BY Client;
```

Résultat : 5 lignes. Aperçu :

| CustomerId | Client | Country |
| --- | --- | --- |
| 11 | Alexandre Rocha | Brazil |
| 10 | Eduardo Martins | Brazil |
| 13 | Fernanda Ramos | Brazil |
| 1 | Luís Gonçalves | Brazil |
| 12 | Roberto Almeida | Brazil |

## 3. Factures des clients brésiliens

Le pays du client détermine le filtre ; le pays de facturation est affiché séparément.

```sql
SELECT c.FirstName || ' ' || c.LastName AS Client, i.InvoiceId, i.InvoiceDate, i.BillingCountry FROM Customer c JOIN Invoice i ON i.CustomerId=c.CustomerId WHERE c.Country='Brazil' ORDER BY i.InvoiceDate,i.InvoiceId;
```

Résultat : 35 lignes. Aperçu :

| Client | InvoiceId | InvoiceDate | BillingCountry |
| --- | --- | --- | --- |
| Eduardo Martins | 25 | 2021-04-09 00:00:00 | Brazil |
| Roberto Almeida | 34 | 2021-05-23 00:00:00 | Brazil |
| Fernanda Ramos | 35 | 2021-06-05 00:00:00 | Brazil |
| Alexandre Rocha | 57 | 2021-09-06 00:00:00 | Brazil |
| Fernanda Ramos | 58 | 2021-09-07 00:00:00 | Brazil |

## 4. Agents de vente

Filtrer sur le titre exact présent dans les données.

```sql
SELECT EmployeeId, FirstName || ' ' || LastName AS Agent, Title FROM Employee WHERE Title='Sales Support Agent' ORDER BY EmployeeId;
```

Résultat : 3 lignes. Aperçu :

| EmployeeId | Agent | Title |
| --- | --- | --- |
| 3 | Jane Peacock | Sales Support Agent |
| 4 | Margaret Park | Sales Support Agent |
| 5 | Steve Johnson | Sales Support Agent |

## 5. Pays de facturation distincts

DISTINCT élimine les répétitions dans le résultat, sans modifier les sources.

```sql
SELECT DISTINCT BillingCountry FROM Invoice ORDER BY BillingCountry;
```

Résultat : 24 lignes. Aperçu :

| BillingCountry |
| --- |
| Argentina |
| Australia |
| Austria |
| Belgium |
| Brazil |

## 6. Factures par agent

La relation est Invoice → Customer → Employee.

```sql
SELECT i.InvoiceId, i.InvoiceDate, e.FirstName || ' ' || e.LastName AS Agent FROM Invoice i JOIN Customer c ON c.CustomerId=i.CustomerId JOIN Employee e ON e.EmployeeId=c.SupportRepId ORDER BY e.EmployeeId,i.InvoiceId;
```

Résultat : 412 lignes. Aperçu :

| InvoiceId | InvoiceDate | Agent |
| --- | --- | --- |
| 6 | 2021-01-19 00:00:00 | Jane Peacock |
| 7 | 2021-02-01 00:00:00 | Jane Peacock |
| 9 | 2021-02-02 00:00:00 | Jane Peacock |
| 10 | 2021-02-03 00:00:00 | Jane Peacock |
| 11 | 2021-02-06 00:00:00 | Jane Peacock |

## 7. Détails des factures

LEFT JOIN conserve la facture même si un agent n'est pas renseigné.

```sql
SELECT i.InvoiceId, i.Total, c.FirstName || ' ' || c.LastName AS Client, i.BillingCountry, e.FirstName || ' ' || e.LastName AS Agent FROM Invoice i JOIN Customer c ON c.CustomerId=i.CustomerId LEFT JOIN Employee e ON e.EmployeeId=c.SupportRepId ORDER BY i.InvoiceId;
```

Résultat : 412 lignes. Aperçu :

| InvoiceId | Total | Client | BillingCountry | Agent |
| --- | --- | --- | --- | --- |
| 1 | 1.98 | Leonie Köhler | Germany | Steve Johnson |
| 2 | 3.96 | Bjørn Hansen | Norway | Margaret Park |
| 3 | 5.94 | Daan Peeters | Belgium | Margaret Park |
| 4 | 8.91 | Mark Philips | Canada | Steve Johnson |
| 5 | 13.86 | John Gordon | USA | Margaret Park |

## 8. Ventes en 2009 et 2011

Les années sans facture sont conservées avec zéro. La base actuelle ne couvre pas ces années.

```sql
WITH annees(Annee) AS (VALUES ('2009'),('2011')) SELECT a.Annee, COUNT(i.InvoiceId) AS Factures, ROUND(COALESCE(SUM(i.Total),0),2) AS Ventes FROM annees a LEFT JOIN Invoice i ON strftime('%Y',i.InvoiceDate)=a.Annee GROUP BY a.Annee ORDER BY a.Annee;
```

Résultat : 2 lignes. Aperçu :

| Annee | Factures | Ventes |
| --- | --- | --- |
| 2009 | 0 | 0.0 |
| 2011 | 0 | 0.0 |

## 9. Lignes de la facture 37

COUNT compte les lignes ; SUM(Quantity) compte les unités vendues.

```sql
SELECT InvoiceId, COUNT(*) AS Lignes, SUM(Quantity) AS Unites FROM InvoiceLine WHERE InvoiceId=37 GROUP BY InvoiceId;
```

Résultat : 1 lignes. Aperçu :

| InvoiceId | Lignes | Unites |
| --- | --- | --- |
| 37 | 4 | 4 |

## 10. Lignes par facture

GROUP BY produit une ligne par facture.

```sql
SELECT InvoiceId, COUNT(*) AS Lignes, SUM(Quantity) AS Unites FROM InvoiceLine GROUP BY InvoiceId ORDER BY InvoiceId;
```

Résultat : 412 lignes. Aperçu :

| InvoiceId | Lignes | Unites |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | 4 | 4 |
| 3 | 6 | 6 |
| 4 | 9 | 9 |
| 5 | 14 | 14 |

## 11. Morceaux par ligne de facture

Le nom est obtenu grâce à la clé TrackId.

```sql
SELECT il.InvoiceLineId, il.InvoiceId, t.Name AS Morceau FROM InvoiceLine il JOIN Track t ON t.TrackId=il.TrackId ORDER BY il.InvoiceLineId;
```

Résultat : 2240 lignes. Aperçu :

| InvoiceLineId | InvoiceId | Morceau |
| --- | --- | --- |
| 1 | 1 | Balls to the Wall |
| 2 | 1 | Restless and Wild |
| 3 | 2 | Put The Finger On You |
| 4 | 2 | Inject The Venom |
| 5 | 2 | Evil Walks |

## 12. Morceaux et artistes

La chaîne Track → Album → Artist évite une jointure supposée directe.

```sql
SELECT il.InvoiceLineId, il.InvoiceId, t.Name AS Morceau, ar.Name AS Artiste FROM InvoiceLine il JOIN Track t ON t.TrackId=il.TrackId JOIN Album al ON al.AlbumId=t.AlbumId JOIN Artist ar ON ar.ArtistId=al.ArtistId ORDER BY il.InvoiceLineId;
```

Résultat : 2240 lignes. Aperçu :

| InvoiceLineId | InvoiceId | Morceau | Artiste |
| --- | --- | --- | --- |
| 1 | 1 | Balls to the Wall | Accept |
| 2 | 1 | Restless and Wild | Accept |
| 3 | 2 | Put The Finger On You | AC/DC |
| 4 | 2 | Inject The Venom | AC/DC |
| 5 | 2 | Evil Walks | AC/DC |

## 13. Nombre de factures par pays

Chaque ligne Invoice représente une facture.

```sql
SELECT BillingCountry, COUNT(*) AS Factures FROM Invoice GROUP BY BillingCountry ORDER BY Factures DESC,BillingCountry;
```

Résultat : 24 lignes. Aperçu :

| BillingCountry | Factures |
| --- | --- |
| USA | 91 |
| Canada | 56 |
| Brazil | 35 |
| France | 35 |
| Germany | 28 |

## 14. Morceaux par playlist

LEFT JOIN affiche également les playlists vides.

```sql
SELECT p.Name AS Playlist, COUNT(pt.TrackId) AS Morceaux FROM Playlist p LEFT JOIN PlaylistTrack pt ON pt.PlaylistId=p.PlaylistId GROUP BY p.PlaylistId,p.Name ORDER BY Morceaux DESC,p.Name;
```

Résultat : 18 lignes. Aperçu :

| Playlist | Morceaux |
| --- | --- |
| Music | 3290 |
| Music | 3290 |
| 90’s Music | 1477 |
| TV Shows | 213 |
| TV Shows | 213 |

## 15. Catalogue sans identifiants

Choisir explicitement les colonnes évite d'afficher les IDs.

```sql
SELECT t.Name AS Morceau, al.Title AS Album, mt.Name AS TypeMedia, g.Name AS Genre, t.Composer, t.Milliseconds, t.Bytes, t.UnitPrice FROM Track t JOIN Album al ON al.AlbumId=t.AlbumId JOIN MediaType mt ON mt.MediaTypeId=t.MediaTypeId LEFT JOIN Genre g ON g.GenreId=t.GenreId ORDER BY Morceau,Album;
```

Résultat : 3503 lignes. Aperçu :

| Morceau | Album | TypeMedia | Genre | Composer | Milliseconds | Bytes | UnitPrice |
| --- | --- | --- | --- | --- | --- | --- | --- |
| "40" | War | MPEG audio file | Rock | U2 | 157962 | 5251767 | 0.99 |
| "?" | Lost, Season 2 | Protected MPEG-4 video file | TV Shows | None | 2782333 | 528227089 | 1.99 |
| "Eine Kleine Nachtmusik" Serenade In G, K. 525: I. Allegro | Sir Neville Marriner: A Celebration | Protected AAC audio file | Classical | Wolfgang Amadeus Mozart | 348971 | 5760129 | 0.99 |
| #1 Zero | Out Of Exile | MPEG audio file | Alternative & Punk | Cornell, Commerford, Morello, Wilk | 299102 | 9731988 | 0.99 |
| #9 Dream | Instant Karma: The Amnesty International Campaign to Save Darfur | Protected AAC audio file | Pop | None | 278312 | 4506425 | 0.99 |

## 16. Factures et nombre de lignes

Ne pas sommer Total après la jointure : il serait répété pour chaque ligne.

```sql
SELECT i.InvoiceId, i.InvoiceDate, i.Total, COUNT(il.InvoiceLineId) AS Lignes, COALESCE(SUM(il.Quantity),0) AS Unites FROM Invoice i LEFT JOIN InvoiceLine il ON il.InvoiceId=i.InvoiceId GROUP BY i.InvoiceId,i.InvoiceDate,i.Total ORDER BY i.InvoiceId;
```

Résultat : 412 lignes. Aperçu :

| InvoiceId | InvoiceDate | Total | Lignes | Unites |
| --- | --- | --- | --- | --- |
| 1 | 2021-01-01 00:00:00 | 1.98 | 2 | 2 |
| 2 | 2021-01-02 00:00:00 | 3.96 | 4 | 4 |
| 3 | 2021-01-03 00:00:00 | 5.94 | 6 | 6 |
| 4 | 2021-01-06 00:00:00 | 8.91 | 9 | 9 |
| 5 | 2021-01-11 00:00:00 | 13.86 | 14 | 14 |

## 17. Ventes par agent

Sommer les factures à leur granularité originale.

```sql
SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS Agent, ROUND(COALESCE(SUM(i.Total),0),2) AS Ventes FROM Employee e LEFT JOIN Customer c ON c.SupportRepId=e.EmployeeId LEFT JOIN Invoice i ON i.CustomerId=c.CustomerId WHERE e.Title='Sales Support Agent' GROUP BY e.EmployeeId,e.FirstName,e.LastName ORDER BY Ventes DESC,e.EmployeeId;
```

Résultat : 3 lignes. Aperçu :

| EmployeeId | Agent | Ventes |
| --- | --- | --- |
| 3 | Jane Peacock | 833.04 |
| 4 | Margaret Park | 775.4 |
| 5 | Steve Johnson | 720.16 |

## 18. Meilleur agent en 2009

Conserver tous les ex æquo ; une absence de données ne permet pas de nommer un gagnant.

```sql
WITH ventes AS (SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS Agent, ROUND(SUM(i.Total),2) AS Ventes FROM Employee e JOIN Customer c ON c.SupportRepId=e.EmployeeId JOIN Invoice i ON i.CustomerId=c.CustomerId WHERE strftime('%Y',i.InvoiceDate)='2009' GROUP BY e.EmployeeId,e.FirstName,e.LastName) SELECT * FROM ventes WHERE Ventes=(SELECT MAX(Ventes) FROM ventes);
```

Résultat : 0 lignes. Aperçu :

Aucune ligne : aucune donnée disponible pour ce filtre.

## 19. Meilleur agent en 2010

Même méthode, avec un filtre annuel différent.

```sql
WITH ventes AS (SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS Agent, ROUND(SUM(i.Total),2) AS Ventes FROM Employee e JOIN Customer c ON c.SupportRepId=e.EmployeeId JOIN Invoice i ON i.CustomerId=c.CustomerId WHERE strftime('%Y',i.InvoiceDate)='2010' GROUP BY e.EmployeeId,e.FirstName,e.LastName) SELECT * FROM ventes WHERE Ventes=(SELECT MAX(Ventes) FROM ventes);
```

Résultat : 0 lignes. Aperçu :

Aucune ligne : aucune donnée disponible pour ce filtre.

## 20. Meilleur agent global

Comparer les montants agrégés sans supprimer les ex æquo.

```sql
WITH ventes AS (SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS Agent, ROUND(SUM(i.Total),2) AS Ventes FROM Employee e JOIN Customer c ON c.SupportRepId=e.EmployeeId JOIN Invoice i ON i.CustomerId=c.CustomerId GROUP BY e.EmployeeId,e.FirstName,e.LastName) SELECT * FROM ventes WHERE Ventes=(SELECT MAX(Ventes) FROM ventes);
```

Résultat : 1 lignes. Aperçu :

| EmployeeId | Agent | Ventes |
| --- | --- | --- |
| 3 | Jane Peacock | 833.04 |

## 21. Clients attribués par agent

Compter CustomerId et non les factures.

```sql
SELECT e.EmployeeId,e.FirstName || ' ' || e.LastName AS Agent,COUNT(c.CustomerId) AS Clients FROM Employee e LEFT JOIN Customer c ON c.SupportRepId=e.EmployeeId WHERE e.Title='Sales Support Agent' GROUP BY e.EmployeeId,e.FirstName,e.LastName ORDER BY Clients DESC,e.EmployeeId;
```

Résultat : 3 lignes. Aperçu :

| EmployeeId | Agent | Clients |
| --- | --- | --- |
| 3 | Jane Peacock | 21 |
| 4 | Margaret Park | 20 |
| 5 | Steve Johnson | 18 |

## 22. Ventes totales par pays

Le pays de facturation définit ici la dimension géographique.

```sql
SELECT BillingCountry,ROUND(SUM(Total),2) AS Ventes FROM Invoice GROUP BY BillingCountry ORDER BY Ventes DESC,BillingCountry;
```

Résultat : 24 lignes. Aperçu :

| BillingCountry | Ventes |
| --- | --- |
| USA | 523.06 |
| Canada | 303.96 |
| France | 195.1 |
| Brazil | 190.1 |
| Germany | 156.48 |

## 23. Morceau le plus acheté en 2013

Popularité mesurée en unités ; conserver les ex æquo.

```sql
WITH ventes AS (SELECT t.TrackId,t.Name AS Morceau,SUM(il.Quantity) AS Unites FROM Track t JOIN InvoiceLine il ON il.TrackId=t.TrackId JOIN Invoice i ON i.InvoiceId=il.InvoiceId WHERE strftime('%Y',i.InvoiceDate)='2013' GROUP BY t.TrackId,t.Name) SELECT * FROM ventes WHERE Unites=(SELECT MAX(Unites) FROM ventes) ORDER BY TrackId;
```

Résultat : 0 lignes. Aperçu :

Aucune ligne : aucune donnée disponible pour ce filtre.

## 24. Top 5 des morceaux

Exactement cinq lignes ; TrackId départage les ex æquo de façon reproductible.

```sql
SELECT t.TrackId,t.Name AS Morceau,SUM(il.Quantity) AS Unites FROM Track t JOIN InvoiceLine il ON il.TrackId=t.TrackId GROUP BY t.TrackId,t.Name ORDER BY Unites DESC,t.TrackId LIMIT 5;
```

Résultat : 5 lignes. Aperçu :

| TrackId | Morceau | Unites |
| --- | --- | --- |
| 2 | Balls to the Wall | 2 |
| 8 | Inject The Venom | 2 |
| 9 | Snowballed | 2 |
| 20 | Overdose | 2 |
| 32 | Deuces Are Wild | 2 |

## 25. Top 3 des artistes

Les plus vendus sont classés en unités ; le chiffre d'affaires est fourni séparément.

```sql
SELECT ar.ArtistId,ar.Name AS Artiste,SUM(il.Quantity) AS Unites,ROUND(SUM(il.Quantity*il.UnitPrice),2) AS Ventes FROM Artist ar JOIN Album al ON al.ArtistId=ar.ArtistId JOIN Track t ON t.AlbumId=al.AlbumId JOIN InvoiceLine il ON il.TrackId=t.TrackId GROUP BY ar.ArtistId,ar.Name ORDER BY Unites DESC,ar.ArtistId LIMIT 3;
```

Résultat : 3 lignes. Aperçu :

| ArtistId | Artiste | Unites | Ventes |
| --- | --- | --- | --- |
| 90 | Iron Maiden | 140 | 138.6 |
| 150 | U2 | 107 | 105.93 |
| 50 | Metallica | 91 | 90.09 |

## 26. Type de média le plus acheté

La popularité correspond à SUM(Quantity), pas au nombre de références du catalogue.

```sql
WITH ventes AS (SELECT mt.MediaTypeId,mt.Name AS TypeMedia,SUM(il.Quantity) AS Unites FROM MediaType mt JOIN Track t ON t.MediaTypeId=mt.MediaTypeId JOIN InvoiceLine il ON il.TrackId=t.TrackId GROUP BY mt.MediaTypeId,mt.Name) SELECT * FROM ventes WHERE Unites=(SELECT MAX(Unites) FROM ventes);
```

Résultat : 1 lignes. Aperçu :

| MediaTypeId | TypeMedia | Unites |
| --- | --- | --- |
| 1 | MPEG audio file | 1976 |
