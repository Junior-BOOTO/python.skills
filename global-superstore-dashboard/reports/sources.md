# Source et transformations

- Tableau, **Global Superstore**, archive officielle : https://www.tableau.com/sites/default/files/training/global_superstore.zip
- Source pédagogique officielle décrivant le jeu : https://origin-tableau-www.tableau.com/sites/default/files/getting_started_with_data_es-es.pdf
- Collecte : 11 octobre 2026. Classeur comprenant Orders, Returns et People ; seules Orders et Returns sont utilisées.
- Période : 1 janvier 2011 au 31 décembre 2014. Données d’une entreprise fictive.
- Empreinte SHA-256 du classeur : `manifest.json`.
- Le classeur source ne fournit pas de devise explicite. Les montants restent en UM.
- Les noms de clients, produits individuels et personnes ne sont pas nécessaires au tableau de bord et ne sont pas exportés.
- Conditions de redistribution spécifiques non identifiées : le classeur original n’est pas inclus dans le dépôt ou l’archive du projet. Le script le télécharge depuis la source officielle lorsque demandé.
- Modifications : harmonisation du marché des retours, jointure sur clé composite, agrégation et calcul d’indicateurs. Aucun montant source n’est corrigé.
- Inspiration : *Data Analysis Projects*, Natacha Njongwa Yepnga / LeCoinStat, projet 7. Le PDF original n’est pas redistribué.
