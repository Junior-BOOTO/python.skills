# FLE Resource Studio

**Junior BOOTO Waba · FLE × Python · MVP 1.0.0**

Préparer une ressource FLE A1 à partir d'un thème, d'une aide et d'une langue de soutien. Le studio assemble des contenus explicites et inspectables ; il ne prétend ni générer librement toutes les séances, ni certifier un niveau CECRL.


## Découvrir le projet en trois minutes

1. **Essayer** : [ouvrir le studio](https://junior-booto-fle.juniorbooto.chatgpt.site/fle-resource-studio.html), choisir un thème, une aide et une langue.
2. **Observer** : comparer les modèles et les critères « Je peux… » entre deux aides. Cinq thèmes, trois aides et trois langues donnent 45 combinaisons vérifiées.
3. **Examiner** : [validation](reports/validation.json), [tests](reports/tests.txt), [contrôle navigateur daté](docs/verification-navigateur-2026-10-18.md).

**Compétences illustrées** : Python, catalogue structuré, exports et différenciation. Ressources à relire ; aucun effet mesuré en classe revendiqué.

**Reproduire** : [démarrage rapide](DEMARRAGE.md), puis section « Reproduire avec Python » ci-dessous.


## Version téléchargeable

[Version 1.0.1 et fichiers de distribution](https://github.com/Junior-BOOTO/python.skills/releases/tag/fle-resource-studio-v1.0.1) · [Démarrage rapide](DEMARRAGE.md) · [Historique](CHANGELOG.md)

La publication est effectuée par GitHub Actions uniquement après réussite des tests. Le rapport de validation accompagne l’archive. Cette distribution n’ajoute ni validation en classe ni licence ouverte générale.

## Ouvrir le studio

Ouvrir `reports/studio.html` dans un navigateur moderne. Le choix du thème, de l'appui et de la langue utilise des variantes préconstruites par Python. Les fiches individuelles `kits/<theme>/kit.html` sont autonomes. Aucun compte, clé payante ou API externe n'est nécessaire pour les ressources principales.

| Thème | Grade proposé | Objectif commun |
|---|---:|---|
| Les meubles de la maison | 2 | Dire trois phrases avec « C'est un/une… ». |
| Les travaux ménagers | 3 | Dire trois actions pour aider avec « Je… ». |
| La routine quotidienne | 4 | Présenter trois actions de sa journée. |
| Les paysages naturels | 4 | Décrire trois éléments avec « Je vois… ». |
| Droits, devoirs et écoresponsabilité | 5 | Dire un droit et deux devoirs avec les structures proposées. |

50 entrées de glossaire, 3 parcours et 3 langues d'aide donnent **45 combinaisons vérifiées**. Les repères graphiques sont des symboles/emoji indicatifs, pas des images réalistes ni une preuve que l'élève comprend le mot. Les enseignants apportent des objets ou dessins explicites selon leurs élèves.

## Contenu des fiches

- Glossaire français / espagnol / anglais, construit explicitement et éditable.
- Trois phrases modèles et une observation grammaticale.
- Fiche apprenant : correspondances de sens, trois phrases à préparer, critères « Je peux… ».
- Fiche enseignant : ouverture 8 min, activité principale 29 min, clôture 8 min.
- Trois aides avec le même objectif : appui renforcé, modèle, autonomie.
- Ressources et regroupements explicités ; corrigé et seuils observables.
- Script de lecture et lecture vocale facultative par le navigateur.
- Provenance, statut de revue pédagogique et candidates vidéo distinguées des vidéos approuvées.

Les contenus sont des propositions originales préparées avec assistance IA, **à relire et adapter par l'enseignant**. Aucune validation en classe, efficacité pédagogique ou donnée d'élève n'est revendiquée. Les exemples de droits/devoirs ne constituent pas une description juridique complète de la Colombie.

## Reproduire avec Python

Python **3.10+**, bibliothèque standard uniquement. Depuis la racine du projet :

```bash
export PYTHONPATH=src
python -m fle_studio studio --output reports/studio-regenerated.html
python -m fle_studio build meubles --support guided --language es --output my-kits
python -m unittest discover -s tests -v
```

Sous PowerShell : remplacer la première ligne par `$env:PYTHONPATH = "src"`.

Chaque export produit `kit.json`, `kit.html`, `teacher.txt`, `answers.json`, `audio-script.txt`. Un dossier de kit existant n'est pas écrasé. Choisir un nouveau dossier de sortie pour une nouvelle version. L'option `--level A2` est refusée : aucune adaptation automatique A2 n'est implémentée.

`data/build_catalog.py` est le générateur du catalogue initial. Il écrit le fichier de départ et écraserait une édition manuelle de `data/catalog.json` : ne le relancer que pour reconstruire ce catalogue de départ, après sauvegarde de vos adaptations.

## API locale en lecture seule

```bash
python -m fle_studio serve --port 8766
```

- `http://127.0.0.1:8766/` : studio.
- `GET /api/catalog` : thèmes et provenance.
- `GET /api/kits/meubles?level=A1&support=guided&language=es` : fiche structurée.

Les options sont validées ; POST/PUT/DELETE sont refusés. Le serveur reste lié à `127.0.0.1`. C'est une API locale de développement, sans publication automatique ou service distant revendiqué. Routes, erreurs et absence de mutation testées réellement sur l'interface loopback.

## Lecture vocale : état exact

« Écouter les modèles » utilise `speechSynthesis` si une voix française est disponible dans le navigateur. L'outil affiche un état explicite en cas d'absence de voix ou d'erreur. La vitesse est réglée à 0,85 ; ce n'est pas une mesure pédagogique de débit. Certaines voix utilisent un service distant selon le navigateur. Aucune parole d'élève n'est enregistrée.

Aucun moteur français de synthèse vocale exécutable n'était disponible pour créer une bande-son dans cet environnement. **Aucun MP3/WAV n'est donc livré.** Les scripts TXT sont fournis et la lecture de l'enseignant constitue un parcours complet. La lecture vocale réelle reste à vérifier. Le rendu navigateur a été contrôlé dans Chromium le 18 octobre 2026 ; voir le compte rendu daté en fin de page.

## Traductions : état exact

Les aides FR/ES/EN sont un glossaire explicite de 50 entrées, pas un appel à Google Translate ou une traduction libre de textes. Elles sont proposées dans le contexte du thème. Toute adaptation de sens, variante régionale ou expression nouvelle doit être revue par un enseignant. Les aides espagnoles et anglaises peuvent être retirées pour une version française seulement.

## Vidéos : découverte et revue séparées

Une candidate sur la routine a été repérée dans les résultats web le 12 octobre 2026. Sa page et ses métadonnées ont été identifiées, mais la vidéo n'a pas été visionnée ; âge, difficulté et segment utilisable restent inconnus. Elle n'est **pas intégrée aux vidéos approuvées**.

Pour approuver une ressource, renseigner dans le catalogue : `review_status: approved`, le nom du relecteur, une date et les quatre contrôles vrais : adéquation à l'âge, langue accessible, lien avec l'objectif et segment utilisable. Cette déclaration est manuelle et reste sous la responsabilité de l'enseignant. Les métadonnées ne suffisent pas.

Connecteur facultatif de métadonnées, nécessitant une clé fournie par votre environnement sécurisé :

```bash
python -m fle_studio youtube yW5PvraL-wA --output reports/youtube-metadata.json
```

La variable `YOUTUBE_API_KEY` est lue par le connecteur. Ne jamais publier une clé. L'appel `videos.list` récupère les métadonnées ; il n'approuve pas la vidéo et ne télécharge ni vidéo, ni transcript, ni sous-titre. Les réponses ont une limite de taille et un timeout. Les tests du connecteur utilisent des réponses simulées et vérifient notamment l'absence de fuite de clé dans les erreurs. **Aucun appel YouTube authentifié n'a été exécuté dans cette livraison.**

## Preuves et limites

20 tests de comportement réussis localement sous Linux. Les 45 combinaisons ont été construites et vérifiées, cinq kits par défaut exportés et la syntaxe JavaScript contrôlée. Résultats et versions : `reports/validation.json` et `reports/tests.txt`.

La feuille d'impression masque la fiche enseignant, les vidéos et le corrigé. Le profil A4 a été contrôlé dans Chromium le 18 octobre 2026 sur les cinq thèmes : deux pages par fiche. L’impression physique et les autres navigateurs restent à vérifier.

Pas de profil d'élève, de note automatique, de chatbot conversationnel, de reconnaissance vocale, de connexion Drive ni de stockage cloud. L'objectif est fixé par le thème et aligné avec la tâche et les critères ; un objectif différent exige une adaptation de la séance entière.

## Attribution et portfolio

Conception pour Junior BOOTO Waba avec assistance ChatGPT. Inspiration conceptuelle : *Python Projects With API*, Minal Pandey (catalogue/API, métadonnées YouTube, traduction, synthèse vocale). Aucun code ou PDF du livre n'est redistribué. La vidéo candidate reste un lien vers son créateur, sans droits de redistribution supposés.

Références consultées :
- https://developers.google.com/youtube/v3/docs/videos/list
- https://developers.google.com/youtube/v3/docs/videos
- https://www.youtube.com/watch?v=yW5PvraL-wA (candidate non validée pédagogiquement)

Le code et les propositions de ressources ne reçoivent pas automatiquement une licence ouverte. La licence doit être choisie par l'auteur avant une redistribution sous licence ouverte. Projet présenté dans les axes FLE et Python/data du portfolio : [studio](https://junior-booto-fle.juniorbooto.chatgpt.site/fle-resource-studio.html) · [code](https://github.com/Junior-BOOTO/python.skills/tree/main/fle-resource-studio). La lecture vocale reste dépendante du navigateur et les ressources nécessitent une revue enseignante.

## Contrôle du rendu — 18 octobre 2026
La version 1.0.0 a été examinée dans Chromium sur ordinateur et mobile : 45 variantes et export JSON vérifiés. L’inspection des PDF a révélé une grille répartie sur trois pages. La version 1.0.1 corrige le profil A4 et les sauts : une page de lexique/modèles puis une page d’activités et de critères. La lecture vocale réelle, les autres navigateurs et l’impression physique restent à vérifier. Les preuves du contrôle sont conservées dans les artefacts GitHub Actions du processus de publication.

[Compte rendu de la vérification navigateur et impression](docs/verification-navigateur-2026-10-18.md).
