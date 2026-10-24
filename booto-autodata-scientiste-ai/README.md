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
