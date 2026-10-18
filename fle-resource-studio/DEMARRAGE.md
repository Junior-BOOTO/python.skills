# Démarrer avec FLE Resource Studio — 1.0.1

## Sans Python : consulter les ressources
1. Télécharger l’archive ZIP depuis la [version publiée](https://github.com/Junior-BOOTO/python.skills/releases/tag/fle-resource-studio-v1.0.1), puis utiliser « Extraire tout ».
2. Ouvrir le dossier fle-resource-studio-1.0.1.
3. Ouvrir reports/studio.html dans un navigateur. Les ressources principales sont autonomes.
4. Choisir le thème, l’aide et la langue de soutien. La lecture vocale dépend des voix disponibles sur votre appareil.
5. Pour une fiche autonome, ouvrir kits/<theme>/kit.html : meubles, taches, routine, paysages ou ecocitoyen.

Les aperçus utilisent des symboles, pas des photographies réalistes. Relire les contenus avant la classe. Les vidéos candidates ne sont pas des vidéos approuvées.

## Avec Python : construire une fiche
Prérequis : Python 3.10 ou plus récent. Aucune bibliothèque tierce nécessaire à ces commandes.
Ouvrir le terminal **dans le dossier extrait**, celui qui contient data/, src/ et README.md.

Linux/macOS :
```bash
export PYTHONPATH=src
python -m fle_studio build meubles --support guided --language es --output mes-fiches
python -m unittest discover -s tests -v
```

Windows PowerShell :
```powershell
$env:PYTHONPATH = "src"
python -m fle_studio build meubles --support guided --language es --output mes-fiches
python -m unittest discover -s tests -v
```

Le résultat se trouve dans mes-fiches/meubles/. Une destination de fiche existante est refusée : choisir un nouveau dossier pour recommencer.

## Construire le studio ou ouvrir l’API locale
Après définition de PYTHONPATH comme ci-dessus :
```bash
python -m fle_studio studio --output mes-exports/studio.html
python -m fle_studio serve --port 8766
```
Ouvrir http://127.0.0.1:8766/ ; arrêter le serveur avec Ctrl+C. Ce serveur reste local et ne publie pas votre travail sur Internet.

## Impression et utilisation pédagogique
Ouvrir une fiche autonome puis l’aperçu d’impression du navigateur. Vérifier format A4, débordements, pages et séparation du corrigé avant de lancer le tirage. La feuille d’impression masque les sections enseignant et corrigé ; ce comportement nécessite un contrôle visuel sur votre appareil. Aucun PDF à mise en page fixe ni validation d’impression n’est revendiqué dans cette version.

Conserver les scripts d’écoute comme textes à lire ; aucun MP3 n’est livré. Ne pas importer de données d’élèves.

## En cas de difficulté
- Module introuvable : vérifier le dossier courant et PYTHONPATH.
- Catalogue introuvable : se placer dans le dossier contenant data/catalog.json.
- Destination existante : choisir un nouveau dossier d’export.
- Voix absente : lire soi-même le script fourni.
- Signaler le système, Python, la commande et l’erreur, sans donnée personnelle, dans une Issue du dépôt ; préciser « FLE Resource Studio ».

## Validation et droits
La construction du ZIP vérifie son intégrité, relance les 20 tests depuis une extraction temporaire et génère un studio ainsi qu’une fiche. Le rapport joint à la version précise l’environnement. Ces contrôles ne remplacent ni une validation pédagogique, ni une inspection visuelle dans le navigateur.

La disponibilité du ZIP ne change pas les droits des contenus. Aucune licence ouverte générale n’est attribuée par cette publication. Voir les attributions et limites du README.
