# Plan de tests et critères de validation

## Tests déjà prévus (automatisés)

- Validation du CSV : colonne obligatoire, lignes vides et nombre de lignes.
- Tokenisation multilingue et respect du texte original.
- Exécution du pipeline supervisé sans fuite du jeu de test.
- Sortie de prédiction et conservation des identifiants.
- Extraction de mots-clés et voisinage de similarité.
- Répartition et volume du jeu synthétique.

Exécuter : `python -m pytest -q`.

## Tests d'acceptation à réaliser (non réalisés)

| Critère | Jeu | Objectif |
|---|---|---|
| Langues FR/EN/ES | >=60 nouveaux textes manuellement validés, >=10 mots | exactitude >=95 % |
| Classification | corpus indépendant représentatif avec annotations vérifiées | macro-F1 >=0,75 |
| Débit | 300 documents <=2 000 caractères, ordinateur 8 Go RAM | <30 sec après chargement modèles |
| CSV | document 300 lignes | import et export sans perte |
| Erreurs | CSV absent, incorrect, vide | messages explicites |
| Interface | tests manuels depuis navigateur | onglets, graphiques, export opérationnels |

## Mise en garde

Le jeu `corpus_300_demo.csv` contient des phrases synthétiques et des structures répétitives. Les métriques qu'il produit sont indicatives de l'exécution du code, non de la précision réelle d'un modèle déployable.
