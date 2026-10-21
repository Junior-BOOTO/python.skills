# Déploiement de BOOTO NLP LAB sur Streamlit Community Cloud

**Statut : configuration GitHub préparée ; aucune URL publique Streamlit confirmée.**

## Paramètres à saisir

Dans l'espace [Streamlit Community Cloud](https://share.streamlit.io/), connecter le compte GitHub autorisé puis sélectionner **Create app** → **Yup, I have an app**.

| Champ Streamlit | Valeur |
| --- | --- |
| Repository | `Junior-BOOTO/python.skills` |
| Branch | `main` |
| Main file path | `booto-nlp-lab/app/main.py` |
| Python version (Advanced settings) | `3.11` |
| App URL | Laisser attribuer automatiquement, ou choisir un sous-domaine disponible |

Le fichier `booto-nlp-lab/app/requirements.txt` est volontairement installé **à côté du point d'entrée**, car Streamlit Community Cloud le recherche à cet emplacement, ou à la racine du dépôt GitHub (qui contient d'autres projets). Ne pas confondre avec `booto-nlp-lab/requirements.txt`, prévu pour l'exécution locale.

**Après le clic Deploy :** vérifier que les données d'exemple s'affichent, tester l'import CSV, les quatre onglets, le téléchargement CSV et consulter les logs en cas d'erreur. Ne pas affirmer que l'app est disponible tant que son URL n'est pas vérifiée.

## Test local

Depuis `booto-nlp-lab/` :

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app/main.py
```

## Critères avant d'afficher une démonstration publique

- Le site charge son corpus synthétique d'exemple.
- Aucun message d'erreur critique au chargement.
- Langues, thèmes, mots-clés, similarité et CSV fonctionnent.
- L'encadré « prototype expérimental » reste visible et ne laisse pas penser que les performances sont certifiées.
- La politique de confidentialité impose d'utiliser uniquement des textes dont l'utilisateur possède les droits.

## Après publication

Ajouter l'URL Streamlit réellement obtenue dans `README.md` et dans la rubrique Python / NLP du portfolio professionnel. Aucun lien d'application n'est inventé à l'avance.

## Documentation de la plateforme

- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
