# Portfolio Evidence Hub — Junior BOOTO Waba

## Chaque constat relié à une preuve

Ce prototype Python relie la documentation, les fichiers et les résultats CI de projets de portfolio à leurs sources exactes. Son tableau de bord rend visibles les preuves manquantes et évite de confondre présence de tests et exécution réussie.

Trois projets réels sont audités : Portfolio File Guardian, AfriFlow Explain et API météo Bogotá. Le registre, les règles et les instantanés sont fournis pour reproduire l'analyse hors ligne.

L'apport du projet est une traçabilité examinable : SHA du commit, références de fichiers, attribution explicite des workflows, empreintes et horodatages. Une difficulté d'accès au site est présentée comme une incertitude, pas comme une page cassée.

## Compétences mises en pratique

Python modulaire, API REST, provenance des données, empreintes de contenu, contrôle des erreurs, règles explicites, API locale en lecture seule, tableau de bord filtrable et tests de comportement.

Le projet réutilise les fichiers et preuves de File Guardian, puis étend le périmètre à GitHub et aux liens du site. Il ne remplace pas une revue de code et ne mesure pas l'expertise du propriétaire.

## English summary

Portfolio Evidence Hub is a read-only Python MVP for auditing a project portfolio using commit-pinned file evidence, explicitly attributed CI runs, local file comparisons and dated website observations. Three real public projects are included. It distinguishes missing artifacts from unavailable evidence, provides a standalone dashboard and a local read-only API, and does not execute audited code or publish automatically.

## Statut

Code et audit exécutés localement. Résultats détaillés dans reports/audit.json ; tests et environnement dans reports/validation.json. Collecteur GitHub autonome fourni, sans exécution complète de ce connecteur réseau dans cette livraison. Présentation : https://junior-booto-fle.juniorbooto.chatgpt.site/portfolio-evidence-hub.html. Code : https://github.com/Junior-BOOTO/python.skills/tree/main/portfolio-evidence-hub. Audit historique daté, non actualisé automatiquement.

## Grille interne de conception

| Critère | Note / 2 | Justification |
|---|---:|---|
| Utilité | 2 | Relie des preuves réellement dispersées entre projets et canaux. |
| Reproductibilité | 2 | Instantané daté et audit hors ligne. |
| Robustesse | 1 | Erreurs et attributions testées ; accès HTTP et validation visuelle restent limités. |
| Preuves | 2 | Commit, blobs, CI, empreintes et constats inspectables. |
| Documentation | 2 | États, commandes, portée et limites explicites. |

9/10 selon cette grille interne, sans valeur de certification ni d'évaluation d'expertise.
