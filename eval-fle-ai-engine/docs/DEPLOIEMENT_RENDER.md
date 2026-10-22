# Déploiement sur Render — BOOTO Éval’FLE AI Engine

## Important : ne pas modifier BOOTO NLP LAB

Créer un **nouveau Web Service**, sans réutiliser ni renommer les services BOOTO NLP LAB existants. Le dépôt GitHub commun peut héberger plusieurs services Render avec un répertoire racine et une commande de lancement distincts.

## Depuis le tableau de bord Render

1. Aller sur https://dashboard.render.com/ puis **New → Web Service**.
2. Choisir **Build and deploy from a Git repository**. Autoriser GitHub si nécessaire.
3. Choisir `Junior-BOOTO/python.skills`, branche `main`.
4. Donner le nom de service `booto-eval-fle-ai` (ou tout nom disponible).
5. **Root Directory** : `eval-fle-ai-engine` (exactement).
6. **Build Command** : `python -m pip install -r requirements.txt`.
7. **Start Command** : `python -m streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true --browser.gatherUsageStats false`.
8. Dans **Environment**, ajouter `PYTHON_VERSION` = `3.11.11`. Cette version est celle utilisée pour le contrôle GitHub Actions ; ne pas dépendre du Python par défaut de Render.
9. Choisir la région et le plan adapté (gratuit si Render le propose effectivement).
10. Déployer le service. Attendre la confirmation Render, puis cliquer sur l’URL `onrender.com` **assignée à ce nouveau service**.
11. Vérifier : page d’accueil, bascule Grade 4/5, téléchargements DOCX/PDF, correction anonyme. Ne pas entrer de données réelles d’élèves.

## Alternative : Blueprint autonome

Ce dossier contient un `render.yaml` qui décrit *uniquement* le nouveau service Éval’FLE. Ne **pas remplacer** le `render.yaml` racine du dépôt, qui peut appartenir à BOOTO NLP LAB. Pour déployer via Blueprint, copiez ce fichier sous un nouveau nom racine convenu ou choisissez un chemin Blueprint si votre interface Render le propose, après vérification des paramètres. La voie **New → Web Service** ci-dessus est plus directe et plus sûre.

## Pré-vol

- Le dépôt GitHub doit contenir `eval-fle-ai-engine/app.py`, `src/evalfle`, `data/banque_demo_a1.json`, `requirements.txt`.
- À partir de `eval-fle-ai-engine`, exécuter `python -m pip install -r requirements-dev.txt` puis `python -m pytest -q`.
- Sur GitHub Actions, attendre le statut de `eval-fle-ai-engine-tests.yml` avant déploiement.
- Vérifier `/_stcore/health` après lancement, puis **tester l’interface réellement** (la réponse du healthcheck seule n’est pas suffisante).

## État de publication

La présence de ces instructions ne confirme pas qu’un service Render a été créé. Ne mentionner une URL de déploiement qu’après l’avoir obtenue et testée sur Render.
