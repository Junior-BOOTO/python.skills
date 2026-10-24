# Checklist de validation — BOOTO AutoData Scientiste AI

## Réalisé et testé localement (moteur Python)

- [x] Chargement CSV UTF-8 et XLSX avec validation taille et dimensions.
- [x] Deux scénarios 100 % synthétiques.
- [x] Profil qualité + choix de la cible et des exclusions.
- [x] Préparation intégrée aux pipelines et sélection par validation croisée sur TRAIN.
- [x] Baseline + 2 familles de candidats ; évaluation sur jeu de test réservé.
- [x] Rapport HTML et manifeste ZIP sans données sources par défaut.
- [x] Tests unitaires et intégration du moteur : 16 tests réussis le 24 octobre 2026 dans l'environnement de développement.

## À vérifier après installation de Streamlit et sur Render

- [ ] Serveur Streamlit démarre et répond sur la page d'accueil.
- [ ] Classification : sélection de la cible `categorie_fictive`, validation humaine, entraînement et export ZIP.
- [ ] Régression : sélection de la cible `montant_simule`, entraînement et vérification MAE/RMSE/R².
- [ ] Import CSV et XLSX réels *non sensibles* et gestion des erreurs.
- [ ] Navigation mobile, temps d'entraînement et usage mémoire du plan hébergé.
- [ ] Tests GitHub Actions verts pour le commit publié.
- [ ] URL externe Render effectivement reçue puis vérifiée.

## Évolutions prévues (pas en V1)

API de collecte, clustering, séries temporelles, vision par ordinateur, suivi MLflow, versions de modèles, surveillance drift, réentraînement et authentification.
