# Analyse et modèle — Réanalyse météo Bogotá 2025

## Analyse descriptive
365 jours complets, sans valeur absente. Température quotidienne moyenne annuelle 14.51 °C ; minimum et maximum des moyennes quotidiennes 12.6 et 16.5 °C. Ces valeurs ne sont pas des minima et maxima horaires.

Précipitations cumulées 1424.3 mm ; 270 jours avec au moins 1 mm. Ce seuil définit les jours pluvieux de cette analyse, pas une vérité universelle. Avril est le mois le plus humide, 227.1 mm. Spearman température/pluie = -0.030 : relation monotone faible, sans démonstration causale.

Les valeurs proviennent de la réanalyse ERA5 par Open-Meteo. Coordonnées demandées : 4,7110, −74,0721 ; grille renvoyée : 4,75, −74,00, altitude 2 557 m. Ce n’est pas une mesure directe de station à une adresse de Bogotá. Fuseau America/Bogota, unités °C/mm.

## Objectif et protocole
Estimer la température moyenne quotidienne du lendemain (J+1) à partir des sept jours précédents et du calendrier connu. Les sept premiers jours ne peuvent pas former un historique complet : 358 observations utilisables.

Dates cibles : apprentissage du 8 janvier au 31 juillet (205), validation août–septembre (61), test octobre–décembre (92). Les dates sont ordonnées et disjointes. Les moyennes et retards météo sont décalés avant calcul, sans variable du jour cible. Standardisation apprise sur apprentissage uniquement.

Références : température du jour précédent (persistance) et moyenne d’apprentissage. Huit Ridge comparés : alpha 0,1 / 1 / 10 / 100, avec ou sans calendrier sin/cos. Choix par MAE de validation, référence simple privilégiée si elle est à moins de 1 % du meilleur. Modèle choisi : Ridge_retards_calendrier_alpha_100. Aucun réglage sur le test.

## Résultats
| Ensemble / méthode | MAE °C | RMSE °C | R² |
|---|---:|---:|---:|
| Modèle, apprentissage ajusté | 0.399 | 0.497 | 0.468 |
| Modèle, validation | 0.373 | 0.474 | -0.016 |
| Modèle, test | 0.340 | 0.449 | 0.468 |
| Persistance, test | 0.391 | 0.491 | 0.363 |

Gain de MAE face à la persistance : 13.05 %. Le biais moyen cible−estimé sur test est +0.074 °C. La corrélation de retard 1 des résidus test est 0.215 : les erreurs peuvent être dépendantes. Pas d’intervalle de confiance calculé, pas de significativité ou garantie de gain futur annoncée.

R² légèrement négatif sur validation malgré une MAE meilleure que la persistance : les métriques décrivent des aspects différents et la variabilité varie selon la période. R² n’est pas une accuracy. Les tableaux par mois et graphiques d’erreurs sont inclus.

Le test effectue des estimations quotidiennes à un jour ; la température de la veille du test devient disponible dans l’historique du jour suivant. Il ne prédit pas trois mois d’un seul bloc.

## Export et limites
Export JSON rechargé, les 92 estimations reproduites. Modèle conservé tel qu’évalué, sans refit sur validation ou test. Le code predire.py illustre sa réutilisation ; aucune observation du lendemain demandé n’est utilisée.

Une année et une seule grille ne suffisent pas à valider une méthode climatologique ou opérationnelle. ERA5 est une réanalyse rétrospective : disponibilité des données à l’instant réel d’une décision non vérifiée. Pour une vraie prévision, utiliser des entrées disponibles à l’heure d’émission, plusieurs années et une validation indépendante contre des observations appropriées. Aucun modèle de pluie, alerte météo, intervalle probabiliste garanti ou connexion installée dans les GPT n’est annoncé.
