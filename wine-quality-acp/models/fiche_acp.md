# Fiche ACP

Usage : exploration de l’échantillon UCI Wine Quality, visualisation et réduction descriptive des dimensions.

Variables : ordre exact des 11 propriétés dans `analyse.py`. `quality`, `color` et `source_row` sont exclus.

Export : `acp.npz`, tableaux numériques sans pickle. Projection d’un tableau X : `((X - mean) / scale - pca_mean) @ components.T`. Rechargement et projection de cinq lignes vérifiés dans le script. Le fichier contient les 11 axes ; prendre les deux ou trois premiers pour une projection.

Résultats : 50,22 % de variance en 2D ; 64,36 % en 3D ; six axes pour ≥ 80 %. Aucune accuracy ou performance prédictive annoncée.

Restrictions : mélange de types de vins, profils répétés, échantillon non représentatif démontré, absence de clients. Ne pas utiliser comme outil de notation automatique, segmentation de clients ou décision commerciale validée. Aucun service n’a été déployé.
