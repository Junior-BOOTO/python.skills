# Portfolio File Guardian 1.0.0

Première archive versionnée du prototype d’organisation de fichiers de Junior BOOTO Waba.

## Contenu
- portfolio-file-guardian-1.0.0.zip : code, tests, démonstration fictive, rapports et guide DEMARRAGE.md.
- SHA256SUMS.txt : empreinte SHA-256 du ZIP.
- release-validation.json : contrôles réalisés sur une extraction temporaire de l’archive.

## Pour commencer
Extraire le ZIP puis lire DEMARRAGE.md. Ouvrir reports/report.html pour découvrir un inventaire fictif. Avec Python 3.10+, commencer par scripts/demo.py avant d’examiner vos propres fichiers.

La publication exige des tests réussis sous Linux/Python 3.10 et 3.12. L’archive est construite sous Python 3.12 puis vérifiée en relançant les 20 tests, la démonstration et l’aide de la CLI.

Simulation par défaut ; copie uniquement sur demande explicite ; aucune suppression automatique des doublons. La restauration retire seulement les copies journalisées inchangées. Les originaux sont conservés.

Windows et macOS restent à valider. Aucun service cloud ni licence ouverte générale n’est ajouté ; lire README.md et NOTICE.md.
