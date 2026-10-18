# Portfolio File Guardian — démarrage 1.0.0

## Télécharger et découvrir
Télécharger [la version 1.0.0](https://github.com/Junior-BOOTO/python.skills/releases/tag/portfolio-file-guardian-v1.0.0), extraire le ZIP et ouvrir reports/report.html pour consulter le rapport fictif. Le programme de traitement exige Python 3.10 ou plus récent ; aucune bibliothèque tierce n’est nécessaire.

Ouvrir le terminal dans le dossier extrait contenant src/, tests/ et README.md.

Linux/macOS :
```bash
export PYTHONPATH=src
```

Windows PowerShell :
```powershell
$env:PYTHONPATH = "src"
```

## Essayer sur des données fictives
```bash
python scripts/demo.py
python -m unittest discover -s tests -v
```

La démonstration crée huit fichiers fictifs dans un espace temporaire, vérifie copie et restauration, puis nettoie cet espace. Ses rapports sont écrits dans reports/. Les documents personnels ne sont pas utilisés.

## Inventorier vos fichiers
Remplacer les chemins d’exemple par des chemins absolus existants :
```bash
python -m file_guardian scan /chemin/mes-fichiers
python -m file_guardian scan /chemin/mes-fichiers --output /chemin/rapport-separe
```

Sous Windows, utiliser par exemple un chemin entre guillemets de la forme "C:\\MesDocuments\\Exemple". Le dossier des rapports doit être distinct de la source et extérieur à celle-ci. Sans --output, scan affiche l’inventaire sans écrire de rapport.

## Simuler puis copier
```bash
python -m file_guardian organize /chemin/mes-fichiers /chemin/nouveau-dossier
python -m file_guardian organize /chemin/mes-fichiers /chemin/nouveau-dossier --execute
```

La première commande simule. La seconde copie les fichiers après contrôle. La destination doit être nouvelle et extérieure à la source. Les originaux sont conservés ; les doublons sont repérés mais ne sont pas supprimés automatiquement.

## Examiner la restauration
```bash
python -m file_guardian restore /chemin/nouveau-dossier
python -m file_guardian restore /chemin/nouveau-dossier --execute
```

La restauration simule par défaut. Avec --execute, elle retire les copies journalisées dont le contenu est inchangé ; elle conserve les originaux et les fichiers non journalisés. Une copie modifiée bloque le contrôle initial. Lire le README avant toute opération sur des fichiers réels.

## Validation et limites
Les tests et la démonstration sont réexécutés depuis le ZIP extrait avant publication. Ils couvrent le comportement sous Linux ; les commandes PowerShell sont proposées, mais le comportement Windows/macOS n’a pas été exécuté dans cette publication.

Prototype pour un dossier stable et une opération à la fois. Pas de stockage cloud, synchronisation, déplacement ou transaction globale. La copie ne conserve pas les ACL, attributs étendus et dates originales. Le journal doit être conservé et protégé.

Le ZIP n’attribue aucune licence ouverte générale. Consulter NOTICE.md et le README pour les droits et attributions.
