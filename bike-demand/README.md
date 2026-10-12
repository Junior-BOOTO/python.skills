# BikeDemand — Junior BOOTO Waba

Prévision calendaire des locations horaires à J+1. Exécution des trois rôles dans un pipeline Python partagé ; aucun appel automatique aux GPT indépendants.

## Source et qualité
UCI Bike Sharing, Hadi Fanaee-T (2013), DOI 10.24432/C5W894, CC BY 4.0. Capital Bikeshare, 2011–2012. Source : https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip
17,379 observations ; 165 heures absentes de la grille. Ces absences sont conservées et ne sont pas remplacées par des zéros. Leur origine n'est pas établie. Les totaux portent sur les heures présentes. Pas de valeurs manquantes dans les lignes observées, ni de doublons d'horodatage. Le fuseau n'est pas explicité dans les CSV : aucune conversion arbitraire.

## Analyse
Profil des jours ouvrés et non ouvrés, évolution mensuelle, sans interprétation causale. Les graphiques décrivent tout l'historique ; le choix de variables et le protocole étaient fixés avant l'entraînement.

## Modélisation
Variables : hr, weekday, mnth, workingday, holiday, yr. Calendrier connu à J+1. Météo réalisée exclue, ainsi que casual, registered, instant et la cible cnt. Aucune variable future ni transformation apprise sur le jeu complet.
Entraînement : janvier 2011–juin 2012 (13003 lignes). Validation : juillet–septembre 2012 (2208). Test final : octobre–décembre 2012 (2168). Comparaison de deux configurations fixées et d'une référence médiane par jour de semaine et heure. Encodage ajusté dans les pipelines. Sélection sur MAE validation, puis réentraînement jusqu'au 30 septembre. Aucun réglage sur le test. Prédictions négatives ramenées à zéro, règle fixée avant évaluation.
Modèle retenu : **Boosting**. MAE test **72.35 locations/heure**, RMSE 111.71, R² 0.693. Référence MAE 79.79 ; gain 9.3 %. Résultats complets : models/resultats.csv.
Export et rechargement vérifiés sur dix observations. Le modèle est un prototype historique, pas un service déployé ni une prévision de la demande actuelle. Le seul trimestre de test ne démontre pas une performance annuelle ; évolution de la demande et météo limitent cette approche calendaire. Les heures absentes peuvent biaiser l'évaluation.

## Reproduction
Python 3.12.14. Installer requirements.txt puis lancer `python pipeline.py`. Le ZIP brut est conservé ; toutes les sorties sont régénérées dans ce dossier. Ne charger que les fichiers joblib de provenance fiable.
