# Portfolio File Guardian

**Junior BOOTO Waba | Python et automatisation | Prototype vérifié**

## Organiser des ressources avec des décisions traçables

Ce projet répond à une difficulté concrète : identifier les doublons dans un ensemble de ressources et préparer une organisation sans perdre les originaux. Son intérêt repose sur des preuves inspectables : empreintes SHA-256, inventaire, plan de copie et journal de restauration.

Le programme distingue le nom du fichier de son contenu. Les règles de classement sont configurables et les chemins relatifs sont conservés, ce qui évite d'écraser deux documents de même nom. Une simulation précède toute copie. Le retrait des copies exige une option explicite et vérifie leur contenu.

## Preuves obtenues

| Indicateur | Résultat du scénario synthétique |
|---|---:|
| Fichiers analysés | 8 |
| Contenu total | 248 octets |
| Groupes de doublons exacts | 1 |
| Collision de nom avec contenus distincts | 1 |
| Copies vérifiées puis retirées | 8 |
| Originaux conservés | 8 sur 8 |
| Tests de comportement réussis | 20 |

44 octets de contenu sont redondants dans ce jeu fictif. Il ne s'agit pas d'une estimation de gains réels sur un disque.

## Compétences mises en pratique

Python modulaire, fichiers et chemins, calcul d'empreintes en flux, validation des entrées, CLI, exports JSON/CSV/HTML, traitement explicite des erreurs, tests unitaires et scénario d'intégration. L'outil fonctionne sans API et sans dépendance tierce d'exécution.

## Méthode et portée

Inventaire → empreintes → groupes et catégories → simulation → copie explicite → vérification → restauration contrôlée.

L'outil est un prototype local pour des dossiers stables. Il conserve les doublons ; il ne synchronise pas un cloud, n'interprète pas le contenu pédagogique et ne garantit pas une transaction globale en cas de panne. Les tests ont été exécutés sous Linux. Le workflow GitHub Actions fourni reste à exécuter sur GitHub.

## Transparence

Projet conçu pour le portfolio de Junior BOOTO Waba avec assistance de ChatGPT. Inspiration conceptuelle : exercices de gestion de fichiers dans *53 Must Do Python Projects For All*, Edcorner Learning. Code réécrit pour cette livraison ; livre non redistribué. Aucune expertise industrielle n'est revendiquée.

Liens de publication du projet :

- https://github.com/Junior-BOOTO/python.skills/tree/main/portfolio-file-guardian
- https://junior-booto-fle.juniorbooto.chatgpt.site/portfolio-file-guardian.html

Profil et site :

- https://github.com/Junior-BOOTO
- https://junior-booto-fle.juniorbooto.chatgpt.site

## English summary

Portfolio File Guardian is a verified local Python prototype for file inventory, exact SHA-256 duplicate detection and reversible copy-only organization. A synthetic eight-file scenario demonstrates one duplicate group, one same-name content conflict, verified copies and unchanged originals. Twenty behavior tests pass locally on Linux. The project uses the Python standard library and includes reproducible evidence, documentation and a proposed CI workflow. It is a learning portfolio project, not a production cloud service.

## Grille interne (0–2 par critère)

| Critère | Note | Justification et limite |
|---|---:|---|
| Utilité | 2 | Problème concret d'organisation ; catégories explicites. |
| Reproductibilité | 2 | Démo synthétique et commandes hors ligne. |
| Robustesse | 1 | Parcours sensibles testés ; pas de transaction globale ni validation multiplateforme. |
| Preuves | 2 | Rapports JSON/CSV/HTML et journal de tests réels. |
| Documentation | 2 | Installation, décisions, exemples et limites explicités. |

Total interne : 9/10. Cette grille n'est ni une certification ni une mesure d'expertise professionnelle.
