# Rapport — Relations bivariées dans les performances commerciales

## Résultats et portée
51 290 lignes de vente, 25 072 commandes distinctes identifiées par Market + Order ID. Total ventes : 12 642 501,91 UM ; bénéfice source : 1 467 457,29 ; marge agrégée : 11,61 %. 24,46 % des lignes présentent un bénéfice négatif.

L’unité est une ligne de commande. Les distributions et taux décrivent ces lignes ; ils ne sont pas des résultats sur des clients indépendants. Les marchés regroupent des zones et les régions sont comparées avec leur marché pour éviter de confondre les libellés réutilisés.

## Quali-quali : marché et catégorie
Le tableau croisé compte les lignes par marché et catégorie. La version normalisée par ligne mesure la composition de chaque marché : le dénominateur est l’ensemble des lignes de ce marché.

V de Cramér non corrigé = 0,07384, calculé par sqrt(chi² / [n × min(r−1,c−1)]). Il indique ici une association limitée entre ces deux classifications. Le chi² sert au calcul descriptif ; aucune p-valeur de test d’indépendance n’est interprétée sur ces lignes répétées.

## Quali-quanti : catégories et performance
| Catégorie | Lignes | Marge agrégée | Bénéfice médian de ligne (UM) | Lignes négatives |
|---|---:|---:|---:|---:|
| Furniture | 9 876 | 6,94 % | 15,50 | 31,56 % |
| Office Supplies | 31 273 | 13,69 % | 6,55 | 22,39 % |
| Technology | 10 141 | 13,99 % | 29,94 | 23,90 % |

Les différences de médiane, de marge et de taux de perte mesurent des aspects différents. Les volumes, prix et compositions ne sont pas comparables sans contexte supplémentaire. Ces écarts ne sont pas attribués causalement à la catégorie.

## Quanti-quanti : remises et bénéfices
Pearson remise/bénéfice = −0,31649 ; Spearman = −0,59598. Spearman mesure une association des rangs, et non une relation linéaire en unités monétaires. Les corrélations sont calculées sur toutes les lignes.

Dans chaque catégorie, Spearman reste négatif : Furniture −0,681, Office Supplies −0,610, Technology −0,595. Cette stratification descriptive ne neutralise pas tous les facteurs ni ne prouve une causalité.

Les tranches de remise sont fixées à 0 %, ]0,20 %], ]20,40 %] et >40 %. Dans la dernière tranche, 98,43 % des 6 961 lignes ont un bénéfice négatif. Cela ne permet pas de conclure qu’abaisser une remise entraînerait le même changement de bénéfice sur de nouvelles ventes : prix, coûts, produits, sélection des promotions et volume demandé ne sont pas contrôlés. Une partie des associations peut refléter les liens arithmétiques entre vente remisée et bénéfice.

## Graphiques et contrôles
Parts des catégories par marché, heatmap de marge agrégée, matrice de Spearman, nuage remise/bénéfice, boîtes par catégorie et pertes par tranche. Le nuage affiche un échantillon reproductible de 5 000 lignes ; les boîtes ne montrent pas les points hors moustaches. Les données restent intégralement conservées dans les calculs.

SHA-256 de la source vérifié ; champs requis complets ; montants finis ; Row ID uniques ; totaux par catégorie, marché/catégorie, marché/région et tranche réconciliés ; parts par marché égales à 1. Pas d’imputation, suppression d’extrême ou duplication par jointure.

## Limites et suites raisonnables
Données fictives historiques, devise non documentée (UM), bénéfice source non assimilé à un résultat net. Les observations répétées, constructions de variables et mélanges de produits empêchent une inférence causale directe. Pas de recommandations automatiques sur des prix ou clients.

Pour un usage opérationnel, examiner coûts et compositions avec une source documentée et, pour tester l’effet d’une politique de remise, choisir un protocole causal adapté. Aucun modèle prédictif n’est nécessaire pour livrer cette exploration.
