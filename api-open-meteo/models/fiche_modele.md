# Modèle pédagogique — Température moyenne à J+1

Ridge, alpha 100, entrées : température de la veille et de l’avant-veille, moyennes des trois et sept derniers jours, précipitations de la veille et moyenne des trois jours, sinus et cosinus du jour de l’année cible. Tous les champs météo proviennent de dates strictement antérieures à la cible ; le calendrier cible est connu à l’avance.

Standardisation ajustée sur 205 jours cibles du 8 janvier au 31 juillet 2025. Sélection sur 61 jours d’août–septembre, comparaison à la persistance et à la moyenne train. Test final de 92 jours, octobre–décembre. Le modèle reste appris sur train : il n’est pas réentraîné sur le test.

Test : MAE 0,340 °C, RMSE 0,449 °C, R² 0,468. Persistance : MAE 0,391 °C, RMSE 0,491 °C. Gain de MAE 13,0 %. R² n’est pas un pourcentage de précision et cette différence n’a pas d’intervalle d’incertitude calculé.

Le test est une succession de prévisions à un jour : les observations passées du trimestre de test servent de retards au jour suivant. Ce n’est pas une prévision unique des 92 jours faite fin septembre.

Export JSON complet, sans pickle : ordre des variables, moyenne, échelle, coefficients, intercept, source et périodes. Rechargement vérifié sur toutes les 92 estimations de test. Les coefficients sont des associations conditionnelles, pas des effets causaux.

Limites : une seule année, une grille ERA5, réanalyse rétrospective et températures quotidiennes arrondies dans la réponse API. Les données peuvent ne pas avoir été accessibles à l’heure où une vraie prévision aurait été émise. Ce protocole ne valide donc pas une qualité de prévision opérationnelle, ni un transfert à d’autres années ou lieux. Aucun intervalle de prédiction fiable, système d’alerte ou service temps réel n’est fourni.
