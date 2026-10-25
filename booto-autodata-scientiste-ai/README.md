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


## Collecte depuis une API ou URL publique

Dans « Collecter API / URL publique », indiquez une URL HTTPS directe et son
format JSON ou CSV. JSON accepte une liste d'objets ou un objet de colonnes
contenant des listes de même longueur. Un chemin tel que `data.results`
permet d'atteindre les observations ; les champs objets sont aplatis.
Les listes dans les cellules sont refusées pour éviter une conversion ambiguë.

Une pagination numérique explicite peut collecter de 1 à 5 pages (paramètre
`page`, par exemple). La collecte n'est pas une recherche automatique sur le
Web et ne garantit pas l'exhaustivité. Les paginations par curseur, liens
`next`, formulaires, pages HTML et interfaces avec connexion ne sont pas
prises en charge dans ce premier connecteur.

Après collecte, diagnostic, analyse, entraînement et rapport utilisent la table
normalisée. Le CSV est téléchargeable. Le manifeste du rapport inclut la date
UTC, le nombre de pages et les empreintes des réponses. Les valeurs des
paramètres d'URL sont masquées ; leur empreinte permet de vérifier une requête
connue, sans stocker ses paramètres en clair.

Limites : 5 Mo au total, 30 000 lignes, 80 colonnes ; temporisations réseau,
lecture bornée et pagination limitée. HTTPS public sur port 443 uniquement,
aucun identifiant ni clé secrète, aucune redirection ni réponse compressée.
Les adresses DNS privées/réservées/multicast sont bloquées ; la connexion est
épinglée à l'adresse validée avec vérification TLS du nom d'hôte.

La collecte est déclenchée par l'utilisateur et conservée dans sa session,
sans planification récurrente. Vérifiez le droit d'utiliser chaque source.
Les tests automatisés couvrent le réseau simulé, les formats, la pagination,
les erreurs, les limites et le parcours collecte → entraînement. Un essai réseau
réel dans cet environnement n'a pas abouti ; le connecteur doit être vérifié
sur une source publique depuis Render après déploiement.


## Notebook et code imprimable

Après entraînement, la section « Code Python et notebook » propose deux exports :
- `.ipynb` : code Python du traitement, explications en français, paramètres de
  l'expérience, versions des dépendances et résultats enregistrés ;
- `.html` : même code avec numéros de lignes et résultats, ouvrable hors ligne
  dans un navigateur puis imprimable avec Ctrl+P ou enregistrable en PDF.

Le notebook reprend les fonctions de lecture, contrôle, diagnostic, préparation,
validation croisée, modèles et rapport. Les imports relatifs internes sont
retirés pour une exécution séquentielle dans un seul notebook. Pour une source
collectée, le code du connecteur est également visible ; aucun nouvel appel
réseau n'est lancé automatiquement pendant la reproduction.

Les données sources et les prédictions individuelles ne sont pas intégrées.
Conservez la source (ou le CSV normalisé téléchargé pour une collecte), à côté
du notebook ; l'empreinte SHA-256 est contrôlée avant analyse. Pour une démo,
le ZIP de rapport avec inclusion explicite de la source permet de récupérer
le CSV nécessaire. Les résultats déjà affichés sont des instantanés de
l'expérience, clairement signalés ; exécuter le notebook les recalcule.

Le notebook s'ouvre dans Jupyter ou un environnement compatible. Les scripts de
l'interface Streamlit et du générateur d'exports ne sont pas reproduits : le
notebook présente le code du traitement de données, pas le code d'hébergement.
