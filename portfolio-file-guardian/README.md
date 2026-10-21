# Portfolio File Guardian

**Junior BOOTO Waba · Python / automatisation · Prototype 1.0.0**

Inventorier des ressources, identifier leurs doublons exacts et préparer leur organisation, tout en conservant les originaux. Ce projet de portfolio associe traitement de fichiers, empreintes SHA-256, validation des chemins, interface en ligne de commande, journal et tests de comportement.

[Examiner le rapport HTML généré](reports/report.html)


## Découvrir le projet en trois minutes

1. **Voir** : [rapport de démonstration](https://junior-booto-fle.juniorbooto.chatgpt.site/guardian-reports/report.html).
2. **Comparer** : un contenu identique sous deux noms et deux contenus différents portant le même nom. Huit fichiers synthétiques ; un groupe de doublons exacts.
3. **Examiner** : [copie et restauration](reports/demo-evidence.json), [inventaire](reports/inventory.csv), [validation](reports/validation.json), [tests](reports/tests.txt).

**Compétences illustrées** : SHA-256, contrôle des chemins, simulation et journalisation. Originaux conservés ; aucune suppression automatique des doublons.

**Reproduire** : [démarrage rapide](DEMARRAGE.md), puis lancer la démonstration décrite ci-dessous sur les fichiers fictifs temporaires.


## Version téléchargeable

[Version 1.0.0 et archive ZIP](https://github.com/Junior-BOOTO/python.skills/releases/tag/portfolio-file-guardian-v1.0.0) · [Démarrage rapide](DEMARRAGE.md) · [Historique](CHANGELOG.md)

L’archive est construite après réussite des tests ; les empreintes et le rapport de vérification sont joints à la version. Les limites et conditions de réutilisation restent celles décrites ici.

## Problème et apport

Un portfolio rassemble souvent des ressources FLE, du code et des données dans plusieurs dossiers. Deux fichiers portant des noms différents peuvent être identiques ; deux fichiers de même nom peuvent être différents. Guardian distingue ces situations et propose des catégories selon les extensions.

L'organisation copie chaque fichier dans un nouveau dossier en conservant son chemin relatif. Aucun doublon n'est supprimé. Les catégories personnalisées décrivent des règles explicites : elles ne constituent pas une classification sémantique ou un modèle d'IA.

## Résultats effectivement obtenus

Démonstration sur **8 fichiers synthétiques**, total **248 octets** :

- 1 groupe de doublons exacts, soit 44 octets de contenu redondant théorique.
- 1 collision de nom : deux `lesson.txt` aux contenus différents.
- 8 copies vérifiées par SHA-256, puis retirées par le journal de restauration.
- Tous les originaux inchangés ; deux inventaires successifs identiques.
- Suite de tests exécutée : voir [validation](reports/validation.json) et [journal des tests](reports/tests.txt).

La redondance théorique n'est pas une mesure d'espace disque récupérable. Les liens physiques, la compression et les métadonnées de fichiers ne sont pas dédupliqués.

## Exécuter sans installation ni accès réseau

Python **3.10 ou supérieur**, aucune dépendance tierce à l'exécution.

Depuis le dossier du projet, sous Linux/macOS :

```bash
export PYTHONPATH=src
python -m file_guardian scan /chemin/mes-fichiers
python -m file_guardian scan /chemin/mes-fichiers --output /chemin/rapport-separe
python -m file_guardian organize /chemin/mes-fichiers /chemin/nouveau-dossier
```

Sous PowerShell, remplacer la première ligne par :

```powershell
$env:PYTHONPATH = "src"
```

`scan` et `organize` sans `--execute` sont des simulations : lecture des fichiers, aucun changement aux sources, aucune destination créée. L'option explicite `scan --output` écrit seulement les rapports dans un dossier séparé : `plan.json`, `inventory.csv`, `report.html`.

Pour copier, après inspection du rapport :

```bash
python -m file_guardian organize /chemin/mes-fichiers /chemin/nouveau-dossier --execute
python -m file_guardian restore /chemin/nouveau-dossier
python -m file_guardian restore /chemin/nouveau-dossier --execute
```

La destination doit être nouvelle, extérieure à la source et sans liens symboliques. Une deuxième copie vers la même destination est refusée ; l'inventaire est répétable mais la copie n'est pas une synchronisation incrémentale.

`restore` simule par défaut. Avec `--execute`, il retire uniquement les copies journalisées dont l'empreinte correspond. Il conserve les originaux, les fichiers non journalisés, le journal et les dossiers vides. Une copie modifiée bloque la restauration avant la première suppression lors du contrôle initial.

## Démonstration et tests

```bash
python scripts/demo.py
python -m unittest discover -s tests -v
```

La démonstration génère des fichiers fictifs dans un dossier temporaire, vérifie le cycle complet puis les efface ; ses rapports persistent dans `reports/`. Aucun document personnel n'est nécessaire.

Installation facultative dans un environnement virtuel : `python -m pip install -e .`. Elle requiert setuptools pour le packaging ; elle permet ensuite `file-guardian scan ...`.

## Configuration

```bash
python -m file_guardian scan /chemin/mes-fichiers --categories categories.example.json
```

Chaque clé est un nom de catégorie et chaque valeur une liste d'extensions minuscules. Les extensions répétées et les noms de catégorie pouvant sortir du dossier sont refusés. Les extensions non configurées vont dans `other`. `.PDF` et `.pdf` utilisent la même règle.

## Architecture et fichiers

- `src/file_guardian/core.py` : inventaire, hash en flux, catégories, exports, copie et restauration.
- `src/file_guardian/__main__.py` : commandes, options, erreurs et codes de sortie.
- `tests/test_guardian.py` : tests isolés avec fichiers temporaires.
- `scripts/demo.py` : scénario reproductible et assertions.
- `reports/` : inventaire, preuves, journal d'exemple et résultats de tests.
- `docs/portfolio.md` et `docs/portfolio.html` : présentation FR avec résumé EN.
- `manifest.json` : état, livrables et prochaine étape.

## Limites et décisions

Prototype pour des dossiers locaux stables, utilisé par un seul processus. Pas de service web, stockage cloud, surveillance continue, antivirus, déplacement ou suppression automatique des doublons. SHA-256 est une empreinte de contenu, pas une garantie de provenance ni de sécurité d'un fichier.

Les erreurs de lecture sont visibles ; une copie est refusée si l'inventaire contient des erreurs. Les dossiers symlinks sont exclus ; les fichiers symlinks sont refusés. Les chemins et textes HTML/CSV sont contrôlés. Ces mesures ne remplacent pas une protection système face à un processus hostile modifiant les répertoires simultanément. Utiliser un dossier stable ; ne pas exécuter plusieurs opérations en parallèle.

La copie consomme de l'espace supplémentaire et préserve les octets, pas les ACL, les attributs étendus ni les dates originales. En cas d'interruption, le journal marque les intentions et les copies vérifiées ; un fichier partiel dont le hash ne correspond pas est conservé et nécessite une revue manuelle. Pas de transaction globale ni de récupération automatique après panne. Protéger le journal : il constitue la liste de restauration et n'est pas signé cryptographiquement.

Tests exécutés sous Linux/Python indiqué dans `reports/validation.json`. Le comportement Windows et macOS n'a pas été exécuté dans cette livraison. Le test de fichier illisible injecte une `PermissionError`, car l'environnement de validation possède des privilèges élevés. Les symlinks et les autres parcours sont testés sur le système réel.

Les rapports contiennent les noms de fichiers : ne publier que des rapports synthétiques ou expurgés. Présentation en ligne : https://junior-booto-fle.juniorbooto.chatgpt.site/portfolio-file-guardian.html. Dépôt : https://github.com/Junior-BOOTO/python.skills/tree/main/portfolio-file-guardian.

## Attribution et transparence

Inspiration : Edcorner Learning, *53 Must Do Python Projects For All*, familles d'exercices 9, 10, 29, 48 et 49. Le PDF et son code ne sont pas redistribués. L'implémentation livrée a été créée dans cette session avec l'assistance de ChatGPT pour le portfolio de Junior BOOTO Waba. Elle présente un projet d'apprentissage vérifié, pas une expérience industrielle revendiquée.

Profil : https://github.com/Junior-BOOTO · Site : https://junior-booto-fle.juniorbooto.chatgpt.site

Aucune licence ouverte n'est attribuée automatiquement. Avant publication publique, l'auteur doit choisir la licence du code original ; les droits des sources tierces restent distincts. Voir `NOTICE.md`.
