# Rapport — Prévoir les ventes mensuelles à six mois

La méthode saisonnière avec dérive atteint au test une MAE de **71 957,90 UM**, contre **111 964,14** pour la référence saisonnière, réduction de **35,73 %**. RMSE : 80 649,67 contre 120 991,43 ; WAPE : 16,12 % contre 25,09 %.

## Périmètre et qualité
48 mois consécutifs, uniques, sans absence, ventes positives et finies. Total : 12 642 501,90988 UM, identique au projet source Global Superstore. Le montant est une somme mensuelle, pas une moyenne ou un revenu actuel. Profit est présent dans la source agrégée mais n’est pas utilisé comme prédicteur des ventes.

## Validation
Origines fin décembre 2012, fin juin 2013 et fin décembre 2013, horizons six mois ; apprentissage croissant de 24, 30 puis 36 mois. Les ventes futures de chaque fenêtre ne servent pas au fit. Les mois de validation ne se chevauchent pas. Le test juillet–décembre 2014 reste mis à part, fit sur 42 mois.

Quatre configurations fixées : dernière valeur, même mois de l’année précédente, même mois plus moyenne des différences annuelles, et SARIMA (0,1,1)×(0,1,0,12). Le choix se fait sur la MAE moyenne de validation. Pas de recherche de modèle ou réglage supplémentaire sur le test.

La méthode retenue obtient en validation une MAE moyenne de 26 212,29 UM, écart-type entre trois fenêtres de 6 476,89. Le saisonnier simple obtient 52 813,46 et le SARIMA 54 171,15. Avec seulement trois fenêtres, l’écart-type n’est pas un intervalle de confiance. Le modèle plus complexe ne dépasse pas les références utiles dans ce protocole.

## Test et limites
Seuls méthode retenue et témoin saisonnier sont évalués sur les six derniers mois. La MAE du test est nettement supérieure à la MAE de validation : l’erreur n’est pas stable à travers les périodes. Cela peut refléter l’évolution des ventes et de leurs différences annuelles, mais aucune cause commerciale n’est démontrée.

WAPE = somme des erreurs absolues / somme des ventes observées. Toutes les ventes de cette série sont positives ; les règles de gestion de zéros ou de retours nets seraient à revoir sur d’autres sources. Le WAPE ne doit pas être converti en pourcentage de précision individuelle.

## Prolongement 2015 et export
Après le test, refit sur 48 mois puis prévision de janvier à juin 2015. Ces ventes futures ne sont pas connues dans le fichier : il s’agit d’un prolongement historique fictif, sans score réalisé sur 2015. Le fit final n’est pas le fit ayant produit le test.

JSON exporté : méthode, historique, dernière date, horizon et unités. Le rechargement reproduit les six valeurs prévues. Pas d’intervalle probabiliste affiché pour la méthode retenue ; les erreurs de validation ne sont pas transformées en couverture garantie.

Le script vérifie calendrier, total, convergence du SARIMA comparé et reproduction numérique de la prévision. Aucun modèle n’est présenté comme exécuté sans l’être.

## Source et portée
Source mensuelle du projet 7, issue du classeur officiel Tableau Global Superstore. Remplacement documenté de la source Store Sales proposée dans le PDF. Série fictive 2011–2014, quatre cycles annuels seulement. Pas données opérationnelles actuelles, facteurs externes, promotions ou stocks. Aucune tâche automatique de rafraîchissement ni prévision intersessions n’est configurée.
