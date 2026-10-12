# Rapport — Régressions immobilières historiques

## Conclusion
Le modèle sélectionné, Ridge_alpha_10, dépasse la référence moyenne sur le test géographique : MAE 56,752.80 USD de 1990 contre 87,191.46, soit une réduction de 34.91 %. RMSE : 83,356.26 ; R² : 0.475. Cela ne constitue ni une précision de 47,5 % ni une garantie sur le marché actuel.

## Population et cible
20 640 census block groups du recensement américain 1990. Les caractéristiques sont des agrégats de zone, pas celles d’un bien individuel. La cible originale MedHouseVal est exprimée en unités de 100 000 USD ; elle est convertie en USD de 1990 pour interpréter les métriques. Les données sont finies et sans valeurs manquantes. Aucune imputation ni suppression automatique d’extrême n’est appliquée.

## Validation et sélection
Cellules de latitude/longitude de 0,5°. GroupShuffleSplit réserve 36 cellules au test et 140 au développement : 5 744 et 14 896 lignes respectivement. La fraction de 20 % s’applique aux cellules, pas aux observations. Les ensembles sont disjoints en cellules ; les cellules voisines peuvent se toucher car il n’y a pas de zone tampon. Le test représente des zones non vues dans cette partition, pas une période future.

Quatre plis GroupKFold sont construits seulement sur développement. Chaque modèle réapprend la standardisation à l’intérieur de son pli. Candidats : référence moyenne, régression simple sur MedInc, multiple sur les huit variables et Ridge α=0,1 / 1 / 10 / 100. Choix fixé à la MAE moyenne minimale, avant l’évaluation finale. Le test sert uniquement au modèle retenu et à la référence, pas au réglage des hyperparamètres.

La MAE moyenne de validation du modèle retenu est 51,829.98, avec un écart-type entre plis de 5,591.97. Cet écart-type n’est pas un intervalle de confiance. Ridge α=10 et la régression multiple non régularisée sont pratiquement à égalité (environ 2,46 USD de différence). Le choix numérique ne démontre pas un avantage substantiel ou statistiquement établi de Ridge.

La priorité donnée à la MAE compte : la régression simple a un RMSE de validation plus faible, mais une MAE plus élevée que le modèle choisi. Il n’y a donc pas de modèle unanimement meilleur sur toutes les métriques. Le R² moyen entre plis est hétérogène et ne doit pas être remplacé par le R² du test.

## Erreurs et restrictions
La MAE sur développement ajusté est 50,112.40, inférieure à celle du test. Les erreurs ne sont pas uniformes selon les valeurs. 992 cibles dans la source sont au plafond de 500 001 USD. Parmi les 354 cas plafonnés du test, la MAE est 161 792,45 USD et le résidu moyen observé−estimé est +116 980,58 : sous-estimation moyenne de ces cas. Les valeurs supérieures au plafond réel ne sont pas observées.

28 prédictions de test sont négatives. Elles sont conservées dans l’évaluation, sans correction décidée après lecture du test. Les graphiques montrent aussi des valeurs estimées extrêmes. Cela rend le modèle inadapté à une estimation opérationnelle sans nouveau travail et nouvelle validation. Une correction, transformation ou modèle alternatif ne devrait pas être choisi en réutilisant ce même test comme validation indépendante.

## Coefficients et interprétation
Les coefficients en unités originales et pour une variation d’un écart-type d’entraînement sont exportés. Ils sont conditionnels aux autres variables du modèle ; colinéarité, agrégation et effets géographiques compliquent leur interprétation. Un coefficient négatif de pièces moyennes ne prouve pas que rajouter une pièce diminue un prix. Aucune causalité n’est démontrée.

## Vérifications et livrables
Checksum de l’archive officiel au chargeur scikit-learn ; transformation comparée au CSV obtenu ; 20 640 lignes ; absence de valeurs manquantes ; cellules disjointes dans le test et les plis ; export JSON complet rechargé et estimations identiques sur les 5 744 cas test.

Le modèle reste ajusté au développement, sans refit sur le test, pour conserver sa concordance avec les résultats. Un profil synthétique assemblé à partir de médianes de développement est proposé comme exemple de réutilisation, sans désigner une maison réelle. Les données de 1990 ne servent pas à prévoir un prix actuel et aucune application commerciale n’est déployée.
