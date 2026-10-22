# Trois démonstrations du portfolio
Préparation du 22 octobre 2026.

1. BOOTO NLP LAB : dépôt autonome https://github.com/Junior-BOOTO/BOOTO-NLP-LAB ; URL communiquée https://booto-nlp-lab-zuvr.onrender.com/ . Disponibilité non confirmée par cette vérification.
2. Global Superstore : tableau de bord existant, dossier global-superstore-dashboard/web.
3. California Housing Lab : formulaire interactif ajouté dans california-housing-regression/web/index.html, calcul local à partir du modèle Ridge exporté.

## Déployer les deux nouvelles démonstrations
Dans Render, créer un Blueprint, choisir Junior-BOOTO/python.skills, branche main, et renseigner le chemin de Blueprint render-portfolio.yaml.
Ce fichier crée uniquement les deux sites statiques supplémentaires. Il ne remplace pas render.yaml et ne recrée pas BOOTO NLP LAB.
Si vous préférez créer deux Static Sites manuellement, reprendre les rootDir, buildCommand et staticPublishPath du fichier.
Après création, vérifier chaque URL attribuée par Render avant de la publier dans le portfolio.

## Contrôles effectués
- Calcul JavaScript comparé à l'exemple synthétique publié : 177523.64292523992 USD, tolérance 1e-7.
- Profil moyen égal à l'interception du modèle ; valeur non finie rejetée.
- Configuration préparée d'après la documentation Render des Blueprints.
- Pas de test navigateur, de validation CLI Render ni d'exécution des tests Python : environnement local indisponible.
- Aucun nouveau déploiement confirmé. Connexion Render requise pour lancer et contrôler la mise en ligne.
