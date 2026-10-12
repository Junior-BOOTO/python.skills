# Portfolio Evidence Hub

**Junior BOOTO Waba · Python / automatisation · MVP 1.0.0**

Relier chaque constat d'un portfolio à une preuve datée : fichier au commit GitHub, résultat CI attribué au projet, observation de page et concordance avec les fichiers locaux. Les absences de preuve restent visibles. Aucun score d'expertise n'est calculé.

## Problème et résultat

Les sources, rapports et présentations d'un projet peuvent être dispersés entre un dossier local, GitHub et un site. Hub crée un registre de trois projets et audite huit critères par projet. Il distingue présence des tests, résultat local déclaré et exécution GitHub Actions observée.

Le jeu fourni contient des observations publiques réelles du dépôt `Junior-BOOTO/python.skills`, figées au commit indiqué dans `reports/audit.json`. Les exemples des tests unitaires sont, eux, synthétiques. Aucun document privé Drive ou identifiant d'élève n'est inclus.

Ouvrir **reports/dashboard.html** : filtres par projet et état, recherche, preuves dépliables et prochaines actions. La page est autonome et ne fait aucune requête externe ; les liens vers les preuves demandent un accès Internet. L'audit Python n'est pas exécuté dans le navigateur.

## Reproduction hors ligne

Python **3.10+**, bibliothèque standard uniquement à l'exécution.

Depuis ce dossier, Linux/macOS :

```bash
export PYTHONPATH=src
python -m evidence_hub audit --local-snapshot data/local-observations.json
python -m unittest discover -s tests -v
```

PowerShell : remplacer la première ligne par `$env:PYTHONPATH = "src"`.

L’option --local-snapshot rejoue la comparaison locale datée fournie, sans lire vos dossiers. Sans cette option, la concordance locale reste inconnue. Le premier audit lit les instantanés fournis et écrit `reports/audit.json`, `reports/dashboard.html`, `reports/next-actions.md`. Il ne modifie aucun projet, dépôt ou site.

Pour comparer un checkout local avec les fichiers GitHub du projet configuré :

```bash
python -m evidence_hub audit --local portfolio-file-guardian=/chemin/portfolio-file-guardian
```

La comparaison calcule le SHA-256 local et le SHA-1 du blob Git utilisé par ce dépôt. Elle porte sur les fichiers distants répertoriés, détecte leurs absences ou différences, mais ne recherche pas les fichiers locaux supplémentaires. Les symlinks sont refusés. La cohérence de contenu n'est pas une preuve de bon fonctionnement.

## Actualiser les observations

```bash
python -m evidence_hub collect --output data/live
python -m evidence_hub audit --snapshot data/live/github-snapshot.json --sites data/live/site-observations.json
```

Le collecteur interroge l'API REST GitHub et les trois pages HTTPS configurées. Il résout une fois le commit de la branche par défaut, puis fige les lectures à ce commit. Il vérifie la troncature de l'arbre et borne la pagination des workflows à dix pages de cent résultats. Les lectures réseau ont un timeout de quinze secondes et une limite de taille. Les erreurs partielles des documents/workflows sont enregistrées ; l'échec du début de collecte arrête la commande avec un code de sortie 2.

Un jeton GitHub est facultatif pour un dépôt public. Si nécessaire, fournir `GITHUB_TOKEN` par le mécanisme sécurisé de votre environnement, avec des droits de lecture seulement. Le jeton n'est jamais enregistré dans l'instantané ni envoyé au site. L'application n'envoie aucun message, ne publie pas et ne crée pas de webhook.

**Validation réelle de cette livraison :** les données GitHub ont été obtenues par la connexion GitHub disponible, puis le moteur a audité cet instantané. Le collecteur autonome réseau est fourni et testé sur cas contrôlés ; une collecte GitHub complète via ce script n'a pas été exécutée dans cet environnement. Les requêtes HTTP réelles du collecteur vers les pages du site ont été exécutées et leurs résultats sont conservés.

## API locale en lecture seule

```bash
python -m evidence_hub serve --port 8765
```

- `http://127.0.0.1:8765/` : tableau de bord.
- `GET /api/report` : audit complet.
- `GET /api/projects` : liste des projets.
- `GET /api/projects/portfolio-file-guardian` : constats d'un projet.

Le serveur s'attache uniquement à `127.0.0.1`, sans mutation distante. POST/PUT/DELETE retournent 405. API et routes réellement testées localement. Ne pas exposer ce serveur de développement sur Internet sans couche d'hébergement et contrôle d'accès adaptés.

## Signification des états

| État | Interprétation |
|---|---|
| Vérifié | Le contrôle précisément nommé a une preuve suffisante dans l'instantané. |
| Manquant | Une absence est établie dans un inventaire complet, ou HTTP 404/410 est observé. |
| À vérifier | Donnée absente, accès refusé, inventaire incomplet ou résultat non attribuable. |
| Attention | Une différence, un résultat CI échoué ou une réponse inattendue demande une revue. |

Huit critères : documentation, code Python, environnement déclaré, tests présents, résultat local archivé, CI attribuée, page du site, concordance locale/GitHub.

« Tests présents » recherche des fichiers Python `test*` sous un dossier `tests/` ; des assertions présentes ailleurs ne sont pas inventoriées comme une suite de tests structurée. « Résultat local archivé » vérifie l'intégrité d'un fichier de déclaration, pas son exactitude scientifique ni une nouvelle exécution. Les résultats CI d'autres projets ou d'un autre commit ne sont pas transférés. Le registre contient explicitement l'attribution du workflow ; cette configuration doit être revue si le workflow change.

HTTP 200 et un marqueur textuel confirment seulement la réponse reçue. Ni l'accessibilité publique, ni les interactions, ni le rendu visuel ne sont certifiés. Une page bloquée par l'environnement ne devient pas automatiquement une page inexistante.

## Architecture

`projects.json` → collecte GitHub/pages → instantané daté → moteur de règles → JSON + tableau de bord + actions → API locale facultative.

- `src/evidence_hub/audit.py` : règles, intégrité des blobs et comparaison locale.
- `collect.py` : accès REST GitHub et observations HTTP, en lecture seule.
- `render.py` : HTML échappé et filtres côté navigateur.
- `server.py` : API locale en lecture seule.
- `tests/` : vérification des cas de vérité, absence, échec, erreur réseau, intégrité et API.
- `data/` : preuves datées utilisées pour cette livraison.
- `reports/` : résultats calculés, validation et actions.

## Limites et suite

MVP pour trois projets explicitement configurés. Pas d'exécution du code audité, d'analyse de sa qualité, d'accès Drive, de surveillance continue, de traitement de webhooks ni de publication automatique. L'instantané n'est pas signé et les observations site/GitHub ne sont pas simultanées. Un nouveau commit nécessite une nouvelle collecte ; le rapport livré reste historique.

Les filtres JavaScript sont fournis et leur syntaxe est vérifiée. La vérification visuelle complète en navigateur reste non réalisée, faute de navigateur disponible. Les tests ont été exécutés sous Linux ; Windows/macOS restent à vérifier.

Prochaine extension : notifications facultatives et événements GitHub signés, dédupliqués et journalisés. Ne les ajouter qu'après validation du MVP. Drive pourra ensuite fournir un inventaire autorisé distinct, sans rendre publics les fichiers privés.

## Attribution

Conçu pour Junior BOOTO Waba avec assistance de ChatGPT. Prolonge les usages de Portfolio File Guardian et associe les thèmes catalogue/API et GitHub du document *Python Projects With API*, Minal Pandey. Aucun code du livre n'est copié et aucun PDF n'est redistribué. Les README inclus dans l'instantané sont ceux des projets publics du propriétaire.

Documentation officielle utilisée pour préparer le protocole :
- https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api
- https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries (extension future, non implémentée)

Licence du code original à choisir par l'auteur avant redistribution sous licence ouverte. Cette livraison ne revendique pas une certification ou une expertise industrielle. Liens de publication : [GitHub](https://github.com/Junior-BOOTO/python.skills/tree/main/portfolio-evidence-hub) · [Tableau de bord](https://junior-booto-fle.juniorbooto.chatgpt.site/portfolio-evidence-hub.html). L’audit inclus reste un instantané du commit indiqué ; il ne s’actualise pas automatiquement.

## Résultats de cette livraison

24 contrôles sur trois projets : 13 vérifiés, 1 fichier de tests structuré manquant selon la règle, 9 à vérifier et 1 différence locale/GitHub. Cette différence du CSV est exclusivement liée aux fins de ligne CRLF/LF ; les valeurs sont identiques. Les trois requêtes site ont reçu une redirection HTTP 307 non suivie : leur contenu reste non vérifié. 20 tests du Hub réussis localement.
