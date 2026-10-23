# BOOTO FLE MULTIVERSE 3D
## Cahier des charges fonctionnel, pédagogique et technique — Version 1.0

**Projet :** Mission Éco-Cité francophone  
**Signature :** « Le monde change quand tu parles. »  
**Auteur et porteur du projet :** Junior BOOTO Waba  
**Laboratoire :** BOOTO AI & DATA INNOVATION LAB  
**Date :** 23 octobre 2026  
**Statut :** document de conception approuvé pour cadrer un prototype ; application 3D non encore réalisée  
**Public pilote :** Grade 5, FLE A1, avec extension envisagée vers Grade 4 A1 et A2

> **Vision.** Concevoir une aventure 3D dans laquelle la réussite d'une mission dépend de la communication en français : demander, comprendre, proposer, choisir et expliquer. Le monde virtuel réagit aux actes de langage et garde la trace des décisions de l'apprenant.

## 1. Résumé exécutif

BOOTO FLE MULTIVERSE 3D est un projet de jeu sérieux accessible depuis un navigateur. Dans la première mission, l'apprenant explore une **Éco-Cité francophone** fictive et prend part à la restauration d'un quartier. Trois personnages lui présentent des informations, des contraintes et des possibilités d'action. Les dialogues sont courts, illustrés, à embranchements et adaptés au niveau A1. Le joueur peut choisir plusieurs solutions recevables : organiser le tri, protéger les arbres, ou interroger les habitants avant d'agir.

La particularité recherchée est l'association **communication → décision → conséquence visible → rétroaction pédagogique**. Le but n'est pas de récompenser mécaniquement une unique phrase correcte, mais de rendre observables la pertinence communicative et les effets de choix différents. Les effets dans le décor (rivière plus propre, bacs de tri installés, jeunes arbres plantés) sont générés par un moteur de règles déterministe. Un véritable modèle d'IA générative **ne fait pas partie de V1**.

La première version est un **vertical slice**, c'est-à-dire une mission courte mais intégralement jouable, plutôt qu'un vaste univers vide. Elle est pensée pour être montrée à des employeurs et testée pédagogiquement avant toute affirmation d'efficacité.

## 2. Objectifs et indicateurs de réussite

### 2.1 Objectif général

Permettre à un apprenant A1 de résoudre un problème collectif simulé en mobilisant le français pour comprendre une situation, interagir avec des personnages, faire des choix et formuler des actions concrètes.

### 2.2 Objectifs d'apprentissage — « Je peux… »

- **Compréhension écrite :** Je peux comprendre des consignes et de courts dialogues de mission contenant des informations familières.
- **Interaction écrite guidée :** Je peux sélectionner ou compléter une formule adaptée pour demander un lieu, proposer une action ou répondre à un personnage.
- **Lexique :** Je peux identifier quelques lieux (parc, mairie, rivière), objets (poubelle, arbre, déchets) et actions écologiques (recycler, nettoyer, planter).
- **Structures :** Je peux employer « il faut », « nous devons », « on peut », « où est… ? » et des consignes spatiales simples.
- **Médiation élémentaire :** Je peux transmettre à un personnage une information simple comprise auprès d'un autre personnage, à l'aide d'un support.

Ces critères sont **des objectifs opérationnels créés pour le jeu**, inspirés de l'approche actionnelle du CECRL ; ils ne constituent pas une certification officielle. La **compréhension orale et la production orale ne seront pas automatiquement évaluées** dans V1.

### 2.3 Critères vérifiables du prototype

- Une partie complète est possible, depuis l'accueil jusqu'au bilan, **sans inscription ni donnée personnelle**.
- Le joueur peut explorer **un quartier 3D continu** comprenant quatre zones, trois personnages et trois séquences de mission.
- Au moins **deux parcours de décision distincts** produisent des changements visibles différents ; aucun ne nécessite une réponse « piège » arbitraire.
- Le système affiche **une rétroaction compréhensible** pour chaque décision linguistique et indique sur quel élément de la mission elle porte.
- Le joueur peut **relancer la mission**, essayer un autre parcours et comparer les conséquences.
- Les dialogues, objectifs et changements de scène sont décrits dans des fichiers de données séparés du rendu 3D.
- Une voie d'accès **sans déplacement libre en 3D** permet de suivre les dialogues et accomplir les tâches essentielles au clavier.

## 3. Publics et conditions d'utilisation

| Public | Usage V1 | Conditions |
|---|---|---|
| Apprenant Grade 5 A1 | Parcours guidé, 1 mission | Compréhension de phrases courtes ; consignes illustrées |
| Enseignant FLE | Préparer, observer, commenter une session | Bilan local sans profil nominatif |
| Visiteur du portfolio | Essayer un parcours de démonstration | Démonstration fictive, aucun compte |
| Développeur/évaluateur | Lire le code, reproduire les tests | Documentation technique et résultats séparés |

La durée de jeu visée est une **session de 10 à 15 minutes** ; il s'agit d'un objectif ergonomique à vérifier avec des utilisateurs, non d'une mesure observée. Le modèle initial est **mono-joueur, sans chat public**, et ne demande aucun microphone.

## 4. Identité et expérience du jeu

**Titre d'univers :** Éco-Cité francophone. **Ambiance :** aventure lumineuse et accessible, style 3D *low-poly* soigné, lisible sur ordinateur et écran tactile. **Caméra V1 :** troisième personne avec perspective légèrement surélevée ou contrôle simple, plutôt qu'un jeu d'action à caméra rapide. **Interface :** français au premier plan, aides contextuelles en espagnol ou anglais possibles en version ultérieure.

**Prémisse narrative.** Après de fortes pluies, le quartier central présente des déchets près d'une rivière et plusieurs espaces verts dégradés. La mairie a besoin d'idées et d'aide pour agir. L'apprenant est envoyé comme jeune ambassadeur ou ambassadrice de l'Éco-Cité ; il rencontre les habitants, recueille des informations puis contribue à une amélioration visible du quartier.

### 4.1 Carte initiale — quatre zones

| Zone 3D | Personnage/objet | Rôle pédagogique | Transformation visible |
|---|---|---|---|
| Place de la mairie | Panneau de mission, maire | Comprendre le problème, choisir l'objectif | Tableau de mission mis à jour |
| Quartier des habitants | Amina, habitante | Poser une question et recevoir un indice | Bacs de tri et signalétique |
| Parc des Trois Arbres | Nadia, bénévole | Proposer une action et demander du matériel | Jeunes arbres et fleurs apparaissent |
| Rive de la Rivière Claire | Éric, agent écologique | Localiser, comprendre une consigne | Déchets disparaissent, eau visuellement améliorée |

**Lisibilité de l'environnement :** chaque zone possède une couleur et un pictogramme ; les points d'interaction affichent un libellé textuel, un halo discret et une distance d'activation généreuse. Le joueur ne peut ni tomber ni perdre de santé. Aucun chronomètre punitif.

### 4.2 Personnages

- **Amina — habitante :** explique un souci concret, reformule une phrase inconnue, propose deux façons d'agir.
- **Nadia — bénévole :** organise les outils, accompagne la plantation, encourage à formuler « nous pouvons… ».
- **Éric — agent écologique :** donne des indications de lieu, demande « Où devons-nous mettre… ? », informe sur la rivière.
- **Le maire (panneau ou voix textuelle) :** présente la mission ; pour limiter le budget V1, il peut apparaître via un panneau interactif et non un quatrième personnage animé.

Chaque personnage a un **rôle communicatif**, une courte fiche pédagogique et trois à cinq répliques contextualisées. Les dialogues n'improvisent pas librement en V1 : les réponses possibles sont maîtrisées et revues par un enseignant.

## 5. Scénario jouable — Mission 01

### Séquence A — Découvrir le problème

L'apprenant arrive sur la place et lit : « Bonjour ! Notre rivière est sale. Le parc a besoin d'aide. Parle aux habitants et trouve une solution. » L'objectif affiché est : **« Je peux demander où se trouve un lieu »**.

Il rejoint Amina. Elle dit : « La rivière est derrière le parc. Il y a des déchets. » Le joueur doit sélectionner une demande appropriée : **« Où est la rivière ? »** ou **« Comment pouvons-nous aider ? »**. Les choix sont acceptables mais ne donnent pas la même information. Une réponse sans rapport appelle une reformulation et un nouvel essai, sans sanction humiliante.

### Séquence B — Choisir une stratégie

Le joueur consulte Nadia et Éric. Deux chemins principaux sont proposés :

**Chemin 1 — Trier et nettoyer.** Proposition : « Nous devons recycler les déchets. » Le joueur localise les bacs, choisit une consigne adaptée et aide un personnage à trier. **Conséquence :** des conteneurs apparaissent et la rive devient plus propre.

**Chemin 2 — Protéger et planter.** Proposition : « Nous pouvons planter des arbres. » Le joueur demande à Nadia où trouver les outils puis place deux jeunes arbres dans des emplacements signalés. **Conséquence :** le parc reverdit et un panneau présente les actions accomplies.

Le second chemin ne doit pas être présenté comme « faux ». Il traite une dimension différente de la situation, ce que les dialogues et le bilan rendent explicite. Un futur parcours pourra permettre d'effectuer les deux actions.

### Séquence C — Partager la solution

De retour sur la place, le joueur choisit deux phrases pour expliquer son action à un personnage : par exemple « Nous avons nettoyé la rivière » ou, dans une version A1 plus simple, **« La rivière est propre maintenant »** ; « Nous avons planté des arbres » peut être proposé comme modèle, sans en exiger la maîtrise productive en A1. Une dernière question contextualisée vérifie la compréhension de la conséquence observée.

L'écran final montre : le quartier avant/après, les décisions effectuées, les formulations utilisées, deux forces observables et une piste de progrès formulée positivement. L'apprenant peut recommencer sans perdre son droit de choisir autrement.

### 5.1 Échantillon de logique de dialogue

| Situation | Réplique / proposition | Réaction du monde | Indicateur |
|---|---|---|---|
| Demander | « Où est la rivière ? » | Marqueur de carte activé | Demander son chemin |
| Proposer | « Nous devons recycler. » | Chemin du tri débloqué | Proposer une action |
| Choisir | « On peut planter des arbres. » | Jardin et outils activés | Exprimer une possibilité |
| Réviser | Choix non adapté à la question | Indice et seconde tentative | Réutiliser une aide |

## 6. Mécaniques et règles de jeu

### 6.1 Contrôles et navigation

- **Ordinateur :** déplacements avec flèches ou WASD, bouton « Interagir », clic et commandes au clavier pour choisir une réplique.
- **Mobile/tablette :** joystick virtuel facultatif et gros boutons tactiles ; mode « Aller vers… » par liste de lieux si le déplacement tactile pose problème.
- **Caméra :** rotation limitée, collision légère avec les objets, option de désactiver les animations de caméra et les effets de mouvement.
- **Aides :** mini-carte simplifiée, journal des missions, répétition des répliques textuelles, bouton « Indice ».

### 6.2 Moteur d'états

Le moteur maintient des variables claires : `mission_step`, `path_choice`, `talked_to`, `collected_clues`, `world_state`, `supported_phrases` et `teacher_feedback`. Les états possibles comprennent `START`, `DISCOVER`, `DECIDE`, `ACT`, `REPORT`, `COMPLETE`. Les transitions ne doivent pas dépendre d'un clic 3D seul : l'interface accessible déclenche les mêmes actions.

**Principe déterministe :** l'événement pédagogique (« proposition valide pour le tri ») déclenche d'abord le changement d'état, puis la scène 3D affiche ce nouvel état. Cela permet de tester le fonctionnement des missions sans moteur graphique.

### 6.3 Évaluation formative, sans note artificielle

Le bilan suit trois dimensions distinctes : **compréhension des consignes**, **pertinence de la réponse en contexte** et **réemploi d'expressions clés**. Chaque dimension peut être notée qualitativement `observé`, `avec aide` ou `non observé`. Le jeu affiche les traces correspondantes, pas une note CECRL automatique. Le nombre d'essais est contextualisé et n'est pas interprété isolément comme un échec.

## 7. Périmètre de la première version

| INCLUS dans V1 | EXCLU ou reporté |
|---|---|
| Quartier 3D low-poly avec quatre zones | Monde ouvert de grande taille, multijoueur |
| Avatar simple, déplacement et interactions | Personnalisation avancée et inventaire complexe |
| Trois PNJ et scénarios écrits A1 | Chat génératif libre non modéré |
| Une mission complète, deux chemins recevables | 20 missions, scénarios procéduraux illimités |
| Changements persistants pendant la session | Sauvegarde cloud et profils nominatifs d'élèves |
| Mini-bilan « Je peux… » et aide enseignant | Certification CECRL, évaluation automatique orale |
| Version navigateur, interface clavier/tactile | VR/casque immersif et réalité augmentée |
| Tests de la logique narrative et capture de démo | Modèle ML entraîné, reconnaissance vocale |

**Livrable minimal à montrer :** l'accueil, une scène 3D réellement navigable, un premier dialogue, le choix de deux stratégies, un changement visuel pour chacune, puis un bilan consultable. Un simple rendu 3D sans interaction ne satisfait pas le cahier des charges.

## 8. Architecture technique recommandée

**Front-end V1 :** TypeScript + React + Vite, **Three.js** et **React Three Fiber** version stable compatible avec React, avec Drei pour certains composants prêts à l'emploi. React Three Fiber permet de décrire la scène 3D en composants réactifs, distincts des données de mission. **Éviter la version alpha de React Three Fiber** pour le premier prototype public.

**Moteur pédagogique V1 :** modules TypeScript purs et testables, sans serveur obligatoire. Les scénarios, répliques, objectifs et changements d'environnement sont contenus dans des fichiers JSON versionnés.

**Stockage V1 :** état de session en mémoire ; export local facultatif d'un bilan anonyme. Si une sauvegarde sur navigateur est ajoutée, expliquer son fonctionnement et fournir un bouton d'effacement. Aucun compte apprenant.

**Python :** prévoir un module d'analyse hors ligne des traces fictives pour le portfolio Data Science lors d'une phase ultérieure ; ne pas ajouter FastAPI si un serveur n'est pas nécessaire.

**Hébergement :** site statique sur Render, distinct des services Streamlit existants. Pour un projet Vite classique, le répertoire publié sera `dist` après la commande `npm ci && npm run build`. Les paramètres exacts seront vérifiés lors de la création du dépôt.

**Organisation du code envisagée :**

```text
booto-fle-multiverse-3d/
  README.md
  package.json
  index.html
  src/
    app/                 accueil, interfaces, transitions
    world/               scène 3D, zones, PNJ, transformations
    missions/            états, règles, choix, événements
    pedagogy/            critères Je peux, aides, bilan
    data/                dialogues et scénarios JSON
    accessibility/       navigation alternative et préférences
  public/                ressources 3D légères et autorisées
  tests/                 scénarios et évaluations des transitions
  docs/                  cahier des charges, guide enseignant, licences
```

**Modèle de données d'un nœud de dialogue :** identifiant, identifiant PNJ, phrase, niveau indicatif, action attendue, options textuelles, lien vers le nœud suivant, rétroaction et événement de monde (`river.cleaned`, `trees.planted`, `bins.visible`). Chaque nœud doit disposer d'une sortie valable, d'un indice et d'un retour utilisateur accessible.

## 9. Accessibilité, sécurité et éthique

- **Accessibilité :** navigation au clavier, focus visible, commandes réassignables si possible, sous-titres pour tout audio futur, réglage « réduire les mouvements », contrastes suffisants, pictogrammes accompagnés de texte et **alternative 2D / liste** pour l'accomplissement des missions. Se référer aux WCAG 2.2 sans prétendre à une conformité démontrée avant audit.
- **Performance :** assets compressés, style low-poly, limitation des lumières/ombres, option qualité « faible », test sur téléphone modeste ; l'objectif est la fluidité, sans annoncer de FPS garantis avant mesure.
- **Mineurs :** pas de publicités, achats, chat entre inconnus, classement nominatif ni contenu généré librement dans V1.
- **Données :** pas de noms, photos, voix ou copies réelles d'élèves ; scénarios et traces synthétiques pour les tests. Les hébergeurs peuvent conserver des journaux techniques.
- **Culture et langage :** personnages respectueux et variés, contextualisation francophone sans réduire une région à un stéréotype ; contenus révisés par un enseignant.
- **Droits :** modèles 3D, polices, textures et sons créés pour le projet ou provenant de sources dont les licences sont vérifiées avant redistribution.

## 10. Plan de réalisation par jalons

| Jalon | Produit attendu | Condition de passage |
|---|---|---|
| J0 — Référentiel | Cahier des charges et dialogue JSON finalisés | Revue du vocabulaire, règles et droits d'usage |
| J1 — Vertical slice visuelle | Place, parc, rivière, avatar navigable | Caméra stable et contrôles clavier/tactile |
| J2 — Mission jouable | 3 PNJ, deux parcours, conséquences 3D | Chaque parcours mène à un bilan sans impasse |
| J3 — Pédagogie explicable | Aides, critères « Je peux… », bilan | Aucun faux score certifiant le niveau |
| J4 — Assurance qualité | Tests automatisés, revue humaine, accessibilité | Scénarios clés réussis sur PC et mobile |
| J5 — Publication | Dépôt GitHub puis Static Site Render | URL publique fonctionnelle et lien portfolio vérifié |

La publication GitHub, l'hébergement Render et une éventuelle expérimentation en classe constituent **des actes distincts** : aucun n'est réputé effectué par le présent cahier des charges.

## 11. Recette fonctionnelle et critères d'acceptation

| ID | Test de recette | Réussite attendue |
|---|---|---|
| R01 | Ouvrir le jeu sans compte | Accueil, consignes et choix « commencer » visibles |
| R02 | Se déplacer ou utiliser les liens de zones | Accès aux quatre zones et à tous les PNJ |
| R03 | Parler à Amina, demander la rivière | Réplique adaptée et marqueur de lieu affiché |
| R04 | Choisir le tri | Bacs visibles, rive améliorée, cohérence du bilan |
| R05 | Recommencer et choisir la plantation | Jeunes arbres visibles, bilan différent |
| R06 | Choisir une réponse inadaptée | Indice utile, deuxième tentative, aucune impasse |
| R07 | Valider les trois étapes de mission | Écran final avec traces et objectifs « Je peux… » |
| R08 | Jouer au clavier seulement | Tous dialogues, choix et fin de mission accessibles |
| R09 | Désactiver le mouvement | Animation de caméra réduite, mission toujours jouable |
| R10 | Tester une zone sur mobile | Texte lisible, boutons tactiles atteignables |
| R11 | Charger la version sans réseau d'API | Mission jouable sans clé ni service externe |
| R12 | Relancer et comparer deux chemins | Conséquences différenciées et traçables |

**Validation pédagogique pilote :** observer des sessions volontaires sur exemples fictifs ou avec autorisations institutionnelles appropriées ; mesurer compréhension des consignes, autonomie, clarté des rétroactions et charge cognitive. Les performances ou progrès d'apprentissage ne peuvent être revendiqués que sur la base d'une étude documentée.

## 12. Risques et réponses prévues

| Risque | Réduction du risque |
|---|---|
| Monde 3D trop lourd sur mobile | Scène compacte, modèles légers, qualité adaptable, mode alternatif |
| Apparence de jeu, apprentissage superficiel | Chaque interaction reliée à un acte de langage observable |
| Une seule bonne réponse arbitraire | Plusieurs chemins recevables et conséquences expliquées |
| Surpromesse « IA » | V1 annoncée comme simulation à règles, pas modèle génératif |
| Suggestions linguistiques erronées | Dialogues écrits et validés par enseignant, journal de contenu |
| Collecte de données de mineurs | Aucune donnée réelle requise ; aucune inscription |
| Dépendance aux services coûteux | V1 autonome déployable comme site statique |
| Contenus 3D non autorisés | Bibliothèque d'actifs et suivi des licences avant publication |

## 13. Évolutions après la V1

**V2 — Parcours adaptatifs explicables.** Ajouter un tableau de bord enseignant sur données fictives, des variantes de consigne et un moteur de remédiation fondé sur les indices observés.

**V3 — Voix facultative.** Introduire l'écoute, l'oral et une expérimentation de reconnaissance vocale, après analyse des risques pour les mineurs et contrôle des voix utilisées. Ne pas prétendre évaluer la prononciation avec la simple transcription vocale.

**V4 — Studio des mondes.** Donner à l'enseignant la possibilité d'assembler des zones, personnages, dialogues et critères de réussite sans coder.

**V5 — Recherche et validation.** Tester l'outil avec protocole éthique, tâches comparables et indicateurs analysables, avant d'évoquer un impact pédagogique démontré.

## 14. Décision et mandat de conception

**Décision proposée :** adopter ce cahier des charges comme référence de la première réalisation 3D de BOOTO AI & DATA INNOVATION LAB. **Premier livrable d'implémentation :** une scène réellement jouable comprenant une place, une rivière, un parc, trois personnages, une interaction textuelle et deux changements visibles de l'environnement.

**Critère stratégique :** une démonstration sobre, jouable et vérifiable a plus de valeur qu'une vidéo spectaculaire d'un jeu qui n'existe pas encore. Le projet ne sera présenté comme « déployé » qu'après publication effective et vérification de son URL.

## Références de cadrage

- Conseil de l'Europe — CECRL et Volume complémentaire : https://www.coe.int/en/web/common-european-framework-reference-languages
- Conseil de l'Europe — Descripteurs : https://www.coe.int/en/web/common-european-framework-reference-languages/cefr-descriptors
- React Three Fiber, documentation officielle : https://r3f.docs.pmnd.rs/getting-started/introduction
- Render, hébergement des sites statiques : https://render.com/docs/static-sites
- W3C, Web Content Accessibility Guidelines 2.2 : https://www.w3.org/TR/WCAG22/

*Document de conception original — BOOTO FLE MULTIVERSE 3D V1. © 2026 Junior BOOTO Waba. Statut : conception ; ni code 3D, ni démonstration jouable, ni déploiement revendiqués à cette étape.*