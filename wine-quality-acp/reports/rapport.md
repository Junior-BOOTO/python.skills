# Rapport — ACP des profils chimiques des vins

## Question et méthode
Quelles dimensions résument les 11 propriétés chimiques des vins ? Chaque ligne est une observation de vin ; les données ne contiennent pas de clients. Les deux CSV UCI sont fusionnés avec la couleur et le numéro de ligne source. Les 6 497 observations sont conservées ; aucune imputation ni suppression de valeur extrême n’est appliquée.

Les variables sont centrées et réduites avant une ACP par décomposition complète (`svd_solver='full'`). La couleur et la qualité sensorielle servent uniquement à annoter la projection, jamais à calculer les axes. Standardiser est nécessaire pour que les différences d’unités ne déterminent pas seules le résultat.

## Qualité et volume
- 1 599 vins rouges et 4 898 vins blancs ; 0 valeur manquante.
- Qualité observée : de 3 à 9 sur une échelle annoncée de 0 à 10.
- 1 177 lignes répètent un profil déjà présent, en comparant toutes les variables, la note et la couleur. Il n’y a pas d’identifiant permettant de distinguer mesures répétées et doublons techniques.

## Résultats exécutés
| Périmètre | Observations | Variance 2D | Variance 3D | Axes pour ≥ 80 % |
|---|---:|---:|---:|---:|
| Tous les vins | 6 497 | 50,22 % | 64,36 % | 6 |
| Profils uniques (sensibilité) | 5 320 | 49,67 % | 64,10 % | 6 |
| Vins rouges seuls | 1 599 | 45,68 % | 59,78 % | 6 |
| Vins blancs seuls | 4 898 | 43,61 % | 54,72 % | 6 |

Les analyses séparées réajustent standardisation et ACP : leurs axes ne sont pas directement identiques à ceux de l’analyse combinée. Le poids des vins blancs est plus important dans l’analyse globale. La proximité des proportions après retrait des profils répétés ne prouve pas la stabilité des positions individuelles.

## Interpréter les axes
Dans l’orientation calculée, PC1 est positivement associé au dioxyde de soufre total (r = 0,848), au dioxyde de soufre libre (0,750) et au sucre résiduel (0,602), et négativement à l’acidité volatile (−0,663). PC2 oppose surtout densité (0,922) et alcool (−0,734), avec des associations positives à l’acidité fixe et au sucre résiduel.

Ces valeurs sont des corrélations empiriques entre les variables standardisées et les coordonnées des composantes, distinctes des coefficients des axes. Une flèche courte dans le plan signale qu’une variable y est moins bien représentée. Le signe d’un axe est arbitraire : on pourrait inverser ensemble coordonnées et corrélations sans changer l’analyse.

La couleur structure une partie du nuage. Cela n’établit pas des catégories naturelles de qualité ; la projection colorée par note n’est ni un classificateur ni une mesure de performance prédictive. Avec 50,2 % de variance conservée, une proximité en 2D peut masquer des différences sur les autres axes.

## Vérifications et limites
Volumes, absence de valeurs manquantes et finitude des données vérifiés. Somme des proportions de variance égale à 1 ; reconstruction des données standardisées par les 11 axes vérifiée. Export NPZ rechargé avec `allow_pickle=False` et projection de cinq observations comparée à l’original.

Pas de partition entraînement/test : l’objectif est une description de cet échantillon, pas la généralisation à des vins futurs. Pour une future prédiction, repartir des données brutes et réestimer tout prétraitement dans l’entraînement uniquement. Les données ne décrivent pas prix, marques, cépages ou clients ; aucune conclusion sur la rentabilité ou la segmentation commerciale n’est possible. Les associations ne prouvent pas une causalité.
