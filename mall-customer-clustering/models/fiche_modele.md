# Fiche modèle — K-means exploratoire

Usage : résumer les profils du petit jeu pédagogique et illustrer l’affectation au centroïde le plus proche. Aucun ciblage commercial validé.

Entrées, dans cet ordre : revenu annuel `Annual Income (k$)` et score `Spending Score (1-100)`. Revenu exprimé en k$ selon le libellé source, type de dollar non précisé ; score de 1 à 100, formule non documentée. Identifiant, genre et âge exclus de l’analyse primaire.

StandardScaler et K-means à 5 groupes, `random_state=42`, `n_init=30`. Centroïdes ordonnés par revenu puis score pour nommer G0 à G4. Les numéros sont des conventions sans ordre de valeur commerciale.

Export `kmeans.npz` : moyenne, échelle, centroïdes dans l’espace standardisé, ordre des variables. Lecture `allow_pickle=False`. Les 200 affectations après rechargement ont été comparées aux originales : identiques. Aucun fichier pickle ou joblib nécessaire.

Silhouette 0,555, DB 0,572. Dix graines donnent le même regroupement (ARI 1). Vingt sous-échantillons de 160 observations, chacun avec standardisation réajustée : ARI commun moyen 0,989, minimum 0,980. Ce contrôle décrit une stabilité sur cet échantillon, pas une performance sur de nouveaux clients.

Ajouter l’âge au même k donne ARI 0,584 : les frontières dépendent du périmètre choisi. Pas de partition de test indépendante, car le projet décrit l’échantillon ; aucun score prédictif hors échantillon annoncé.

L’affectation au centroïde le plus proche n’est pas une probabilité d’achat ni une certitude de comportement. Les points hors du domaine observé nécessiteraient une revue ; l’algorithme peut néanmoins leur attribuer un groupe. Toute utilisation réelle demande objectifs, données et validation adaptés, puis suivi de dérive. Aucun service de décision n’est déployé.
