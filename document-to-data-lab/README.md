# Document-to-Data Lab
**Junior BOOTO Waba · Python & ingénierie des données · Prototype local**

Transformer des tableaux PDF et CSV en données contrôlées, tout en conservant l’origine de chaque ligne. Le programme distingue extraction, validation et révision humaine.

[Présentation du projet](https://junior-booto-fle.juniorbooto.chatgpt.site/document-to-data-lab.html) · [Rapport de démonstration](demo/results/report.html) · [Résultats JSON](demo/results/summary.json)

## Résultats exécutés
Sur **quatre documents entièrement fictifs** : deux PDF texte avec tableaux à bordures et deux CSV.

| Preuve | Résultat |
|---|---:|
| Lignes extraites | 9 |
| Lignes acceptées | 5 |
| Lignes à revoir | 4 |
| Document au schéma incompatible | 1 |
| Écart de total déclaré | 1 (130 USD déclaré, 125 USD lisible) |
| Cellules de données PDF conformes au mini-jeu de référence | 25 / 25 |
| Tests locaux de comportement | 22 réussis |

Montants acceptés : **65,50 USD et 30 000 COP**, comptés séparément. Les deux occurrences du doublon A001 sont mises en révision ; aucune occurrence arbitraire n’est choisie. A004 a une date impossible et un montant illisible. A007 utilise une devise hors contrat. Le texte susceptible d’être interprété comme formule de tableur est échappé dans le CSV exporté.

Ces résultats portent sur un mini-jeu contrôlé, pas sur la diversité des documents réels. Le taux 25/25 concerne les cellules des deux tableaux fictifs uniquement.

## Démarrer
Python 3.10+ et environnement virtuel recommandé.
```bash
python -m pip install -r requirements.txt
python src/lab.py demo/inputs --out reproduced
python -m unittest discover -s tests -v
```
Ouvrir `reproduced/report.html` dans un navigateur. Une sortie existante non vide est refusée. Le dossier de sortie doit se trouver hors du dossier d’entrée. Les originaux ne sont pas modifiés.

Pour régénérer les documents de démonstration dans un nouveau dossier :
```bash
python src/make_demo.py new_demo
```

## Contrat d’entrée
PDF contenant des tableaux texte à bordures ou CSV UTF-8 (virgule ou point-virgule). Colonnes `id,date,description,amount,currency` ; alias `identifiant,montant,devise,libelle` acceptés. Dates ISO `YYYY-MM-DD`. Montants non négatifs à deux décimales maximum ; séparateur décimal point ou virgule, sans séparateur de milliers. Devises USD/COP dans cette première version.

Identifiants préservés comme texte, y compris zéros initiaux. Espaces externes retirés ; devise convertie en majuscules. Autres formes monétaires ambiguës envoyées en révision plutôt que devinées.

## Architecture et sorties
`src/lab.py` : extraction → validation → détection des identifiants répétés → consolidation par devise → rapport.

| Élément | Contenu |
|---|---|
| src/ | Pipeline et génération de démonstration |
| tests/ | Cas de qualité, sécurité d’export et préservation |
| demo/inputs/ | Documents originaux fictifs |
| demo/results/ | Résultats de référence exécutés |
| docs/ | Méthode, limites et dictionnaire |
| environment.json | Versions réellement utilisées |

Sorties : `accepted.csv`, `review.csv`, `rows.json`, `summary.json`, `manifest.json`, `report.html`. Chaque ligne conserve fichier, SHA-256, page PDF, numéro du tableau et ligne dans le tableau ou CSV. Ce repère est **au niveau ligne**, pas une coordonnée de cellule. Les valeurs brutes sont conservées dans JSON.

## Apport personnel et inspiration
Association des familles « fusion CSV », « fusion PDF », « lecteur PDF/image » et « PDF vers CSV » du document *Python Projects for Developers*, Edcorner Learning, exercices 4, 5, 21 et 22. Implémentation originale ; aucun script ni PDF du livre n’est redistribué. Développement assisté par IA et vérifications exécutées, documentés sans revendication de nouveauté scientifique.

La première version réalise extraction et consolidation de données. Fusion de PDF, OCR et lecture vocale sont des extensions envisagées, **non implémentées**. Un modèle ML n’est pas nécessaire pour les règles de cette version.

## Limites importantes
PDF scannés, tableaux sans bordures, dispositions complexes et tableaux sur plusieurs pages : prise en charge non garantie ; OCR absent. Détection des doublons basée sur l’identifiant supposé unique dans le lot. Les totaux déclarés sont repérés uniquement sous la forme `TOTAL USD: 130.00` ou COP et comparés aux montants lisibles de la même page avant exclusions. Un montant illisible réduit donc le total lisible et appelle une revue. Des lignes acceptées peuvent appartenir à un document dont le total doit encore être vérifié : consulter aussi les incidents documentaires.

Le rapport public est figé ; le filtre navigateur masque/affiche des résultats déjà calculés. Aucun téléversement public, extraction dans le navigateur, serveur Python ou traitement automatisé de données personnelles n’est déployé. Tests exécutés sous Linux ; vérification visuelle navigateur non effectuée dans cet environnement.

## Licence
Code, documents fictifs et documentation originaux : MIT (voir LICENSE). Dépendances sous leurs propres licences. Le livre n’est pas inclus et aucune licence n’est revendiquée sur son contenu.

## English overview
Document-to-Data Lab is a local Python prototype for extracting bordered text-PDF tables and UTF-8 CSV files, validating expenses, retaining row provenance and keeping currencies separate. The synthetic demonstration extracted nine rows: five accepted, four requiring review, one incompatible document and one declared-total discrepancy. Twenty-two local tests passed. OCR and general-purpose document extraction are not implemented; the public report displays recorded results.
