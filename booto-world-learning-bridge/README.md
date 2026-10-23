# BOOTO WORLD LEARNING BRIDGE — Proof of concept V0

**Une compétence. Plusieurs langues. Plusieurs façons d’apprendre.**

**Auteur : Junior BOOTO Waba — BOOTO AI & DATA INNOVATION LAB**

## Pourquoi ce démonstrateur ?

Concevoir un concept d’apprentissage international réellement testable dans un navigateur : une mission de résolution de problème environnemental en français A1, avec consignes en français / espagnol / anglais, plusieurs contextes fictifs, une interface visuelle ou essentielle, un choix d’action ayant des conséquences visibles, et un « passeport » de preuves explicables exportable en JSON.

Ceci **n’est pas** un produit éducatif mondial validé ni un diagnostic automatisé. Le niveau A1 est un objectif d’enseignement et non une certification délivrée par la démo. Les formulations en français de la mission sont les mêmes dans les trois langues d’accompagnement. Une intégration des langues minoritaires demandera une production et une relecture humaines.

## Essayer

Ouvrir `index.html` localement dans Chrome, Edge ou Firefox. Aucune installation, clé API, connexion réseau ni compte. Un lien distinct ouvre BOOTO FLE MULTIVERSE 3D sur Render (ce lien requiert Internet).

## Fonctionnalités V0

- Instructions localisées FR / ES / EN ; objectifs FLE en français.
- Trois décors éducatifs *fictifs*, sans prétention d’exactitude culturelle de terrain.
- Deux modes : illustration visuelle SVG ou mode essentiel, avec le même contenu.
- Quatre tâches observables : identifier, demander, proposer, rendre compte.
- Deux actions correctes à la troisième étape, qui modifient la scène.
- Réponses inadéquates, indices, nouvelles tentatives, bilan transparent.
- Export JSON sans identité ; aucune transmission vers un service externe et aucune sauvegarde automatique sur l’appareil.
- Synthèse vocale française optionnelle **selon les voix installées dans le navigateur**.

## Recette fonctionnelle

1. Passer de Français à Español puis English : l'interface et les explications changent ; les répliques françaises restent l'objet d'apprentissage.
2. Choisir « Essentiel » : l'illustration disparaît mais la mission reste accessible.
3. Répondre volontairement mal à la première question, utiliser un indice puis poursuivre.
4. Au choix écologique, sélectionner « nettoyer » ; la rivière devient propre, la poubelle apparaît.
5. Terminer avec une reformulation correspondante et exporter le JSON.
6. Recommencer, choisir « planter » ; de nouveaux arbres apparaissent, puis compléter et exporter.
7. Vérifier que le fichier exporté contient les étapes observées et aucun nom d'élève.

## Limites honnêtes

Pas de modèle d’IA générative, pas d’apprentissage adaptatif psychométriquement validé, pas de comptes, pas de banque de données scolaires, pas de comparaison entre systèmes éducatifs, pas de reconnaissance vocale. Le changement de décor est une maquette illustrative 2D en SVG, **pas un nouveau monde 3D**. Pour une expérience WebGL 3D déjà développée, voir le bouton « Multiverse 3D ».

Les échanges sont des choix guidés, non une mesure de maîtrise du français. Une véritable étude de terrain nécessite enseignants, accessibilité, contenus dans des langues locales relus, consentement parental lorsqu'applicable, minimisation des données et validation scientifique.

## Publication

Site statique autonome : héberger `index.html` (et éventuellement `README.md`) dans un dossier statique. Aucune commande de compilation requise. Si le jeu est conservé dans un mono-dépôt GitHub, il suffit d'utiliser un dossier racine propre au projet.