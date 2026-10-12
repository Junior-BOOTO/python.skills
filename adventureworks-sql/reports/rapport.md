# Rapport — SQL avancé AdventureWorks

## Périmètre et résultats
Neuf tables commerciales du jeu OLTP officiel Microsoft, à un commit fixé, adaptées à SQLite. Données fictives. 31465 commandes, 121317 lignes, dates du 2022-05-30 au 2025-06-29. Le montant des lignes après remise est 109,846,381.40 UM, hors taxes et fret.

Les 14 exercices calculables et les 3 bonus ont été exécutés. L’exercice 14 est documenté, sans résultat numérique inventé. L’année 2024 demandée est présente dans cette version. « Récent » et « 12 derniers mois » sont ancrés à la dernière date de la base, pas à la date du jour.

## Observations
Bikes représente 94,651,172.70 UM de revenu. Le produit au plus fort revenu est Mountain-200 Black, 38 (4,400,592.80 UM). Ces classements décrivent les ventes cumulées, pas le bénéfice net.

5059 clients ont commandé dans les 90 derniers jours disponibles. Les acheteurs sont segmentés selon leur dépense avec CUME_DIST, et les égalités restent ensemble. 701 clients de la table Customer n’ont pas de commande ; ils sont inclus dans le bonus LEFT JOIN, et exclus de la segmentation des acheteurs.

## Granularité et arrondis
Chaque ligne de la vue de vente correspond à une ligne SalesOrderDetail. Les jointures aux catégories, clients, territoires et coûts ne multiplient pas les 121317 lignes. Les totaux par territoire, catégorie et segment sont rapprochés des détails. Les champs SalesYTD des référentiels ne sont pas substitués à des ventes recalculées sur une période choisie.

Le total SubTotal des en-têtes est 109,846,381.4039 UM. Il diffère du total des lignes d’environ 0.004012 UM : les en-têtes sont arrondis à quatre décimales. La différence maximale par commande est 0.00005000 UM. Les formules des lignes ont été contrôlées en Decimal, sans écart, et les identités TotalDue = SubTotal + TaxAmt + Freight sont vérifiées.

Les sorties CSV sont arrondies à deux décimales pour les montants. Les contrôles de réconciliation utilisent les montants non arrondis avec tolérances documentées dans le code. SQLite utilise REAL pour ces analyses : ce choix ne constitue pas une architecture de comptabilité à précision monétaire fixe.

## Fenêtres et vues
Le calendrier mensuel dense contient 38 mois. Le cumul final est égal au revenu total. La fenêtre de moyenne mobile contient un puis deux puis trois mois au début de la série. L’exercice 12 contient douze lignes pour chaque produit vendu pendant les douze derniers mois calendaires, y compris les zéros. Le rang régional utilise DENSE_RANK et conserve les ex æquo.

Trois vues sont installées : v_ventes, v_ventes_mensuelles et v_clients_total. Elles automatisent les calculs lors de leur consultation ; aucun service planifié ou flux distant n’est configuré.

## Coûts et retours
Le coût standard historique est joint par produit et date de validité, avec bornes de date inclusives. 64 lignes n’ont pas de coût correspondant. Pour l’exercice 15, la marge totale d’un produit est NULL si une partie de ses lignes manque de coût. Le revenu reste disponible. Ce proxy de marge n’intègre pas toutes les charges, les coûts réels ou remboursements et ne représente pas le bénéfice net.

Le taux de retour client nécessiterait une source de quantités retournées liée aux produits et commandes d’origine. Les rebuts de fabrication et annulations ne sont pas des retours clients. L’exercice 14 est donc non calculable, plutôt que déclaré nul.

## Exécution et limites
Intégrité SQLite : ok ; erreurs de clés étrangères : 0. Les dates et fenêtres suivent la version source fixée. Les résultats ne décrivent aucune entreprise réelle. SQL Server n’était pas disponible : seules les requêtes SQLite ont été exécutées. Le guide de migration T-SQL explique les changements de schéma et de dialecte nécessaires.
