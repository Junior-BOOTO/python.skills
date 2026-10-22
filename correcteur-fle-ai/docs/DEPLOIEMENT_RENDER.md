# Déploiement indépendant Render — BOOTO Correcteur FLE V1

## Préparation GitHub

Publier le dossier du prototype **dans `Junior-BOOTO/python.skills/correcteur-fle-ai/`** sur la branche `main`. La publication de ce fichier ZIP à elle seule ne met pas l'application en service. Vérifier que `correcteur-fle-ai/app.py`, `correcteur-fle-ai/requirements.txt` et `correcteur-fle-ai/src/correcteur_fle` sont bien présents en ligne.

## Créer un nouveau Web Service dans Render

| Paramètre | Valeur |
| --- | --- |
| Name | `booto-correcteur-fle-ai` |
| Repository | `Junior-BOOTO/python.skills` |
| Branch | `main` |
| Root Directory | `correcteur-fle-ai` |
| Runtime | Python |
| Build | `python -m pip install -r requirements.txt` |
| Start | `python -m streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true --browser.gatherUsageStats false` |
| Environment | `PYTHON_VERSION=3.11.11` |
| Health Check Path | `/_stcore/health` |

Le plan gratuit dépend des conditions du compte. Après `Deploy succeeded · Live`, ouvrir l'URL `onrender.com` fournie par Render et vérifier : choix des deux thèmes, détection, cases d'acceptation/refus, puis téléchargement PDF/Word/TXT. **Ne jamais modifier les services Render existants.**

La V1 n'est pas hébergée par la seule création du ZIP ou du fichier GitHub.
