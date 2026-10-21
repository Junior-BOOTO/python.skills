# Architecture technique détaillée — BOOTO NLP LAB V1

**Date : 21/10/2026 — Statut : architecture initiale du prototype**

## 1. Vue d'ensemble

```text
Utilisateur
  |
  v
Streamlit : import CSV et filtres (app/main.py)
  |
  v
Import et validation (ingest.py) ----> statut d'erreur par ligne
  |
  +----> Détection de langue (language.py, langid si installé)
  |
  +----> Traitement de texte (preprocess.py)
  |
  +----> TF-IDF (features.py) ----> mots-clés
  |                    |
  |                    +----> régression logistique (classifier.py)
  |                    |
  |                    +----> cosinus (similarity.py)
  |
  v
Résultats / graphiques / export CSV
```

## 2. Contrat de données

Entrée CSV UTF-8 avec `text` requis ; `document_id`, `language`, `category` optionnels.
Les colonnes `language` et `category` sont des **références**, jamais les prédictions.
Sortie : colonnes originales + `processing_status`, `predicted_language`, `language_method`, `predicted_category`.
Les lignes vides sont identifiées, conservées, exclues des prédictions et comptabilisées comme signalées.

## 3. Séparation des responsabilités

| Composant | Entrée | Sortie | Responsabilité |
|---|---|---|---|
| ingest | chemin/fichier CSV | DataFrame validé | structure et erreurs |
| preprocess | chaîne, code langue | tokens normalisés | normalisation et filtrage |
| language | chaîne | code langue, méthode | détection ou inconnu |
| features | liste de textes | termes et scores TF-IDF | extraction quantitative |
| classifier | corpus annoté | modèle et métriques | entraînement supervisé avec pipeline sans fuite |
| similarity | liste de textes, index | documents voisins | similarité lexicale |
| pipeline | DataFrame, modèle | DataFrame enrichi | orchestration |
| app | données, résultats | interface | visualisation et export |

## 4. Protocoles expérimentaux

- Corpus de départ : 300 phrases **synthétiques** (100 par langue), trois thèmes.
- Split 80/20 stratifié par langue + catégorie lorsque possible, aléa fixé à 42.
- TF-IDF est *dans* le pipeline Scikit-learn pour éviter tout apprentissage sur le jeu de test.
- Classification : régression logistique multiclasses, métriques macro-F1, accuracy, matrice de confusion.
- Similarité : cosinus TF-IDF, **pas de traduction ni embeddings sémantiques**.
- Détection : un package `langid` optionnel au runtime ; secours heuristique de démonstration non certifié.

## 5. Exigences sécurité et confidentialité

- Aucun envoi de documents importés vers une API externe dans le code applicatif.
- Pas de base de données ; stockage temporaire en mémoire pendant la session.
- Limitation UI à 5 Mo par fichier CSV.
- Ne pas intégrer de données personnelles réelles dans le dépôt.
- La gestion effective des données dépend également de l'environnement d'hébergement Streamlit : à vérifier avant déploiement public.

## 6. Parcours d'acceptation V1

Aucune validation sur données réelles indépendante n'a encore été réalisée. Les critères du cahier des charges sont des **cibles**, pas des performances acquises. Les tests automatiques unitaires vérifient les fonctions, pas la généralisation des modèles.

## 7. Backlog immédiat

1. Installer et vérifier `langid` et `streamlit` sur une machine avec Internet ; tester l'interface.
2. Construire un jeu réel ou public sous licence de 300 textes, distinct de la démo.
3. Constituer 60 textes indépendants monolingues et vérifier les 95 % de détection.
4. Effectuer une classification macro-F1 >= 0,75 sur jeu indépendant non synthétique.
5. Ajouter lemmatisation spaCy par langue et renforcer les tests de régression.
6. Mesurer le temps de traitement 300 textes sur un ordinateur de référence (8 Go RAM).
7. Comparer Logistic Regression, Naive Bayes et Linear SVM, documenter les choix.
8. Choisir la licence du dépôt avant publication GitHub.
