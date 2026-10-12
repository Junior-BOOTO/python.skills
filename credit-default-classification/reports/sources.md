# Sources, unités et collecte

Yeh, I. (2009). **Default of Credit Card Clients [Dataset]**. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H.

Fiche primaire : https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients

Archive : https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip

SHA-256 vérifié : `56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602`.

Licence UCI : **Creative Commons Attribution 4.0 International**, https://creativecommons.org/licenses/by/4.0/. Attribution conservée pour les résultats dérivés. Le portfolio publie le code, le modèle et les résultats agrégés ; il n’expose pas les dossiers financiers ligne par ligne.

Article associé : I-Cheng Yeh et Che-hui Lien, *The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients*, Expert Systems with Applications, 2009.

Données historiques de Taïwan. Les statuts, relevés et paiements couvrent avril à septembre 2005 ; la cible est le défaut au mois suivant. Montants de crédit, relevés et paiements en nouveaux dollars taïwanais (NT$), selon la description UCI. Le fichier ne permet pas une validation sur plusieurs fenêtres temporelles successives.

Le script lit la deuxième ligne comme en-tête, conserve le fichier original, vérifie dimensions et ID, puis exclut cinq variables des entrées du modèle : ID, SEX, EDUCATION, MARRIAGE, AGE. Les variables de sexe sont consultées uniquement pour un audit statistique agrégé après évaluation. Aucun seuil différent par sexe n’est appliqué.

Les statuts de paiement sont traités comme catégories. Les valeurs −2 et 0 ne sont pas définies dans la description UCI et ne sont pas recodées arbitrairement. Les montants négatifs de relevés sont conservés, sans les assimiler automatiquement à une erreur.

Inspiration : *Data Analysis Projects*, Natacha Njongwa Yepnga / LeCoinStat, projet 11. Le PDF original n’est pas redistribué. Collecte et calculs : 11 octobre 2026, heure de Bogotá ; données historiques 2005.
