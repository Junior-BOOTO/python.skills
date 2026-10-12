# Rapport — Classification du défaut de paiement

## Résultat
Régression logistique C=0.1, sélectionnée par Average Precision sur validation. Sur 5998 cas test : ROC-AUC 0.745, AP 0.501, Brier 0.142. Au seuil 0.26, fixé par maximum F1 de validation, précision 0.498, rappel 0.527, F1 0.512.

La référence ne détecte aucun défaut (rappel et F1 nuls), malgré une accuracy de 77.89 %. Sa probabilité constante est la prévalence d’apprentissage ; son AP test est 0.221. L’AP est la moyenne des précisions pondérée par les incréments de rappel, pas une aire PR trapézoïdale présentée abusivement comme identique.

## Données et cadrage
Jeu public UCI, Taïwan, historiques avril–septembre 2005. Cible : défaut au mois suivant. 30 000 lignes, 6 636 défauts, soit 22,12 %. Aucune valeur manquante, ID uniques. Les ID, le sexe, l’âge, l’éducation et le statut marital n’entrent pas dans le modèle. Les 19 entrées financières doivent être disponibles avant le mois cible.

Les 817 profils financiers répétés sont conservés et placés dans le même ensemble, même si leurs cibles diffèrent. Le fait que deux profils soient identiques ne permet pas d’affirmer que ce sont des doublons techniques. Les quasi-doublons ou relations entre personnes ne peuvent pas être vérifiés avec cette seule source.

## Validation
StratifiedGroupKFold sépare par profils : train 17996 (22.11 % défauts), validation 6006 (22.16 %), test 5998 (22.11 %). Les ensembles ont des groupes disjoints. Les proportions correspondent approximativement à 60/20/20, sans supposer que la stratification de groupes produit une fraction exacte.

StandardScaler sur 13 montants et OneHotEncoder sur six statuts, ajustés sur train uniquement. C=0,1, 1 et 10 sont comparés sur validation. C=0,1 est retenu par AP (Brier en second critère si égalité). Le seuil est recherché sur une grille 0,05–0,95 de validation pour maximiser F1 ; les égalités privilégient le seuil le plus élevé. Aucun coût économique n’étant défini, ce seuil reste une convention pédagogique.

Le modèle et le seuil ne changent pas après consultation du test. Les matrices, la calibration et l’audit agrégé de test servent à évaluer les limites, pas à régler une seconde version. Le modèle exporté reste appris sur train seulement.

## Compromis de seuil sur le test
| Seuil | Vrais positifs | Faux négatifs | Faux positifs | Vrais négatifs | Précision | Rappel | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0,50 | 463 | 863 | 257 | 4415 | 0.643 | 0.349 | 0.453 |
| 0.26 | 699 | 627 | 704 | 3968 | 0.498 | 0.527 | 0.512 |

Le seuil inférieur détecte 236 défauts supplémentaires et génère 447 faux positifs supplémentaires. Les erreurs restent nombreuses. Son accuracy (77.81 %) est légèrement inférieure à celle de la référence majoritaire ; le F1 et le rappel décrivent des dimensions que cette accuracy masque.

## Probabilités et calibration
Les probabilités logistiques brutes sont comparées aux fréquences observées dans dix bins quantiles. Le Brier est inférieur à celui de la référence (0.172), mais les fréquences ne suivent pas exactement les probabilités. L’erreur absolue moyenne entre bins pondérée par leurs effectifs est 0.025 ; ce diagnostic dépend du découpage en bins et n’est pas une garantie de calibration individuelle. Aucun recalibrage n’est ajusté sur le test.

## Audit et interprétation
L’audit par sexe utilise ce champ uniquement après la prédiction, pour des statistiques agrégées. Au seuil fixé, le rappel vaut environ 51,3 % dans le code source 1 et 53,9 % dans le code 2 ; les prévalences diffèrent également. Ces écarts descriptifs ne certifient ni équité ni discrimination et n’ont pas d’intervalle d’incertitude calculé ici. Les variables financières peuvent rester corrélées à des facteurs démographiques. Aucun seuil différencié par sexe n’est appliqué.

Les coefficients portent sur les log-odds, conditionnellement aux autres entrées et à leurs encodages. Ils ne démontrent pas des causes de défaut. Les catégories −2 et 0 des statuts ne sont pas explicitement définies dans la description UCI ; elles sont conservées distinctes, sans interprétation ajoutée.

## Vérifications et limites
Archive et empreinte vérifiées, volumes et plages, séparation des profils, convergence du modèle, matrices totalisant 5998 cas, export JSON reproduisant toutes les probabilités test. L’exemple local emploie un profil entièrement inventé.

Pas de test temporel, de source externe, de validation économique ou réglementaire. Le jeu de 2005 ne représente pas une population actuelle. Le portfolio publie des résultats agrégés et un explorateur de seuils sur validation, sans dossiers clients, notation individuelle en ligne, décision d’éligibilité ou conseil de crédit.
