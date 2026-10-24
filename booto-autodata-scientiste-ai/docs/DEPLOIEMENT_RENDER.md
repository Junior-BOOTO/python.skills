# Déploiement sur Render — BOOTO AutoData Scientiste AI

**Prérequis :** code publié sous `Junior-BOOTO/python.skills/booto-autodata-scientiste-ai`. Le service Render n'est **pas créé automatiquement** par la publication GitHub.

Le dépôt racine contient déjà un `render.yaml` pour un autre projet. **Ne pas remplacer ce fichier** : cela pourrait affecter BOOTO NLP LAB. Utiliser de préférence l'option **New > Web Service** et renseigner :

| Champ Render | Valeur |
|---|---|
| Repository | `Junior-BOOTO/python.skills` |
| Branch | `main` |
| Root Directory | `booto-autodata-scientiste-ai` |
| Runtime / Language | `Python` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python -m streamlit run app/main.py --server.address 0.0.0.0 --server.port $PORT --server.headless true --browser.gatherUsageStats false` |
| Health Check Path | `/_stcore/health` |
| Environment | `PYTHON_VERSION=3.11.11` |
| Compute | `Free` si disponible / acceptable |

**Autre solution :** si le tableau de bord propose de choisir le chemin d'un Blueprint, le fichier `booto-autodata-scientiste-ai/render.yaml` est inclus. Ne pas sélectionner le Blueprint racine destiné à NLP LAB.

1. Ouvrir https://dashboard.render.com/ et cliquer **New > Web Service**.
2. Connecter le dépôt GitHub ; choisir les réglages de la table.
3. Ne coller aucun mot de passe ni secret dans le code ou les commentaires GitHub.
4. Lancer **Create Web Service** (cette opération déploie publiquement une démonstration, à valider par le propriétaire).
5. Examiner les logs : build, puis `Your service is live`.
6. Vérifier `/_stcore/health`, l'interface, et lancer les DEUX scénarios synthétiques sans données personnelles.
7. Récupérer l'URL `https://<nom-unique>.onrender.com` depuis le tableau de bord. **Ne pas deviner le lien.**

**Sécurité :** ne chargez aucune donnée réelle sensible : l'hébergement tiers a ses propres modalités de traitement et de logs. Le service gratuit peut s'endormir. L'application ne possède pas d'authentification utilisateur et ne doit pas stocker d'informations réelles sur un serveur public.

**Dépannage :** `ModuleNotFoundError` → vérifier Root Directory et Build Command ; écran blanc → voir Logs et Start Command ; dépendances incompatibles → vérifier Python 3.11 et le fichier `requirements.txt`.
