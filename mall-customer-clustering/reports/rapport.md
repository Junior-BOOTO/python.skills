# Rapport — Segmentation exploratoire Mall Customers

## Résultat et choix
K-means à 5 groupes atteint une silhouette moyenne de 0.555, maximum observé parmi k=2..8 sur les mêmes données. Les 200 profils sont décrits par revenu et score standardisés. L’inertie passe de 400 pour un groupe à 65.57 : elle diminue mécaniquement avec le nombre de groupes et ne valide pas seule le choix de k.

K-means est retenu pour sa simplicité, sa couverture complète et l’affectation explicite de profils illustratifs. Ward au même k produit une silhouette de 0,554 et un ARI de 0,942 avec K-means. DBSCAN (eps=0,35, min_samples=5) identifie six groupes et 23 points de bruit : sa silhouette de 0,558 est calculée sur les 177 points regroupés. Ce score n’établit pas sa supériorité sur une méthode couvrant les 200 points.

## Stabilité et sensibilité
Dix graines aléatoires avec 30 initialisations donnent les mêmes groupes (ARI=1). Vingt sous-échantillons sans remplacement de 160 clients réajustent la standardisation et K-means. L’ARI sur les observations communes est en moyenne 0.989, au minimum 0.980. Cela mesure l’accord entre regroupements, pas une précision ni une probabilité de réussite commerciale.

L’ajout de l’âge à k=5 donne un ARI de 0.584 avec la partition primaire. Les choix de variables influencent fortement les groupes. La silhouette en trois dimensions n’est pas une comparaison directe de performance avec la géométrie à deux dimensions.

## Profils descriptifs
| Groupe | Effectif | Revenu moyen (k$, source) | Score moyen |
|---|---:|---:|---:|
| G0 | 22 | 25.73 | 79.36 |
| G1 | 23 | 26.30 | 20.91 |
| G2 | 81 | 55.30 | 49.52 |
| G3 | 39 | 86.54 | 82.13 |
| G4 | 35 | 88.20 | 17.11 |

G0 et G1 ont un revenu moyen voisin mais des scores très différents. G2 couvre le profil intermédiaire majoritaire. G3 et G4 ont un revenu moyen supérieur, avec des scores opposés. Ces descriptions relatives ne justifient pas les étiquettes « loyal », « rentable » ou « à risque » : aucun chiffre d’achat, coût, rétention ou résultat de campagne ne les valide.

## Qualité et protocole
200 identifiants uniques, aucune valeur manquante, aucune répétition exacte de profil complet. Le score est compris entre 1 et 100 ; les données observées couvrent un revenu de 15 à 137 k$ selon le libellé de la source. Le type de dollar et le pays ne sont pas connus. Les variables brutes ne sont ni imputées ni modifiées.

L’identifiant et le genre ne déterminent pas les groupes. L’âge n’entre pas dans la segmentation primaire. Standardisation et clustering sont ajustés à tout le jeu pour une description exploratoire ; aucun test indépendant de performance opérationnelle n’est revendiqué. La standardisation est réajustée dans chaque réplication de stabilité.

## Vérifications et usage
Les tailles de groupes totalisent 200. L’export numérique est rechargé sans pickle et reproduit les 200 affectations. Deux exemples synthétiques illustrent l’affectation au plus proche centroïde avec distance standardisée, sans probabilité inventée.

Une utilisation réelle demanderait une source documentée, un objectif métier mesurable et une validation sur des données indépendantes. Les groupes ne démontrent pas des catégories naturelles. Les données pédagogiques ne garantissent aucune représentativité ni absence de biais. Aucune campagne, communication client ou décision commerciale automatique n’a été lancée.
