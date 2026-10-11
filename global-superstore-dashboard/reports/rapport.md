# Rapport — Performances commerciales Global Superstore

## Résultats vérifiés
Période historique : 2011-01-01 au 2014-12-31. 51,290 lignes, 25,072 commandes distinctes et 178,312 unités.

- Ventes : 12,642,501.91 UM.
- Bénéfice fourni par la source : 1,467,457.29 UM.
- Marge globale : 11.61 % (ratio des totaux, pas moyenne des marges de lignes).
- Panier moyen : 504.25 UM.
- Commandes signalées retournées : 1,173, soit 4.68 %.

## Comparaisons descriptives
Le marché au total de ventes le plus élevé est APAC : 3,585,744.13 UM. La catégorie au total de ventes le plus élevé est Technology : 4,744,557.50 UM. Ces totaux dépendent du volume et de la composition des ventes ; ils ne mesurent pas seuls l'efficacité commerciale.

Les tableaux détaillés sont dans analysis/. Les 48 mois sont présents. La courbe représente des totaux mensuels ; un filtre peut laisser des mois sans vente, affichés à zéro.

## Préparation et contrôles
Les champs nécessaires sont présents, les montants finis, les quantités positives et Row ID unique. Les valeurs manquantes des champs géographiques non utilisés, dont Postal Code, ne sont pas imputées.

296 retours utilisaient le marché « United States » tandis que Orders utilise « US ». La correspondance est harmonisée uniquement dans la copie de travail. Les 1 173 retours sont ensuite appariés sans reste. La jointure many-to-one conserve le nombre de lignes de ventes. La clé Market + Order ID évite de mélanger des commandes de marchés différents partageant un identifiant.

Les 6 740 cellules mensuelles gardent les clés internes nécessaires au comptage distinct. Ventes et bénéfices des cellules, des marchés, des régions et des catégories se réconcilient avec les lignes sources. Huit scénarios de filtres sont contrôlés indépendamment entre Python (lignes sources) et JavaScript (cellules agrégées), avec cas combinés et cas vide. Les ratios sur dénominateur nul sont absents, pas infinis.

## Limites
Jeu fictif et historique ; aucun flux temps réel. Devise non documentée : UM. Le bénéfice est une colonne source, sans preuve qu'il représente le résultat net comptable. Les commandes signalées retournées ne donnent pas les quantités remboursées : ventes et bénéfices ne sont pas diminués arbitrairement. Les sommes de commandes distinctes par catégorie ne sont pas un total distinct global.

Le projet propose une version web et un fichier préparé pour import BI. Aucun fichier Power BI ou Tableau natif n'a été créé. Pas de machine learning : les indicateurs descriptifs répondent à la question.
