# Fiche modèle — Régression immobilière historique

Usage : exercice d’apprentissage pour estimer la valeur médiane d’une zone du recensement 1990. Pas estimation de maison individuelle, pas outil de prix actuel.

Modèle : Ridge α=10, huit variables dans l’ordre enregistré dans `regression.json`. StandardScaler ajusté sur les 14 896 observations de développement, avec coefficients conservés dans l’espace standardisé.

Test : 5 744 observations appartenant à 36 cellules géographiques distinctes du développement. MAE 56 752,80 USD de 1990 ; RMSE 83 356,26 ; R² 0,475. Référence : moyenne de la cible du développement, MAE 87 191,46. Le test n’a pas servi à sélectionner le modèle, les variables ou α.

Validation : quatre plis par cellules géographiques, sept configurations y compris la référence, choix par MAE. Ridge α=10 et la régression multiple non régularisée diffèrent d’environ 2,46 USD en MAE moyenne, très peu par rapport à la variabilité entre plis : ne pas présenter cela comme un avantage statistiquement établi. La priorité MAE ne sélectionne pas nécessairement le modèle au meilleur RMSE.

Prédiction : `((X - mean) / scale) @ coefficients_standardized + intercept_standardized`. L’export JSON contient toute la transformation nécessaire. Rechargement vérifié sur toutes les lignes de test. Aucun pickle ou joblib externe à charger.

Restrictions : valeur cible plafonnée, erreurs élevées sur le plafond, 28 valeurs négatives sur le test. Pas de correction ou clipping ajouté après consultation du test. Zones adjacentes possibles, absence de tampon spatial et de validation temporelle. Les coefficients ne prouvent pas d’effet causal. Les variables doivent être des caractéristiques agrégées de zone disponibles à l’instant de l’estimation.

Le modèle exporté reste ajusté uniquement au développement pour conserver la concordance avec l’évaluation. Il n’est pas réentraîné sur le test. Aucun service d’estimation immobilière ou décision financière n’est déployé.
