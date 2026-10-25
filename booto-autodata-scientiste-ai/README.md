# BOOTO AutoData Scientiste AI — Prototype V1

**Auteur : Junior BOOTO Waba** · BOOTO AI & DATA INNOVATION LAB · Python / Data Science

> **Statut : prototype technique, non validé sur jeux de données réels et non déployé automatiquement sur Render.** L'app exécute réellement une chaîne d'analyse et de Machine Learning Python. Le nom « AI » n'implique pas un agent autonome ni un grand modèle de langage.

## Fonctionnalités

1. Sources locales **CSV UTF-8 / XLSX** (5 Mo, 30 000 lignes, 80 colonnes) et deux démonstrations **100 % synthétiques**.
2. Inspection de la qualité : données manquantes, doublons, schéma, types, valeurs distinctes, aperçu.
3. Analyse exploratoire : descriptifs, distributions numériques ; histogrammes simples.
4. Choix **explicite** de la cible, de la tâche classification/régression et des exclusions.
5. Préparation scikit-learn via `Pipeline` + `ColumnTransformer` : imputation, mise à l'échelle, encodage après séparation train/test.
6. Validation croisée 3 plis sur **train uniquement** pour comparer référence + deux candidats.
7. Test réservé 25 % : F1 macro et accuracy, ou MAE/RMSE/R², et matrice de confusion si classification.
8. Rapport HTML et manifeste JSON exportés en ZIP ; **données et prédictions exclues par défaut**.
9. Tests Python et GitHub Actions ; guide de déploiement Render.

## Démarrer en local

Installer Python **3.11** :

```bash
cd booto-autodata-scientiste-ai
python -m venv .venv
# Sur Windows : .venv\Scripts\activate
# Sur Linux/macOS : source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app/main.py
```

Le navigateur ouvre l'application. Sélectionnez **Démonstration — classification** ou **Démonstration — régression**. Ces données sont artificielles et ne concernent aucune personne réelle.

Lancer les tests :

```bash
python -m pip install pytest
python -m pytest -q
```

## Rapports de démonstration réels sur données synthétiques

- [Classification — rapport HTML](docs/demonstration_classification.html)
- [Régression — rapport HTML](docs/demonstration_regression.html)

Ces rapports sont produits par le moteur Python V1 sur **180 observations générées artificiellement**. Ils prouvent le déroulement des calculs sur ces jeux, **pas la fiabilité sur des données réelles**.

## Déploiement Render

[Guide détaillé](docs/DEPLOIEMENT_RENDER.md). **Important :** le fichier Render du monorepo racine existe déjà pour BOOTO NLP LAB ; ne pas le remplacer. Créer un **nouveau Web Service** avec `Root Directory=booto-autodata-scientiste-ai`, build `pip install -r requirements.txt`, et démarrage Streamlit sur `$PORT`. Une action de confirmation dans votre compte Render reste nécessaire. Aucun lien Render effectif n'est présumé.

## Précautions professionnelles

N'importer aucun dossier sensible (élèves, patients, finances privées) sur une démo hébergée publiquement. Vérifier toutes les autorisations. Le module est destiné à la **formation et à la démonstration** ; pas d'automatisation de décisions administratives ou financières réelles. Aucune prédiction individuelle n'est exportée par défaut. Les données ne doivent jamais être mises sur GitHub.

[Références bibliographiques](docs/REFERENCES_ET_LIMITES.md) · [Déploiement Render](docs/DEPLOIEMENT_RENDER.md)


## Améliorations du parcours après déploiement — 24 octobre 2026

- CSV UTF-8 : détection des séparateurs virgule, point-virgule, tabulation et barre verticale ; rejet des en-têtes vides ou répétés.
- Rejet des valeurs numériques infinies avec un message explicite.
- Protection des imports XLSX : maximum 40 Mo de contenu décompressé avant lecture.
- Exploration d'une variable numérique entièrement vide sans interrompre l'application.
- Aperçu des prédictions du jeu de test ; graphiques réel/prédit et résidus pour la régression.
- Tests Streamlit du parcours complet des deux démonstrations et du cas colonne vide.

Validation locale : **29 tests réussis** avec Python 3.12, pandas 2.2.3,
scikit-learn 1.8.0 et Streamlit 1.66.1. Cette validation ne confirme pas
le déploiement Render ni l'affichage sur téléphone.

### Prochaines étapes

1. Vérifier l'URL réelle Render, la version déployée et les deux démonstrations en ligne.
2. Vérifier le rendu mobile et tester des fichiers réels anonymisés.
3. Ajouter la prédiction sur un nouveau fichier avec contrôle du schéma.
4. Ajouter des explications de modèle calculées sur les données d'entraînement.
5. Préparer clustering et validation temporelle comme parcours distincts.
6. Étudier collecte API, historique persistant et suivi des modèles après validation des besoins d'hébergement.

Ces étapes sont prévues ; elles ne sont pas encore implémentées.


## Comparaison de modèles et validation renforcées

Cinq candidats par tâche : référence, modèle linéaire, variante linéaire
(régularisation Ridge plus forte ou logistique équilibrée), forêt aléatoire et
Extra Trees. Les transformations sont apprises dans chaque pli de validation.
Le choix utilise les scores non arrondis sur entraînement uniquement.
La régression utilise cinq plis ; la classification adapte le nombre de plis
(deux à cinq) aux effectifs d'entraînement. La taille du test est augmentée
si nécessaire pour accueillir toutes les classes.

La table affiche une MAE positive, à minimiser, ou un F1 macro, à maximiser.
Les configurations incompatibles sont bloquées avant calcul avec une aide.
Des doublons conservés déclenchent un avertissement : ils peuvent rendre les
scores optimistes. Leur suppression reste une décision explicite.

Un plus grand choix de modèles ne garantit pas un meilleur score sur de
nouvelles données. La comparaison augmente le temps de calcul. Les cinq plis
ne constituent pas une validation externe, temporelle ou par individu/groupe.
