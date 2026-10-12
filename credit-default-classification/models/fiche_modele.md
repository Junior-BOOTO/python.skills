# Fiche modèle — Classification pédagogique du défaut

Usage : évaluer une régression logistique sur une source publique historique. Aucun accès au crédit, taux, limite, refus ou traitement individuel n’est décidé par ce modèle.

Entrées : 13 montants financiers et six statuts de paiement, ordre et catégories dans `logistique.json`. ID et quatre variables démographiques exclus. La cible est le défaut au mois suivant la fenêtre des historiques. Les données d’entrée doivent être disponibles avant ce mois.

Préparation : StandardScaler sur montants, OneHotEncoder sur les statuts, paramètres appris sur train seulement. Régularisation L2, C=0,1, sélection par AP sur validation. Pas de suréchantillonnage ; déséquilibre abordé avec AP, rappel, précision et seuil.

Séparation : profils financiers identiques gardés ensemble avec StratifiedGroupKFold. Tailles train/validation/test : 17 996 / 6 006 / 5 998. Les proportions de lignes sont approximatives. Les ID distincts ne prouvent pas que toutes les observations sont indépendantes ; seule la répétition exacte de profil est contrôlée.

Seuil : 0,26, maximum F1 sur une grille 0,05–0,95 de validation. Le choix n’intègre pas de coûts de faux positifs ou de défauts manqués, faute d’objectif économique fourni. Aucun ajustement après lecture du test.

Test : ROC-AUC 0,745, AP 0,501, Brier 0,142. Au seuil 0,26 : précision 0,498, rappel 0,527, F1 0,512. 627 défauts manqués et 704 faux positifs. Ces erreurs interdisent de présenter le projet comme un système opérationnel validé.

Export JSON : moyenne, échelle, catégories, coefficients, intercept et seuil. Score = sigmoid(intercept + coefficients × données préparées). Rechargement reproduisant les 5 998 probabilités de test vérifié. Pas de pickle ou joblib externe. Catégorie inconnue : encodage nul, comme dans le pipeline ; situation à examiner avant toute réutilisation.

Calibration : courbe à dix bins quantiles et score Brier examinés, sans recalibration postérieure au test. Une probabilité estimée n’est pas une certitude ni un risque individuel garanti. Pas de validation temporelle, de transfert à d’autres pays ou de calibration indépendante.

Équité : sexe, âge, éducation et situation matrimoniale exclus des entrées ; cela ne garantit pas l’absence d’effet de variables proxy ou de biais de sélection. Audit agrégé descriptif fourni, sans certification d’équité.

Le modèle reste ajusté au train, sans réentraînement sur validation ou test. Aucun service de notation individuelle n’est déployé. Toute utilisation réelle nécessiterait un objectif, une gouvernance et une validation indépendants adaptés.
