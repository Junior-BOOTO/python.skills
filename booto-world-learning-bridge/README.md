# BOOTO WORLD LEARNING BRIDGE — V1 immersive

**Une compétence. Plusieurs langues. Plusieurs façons d'apprendre.**

**Auteur : Junior BOOTO Waba · BOOTO AI & DATA INNOVATION LAB**

## Réalisation vérifiable

Cette V1 relie une mission FLE A1 multilingue (FR/ES/EN) **et le véritable Éco-Cité 3D WebGL** dans une même page, avec un passeport d'observations exportable en JSON. Une version autonome du jeu 3D se trouve dans `game/DEMO_AUTONOME.html`. La V1 n'utilise pas d'API payante ni de données d'élèves.

**[Page d'accueil / Démonstration](index.html)** · [Documentation scientifique](RECHERCHE_ET_VALIDATION.md)

1. Lancer `index.html` localement ; faire une mission en français avec une aide en FR, ES ou EN et, facultativement, exporter le passeport.
2. Déplier **« Ouvrir le jeu 3D »** et terminer une mission : Amina → choix nettoyer/planter → Éric/Nadia → mairie.
3. Une fois la mission terminée, les **preuves 3D sont automatiquement transmises au tableau de bord de la page par message local à la fenêtre**, sans transmission réseau ni stockage permanent. Sinon, cliquez sur le bouton « Transmettre ce bilan… » dans le jeu.
4. Vérifier « Mon passeport de compétences partagé » : les trois répliques pertinentes du jeu 3D apparaissent.
5. Cliquer **« Exporter les preuves des deux activités »** : fichier `BOOTO_WORLD_LEARNING_BRIDGE_Passeport_V1_anonyme.json` contenant les activités guidée et 3D.
6. Vérifier l'import : ouvrir la démo 3D de manière autonome, télécharger le passeport JSON puis l'importer dans le Bridge.

Une aide linguistique en FR/ES/EN entoure le jeu 3D ; les dialogues immersifs restent **en français A1**, ce qui est annoncé et assumé. Le changement de contexte fictif affecte la mission guidée 2D ; il ne génère pas un monde 3D culturellement différent.

## Fonctionnement et sécurité

- `src/passport.js` : format versionné `booto.learning-evidence.v1`, contrôle des preuves, liaison entre les activités et fusion anonyme.
- `game/src/mission.js` : règles déterministes et projection du passeport 3D uniquement après la fin du parcours.
- `game/src/app.js` : transmission **postMessage** uniquement au parent, avec bouton de téléchargement local en alternative ; aucun compte ni backend.
- `index.html` : langue d'accompagnement, mission guidée, panneau 3D, import/export et affichage de preuves sans noms.
- `game/src/world.js` : véritable scène WebGL procédurale ; **mode de repli** si WebGL indisponible.
- `tests/passport.test.cjs` : régression des deux parcours, validation et export de données anonymes.

Le parent vérifie l'origine et la fenêtre d'envoi en mode HTTPS, et valide la forme du message avant de l'afficher comme du texte. Les fichiers JSON importés sont limités en taille. **Ne saisissez pas de données nominatives.** L'utilisateur peut vider le passeport 3D et aucun historique automatique n'est enregistré.

## Tester et construire

Avec Node 18+ : `npm test` puis `npm run build`. Une sortie autonome dans `dist/` contient la page principale et le jeu WebGL (aucune dépendance externe).

## Déploiement Render

**Nouveau Static Site**, dépôt `Junior-BOOTO/python.skills`, branche `main`, **Root Directory `booto-world-learning-bridge`**, commande **`npm run build`**, **Publish Directory `dist`**. Aucune variable Python ou clé API. Le fichier `render.yaml` local est une documentation de référence ; **ne pas modifier le Blueprint `render.yaml` racine** utilisé par d'autres applications.

## Limites

Prototype d'ingénierie pédagogique à tester avec des enseignants. Les succès sont des **choix guidés dans deux activités** et non une preuve de maîtrise d'une compétence générale ; aucun niveau CECRL n'est certifié. Pas de reconnaissance vocale ni de diagnostic adaptatif validé ; pas de langues autres que FR/ES/EN. Aucun usage de données réelles d'enfants, aucun mécanisme de sauvegarde, et aucune mesure d'efficacité d'apprentissage réalisée à ce jour.

© 2026 Junior BOOTO Waba.