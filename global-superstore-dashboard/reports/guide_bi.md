# Utiliser les résultats dans Power BI ou Tableau

Exécuter `preparer.py`, puis importer `collected/ventes_preparees.csv`. Le fichier présente une ligne de vente, sans nom de client, avec mois, marché, région, catégorie, segment, clé interne de commande, ventes, bénéfice, quantité et indicateur de retour.

## Indicateurs
- Ventes : somme de `sales`.
- Bénéfice : somme de `profit`.
- Marge : somme de `profit` / somme de `sales`, résultat absent si le dénominateur vaut zéro.
- Commandes : nombre distinct de `order_key`.
- Panier moyen : ventes / nombre distinct de commandes.
- Commandes retournées : nombre distinct de `order_key` parmi les lignes où `returned` est vrai.
- Taux de commandes retournées : commandes retournées / commandes distinctes du périmètre filtré.

Les clés internes ne sont stables que pour cette préparation du jeu. Une commande peut apparaître dans plusieurs catégories ou segments de cellules : ne pas sommer les comptages distincts pour obtenir le total global.

## Vue suggérée
Filtres année (extraite du mois), marché, région, catégorie et segment. Six cartes d’indicateurs, courbe mensuelle ventes ou bénéfice, barres de ventes par région et tableau comparatif par catégorie.

## Export navigateur
Le bouton CSV exporte des **cellules agrégées**. Les colonnes `distinct_orders_in_cell` et `returned_orders_in_cell` ne sont pas additives. Pour recalculer des commandes distinctes à d’autres niveaux dans un outil BI, utiliser le CSV ligne par ligne préparé par Python.

Le script travaille sur une source fixe. Une connexion et une stratégie de rafraîchissement seraient nécessaires pour une alimentation récurrente. Aucun modèle prédictif n’est entraîné pour ce projet descriptif.
