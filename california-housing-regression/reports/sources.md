# Sources et transformation du projet 10

## Données
California Housing, lié à Pace, R. Kelley et Ronald Barry, *Sparse Spatial Autoregressions*, Statistics & Probability Letters, 33:291–297, 1997. Le jeu dérive du recensement américain de 1990, avec une ligne par census block group.

Documentation primaire : https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset

Archive utilisée par le chargeur scikit-learn : https://ndownloader.figshare.com/files/5976036. SHA-256 attendu : `aaa5c9a6afe2225cc2aed2723682ae403280c4a3695a2ddda4ffb5d8215ea681`. La collecte vérifie cette empreinte. Le CSV de travail est comparé aux valeurs dérivées de l’archive.

Transformations déterministes : revenu et âge conservés ; nombre total de pièces et chambres divisé par les ménages ; occupation moyenne = population / ménages ; coordonnées conservées ; cible divisée par 100 000 selon l’interface scikit-learn, puis exprimée en USD de 1990 pour les erreurs du modèle. Le fichier brut et son empreinte sont préservés.

Le libellé MedInc est conservé dans son échelle source. Le projet n’invente pas une conversion monétaire de ce revenu. Les ratios sont des moyennes de zone ; une grande valeur peut provenir d’un petit nombre de ménages plutôt que d’une erreur certaine.

Les droits de redistribution spécifiques de l’archive d’origine ne sont pas précisés dans son fichier domain. Le projet ne redistribue pas cette archive ni le CSV complet : script de récupération, traçabilité et résultats dérivés sont fournis.

## Remplacement de Boston
Le PDF pédagogique propose Boston Housing. La documentation scikit-learn déconseille ce jeu en raison d’une variable construite autour d’hypothèses raciales contestées et cite California Housing et Ames comme alternatives : https://scikit-learn.org/1.0/modules/generated/sklearn.datasets.load_boston.html.

La substitution est explicite : le projet conserve la régression immobilière mais vise une valeur médiane de zone plutôt qu’un prix de bien individuel.

## Inspiration
*Data Analysis Projects*, Natacha Njongwa Yepnga / LeCoinStat, projet 10. Le PDF original n’est pas redistribué. Collecte et calculs : 11 octobre 2026, heure de Bogotá. Les données elles-mêmes décrivent 1990.
