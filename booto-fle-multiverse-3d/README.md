# BOOTO FLE MULTIVERSE 3D · V1 — Mission Éco-Cité francophone

**Le monde change quand tu parles.**  
**Auteur : Junior BOOTO Waba · BOOTO AI & DATA INNOVATION LAB · 23 octobre 2026**

> **Statut** : prototype jouable d'une mission. La progression narrative, les dialogues et les bilans ont été testés en navigateur (mode accessible) et avec des tests automatisés. **Le rendu WebGL n'a pas pu être visualisé dans le navigateur de test de ce laboratoire** ; toutefois, une capture du 23 octobre 2026 fournie par l'auteur confirme que la ville 3D s'affiche dans son navigateur. Les commandes et transformations 3D demandent encore une vérification complète sur cet appareil. Aucune application publique sur Render n'est encore confirmée.

## Le principe

Éco-Cité est une petite aventure destinée au FLE, niveau A1 / Grade 5. Le joueur visite **quatre zones** : mairie, quartier, parc, rivière. Il rencontre **trois personnages** (Amina, Nadia, Éric) et choisit un chemin pertinent :

1. **Nettoyage et tri** : les bacs apparaissent et la rivière devient plus propre.
2. **Plantation et protection** : de jeunes arbres et des fleurs apparaissent dans le parc.

L'avancement dépend de **dialogues en français**, non d'un score automatisé de niveau. Un bilan récapitule les phrases employées, les indices consultés et des observations formatives « Je peux… ». Les réponses hors contexte donnent un indice et permettent un nouvel essai, sans impasse.

## Jouer tout de suite — sans installation

Télécharger le fichier **`DEMO_AUTONOME.html`** (inclus dans l'archive ou proposé séparément), puis l'ouvrir dans Chrome, Edge ou Firefox, sur un ordinateur compatible WebGL.

La démo fonctionne sans serveur ni connexion Internet ; l'environnement 3D est généré à partir de géométries procédurales. Si WebGL n'est pas accessible (matériel/politique navigateur), le mode **dialogue alternatif** est disponible.

Contrôles : **WASD / flèches** pour déplacer l'avatar, **E** pour interagir. On peut aussi cliquer sur les destinations à gauche pour accéder directement aux personnages. Sur téléphone, utiliser les boutons tactiles et la navigation par destinations.

## Conception / architecture

- `index.html` : interface responsive, indicateurs et données de mission embarquées (pour une utilisation hors ligne).
- `src/world.js` : **vraie géométrie 3D WebGL native** (maisons, arbres, pont, rivière, avatar, personnages), sans ressource ni CDN externe.
- `src/mission.js` : moteur narratif **pur et déterministe**, testable indépendamment du rendu 3D ; aucune IA générative ni reconnaissance vocale.
- `src/app.js` : interactions, clavier/tactile, dialogue, rapport et synchro des changements visuels.
- `data/scenario.json` : scènes pédagogiques, personnages, lieux, options et critères. Le contenu est aussi embarqué dans l'HTML autonome.
- `tests/mission.test.cjs` : tests des deux chemins, réponse hors sujet, réinitialisation, traces, objectifs.

**Différence avec le cahier des charges technologique initial :** plutôt que React/Three.js, cette première démonstration emploie **WebGL directement**, sans dépendances. Cela garantit un ZIP autonome et facilite la reproductibilité dans un environnement sans accès au registre npm. Une migration future vers React Three Fiber reste une possibilité et **n'est pas présentée comme déjà réalisée**.

## Tests

Node.js 18+ :

```bash
npm test
npm run build
```

La compilation statique crée `dist/` et ne télécharge **aucun paquet**.

## Publication sur Render — Static Site (pas Web Service Python)

1. Ouvrir le tableau de bord Render : **New → Static Site**.
2. Connecter le dépôt `Junior-BOOTO/python.skills` et la branche `main`.
3. Choisir **Root Directory** : `booto-fle-multiverse-3d`.
4. **Build Command** : `npm run build`.
5. **Publish Directory** : `dist`.
6. Créer le site, puis vérifier l'URL fournie par Render et ses interactions.

**Ne pas sélectionner Web Service** pour ce jeu statique, ni modifier les services déjà présents sur Render. Aucun Runtime Python, aucune Start Command, aucune clé API ni variable d'environnement n'est nécessaire. Le dossier contient un `render.yaml` de référence ; le fichier `render.yaml` du **dépôt racine** gère d'autres services, il ne doit pas être remplacé.

## Périmètre et limites

- Prototype solo, avec un seul quartier 3D low-poly, sans textures externes ni audio.
- L'avatar est une forme simple ; les personnages sont des figures géométriques (sans animation faciale).
- Les dialogues sont des choix **préécrits**, et le bilan est **descriptif**, non une mesure certifiée de l'oral ou de l'écrit selon le CECRL.
- **Aucune collecte volontaire de données personnelles** ; état en mémoire uniquement. Les plateformes d'hébergement peuvent néanmoins conserver des journaux techniques.
- Pas de microphone, de chat entre élèves, de comptes, de modèle d'apprentissage automatique, ni de publicité.
- L'utilisation scolaire réelle nécessite revue pédagogique et essai en conditions de classe.

Le code et les décors procéduraux sont des créations du prototype. **Aucune licence de réutilisation n'est accordée par défaut**, sauf choix ultérieur du propriétaire.

Pour une explication étape par étape et les tests de recette, consulter `docs/GUIDE_ENSEIGNANT_ET_RECETTE.md`.