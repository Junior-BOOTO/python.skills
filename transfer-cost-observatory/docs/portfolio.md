# Transfer Cost Observatory — Junior BOOTO Waba

## Comparer le montant reçu à budget total égal

Ce prototype Python transforme un exercice de conversion monétaire en analyse explicable des coûts : principal, frais à l'envoi, marge de change, frais à réception, reliquat et arrondis. Chaque résultat possède une décomposition vérifiable.

Trois corridors de démonstration relient USD à COP, CDF et ZAR. Avec trois budgets et trois profils fictifs, le programme produit 27 scénarios. Les classements restent limités à un même corridor et budget. Le profil en tête peut changer avec le budget : cela démontre un effet de structure des frais, pas une performance d'une banque.

## Preuves techniques

Calculs Decimal, entrées validées, exports JSON/CSV, tableau de bord filtrable, provenance des taux et gestion des données absentes. Vingt tests passent localement ; résultats conservés dans reports/validation.json.

La tentative de collecte Frankfurter v2 a reçu HTTP 403. La démonstration est donc entièrement synthétique. Le connecteur fourni ne vaut pas une connexion bancaire ; aucun transfert n'est déclenché. Le rendu visuel en navigateur reste à vérifier.

## English summary

Transfer Cost Observatory is an explainable Python MVP that compares recipient amounts at equal total sender budgets. Decimal arithmetic separates sender fees, FX margin, receiver fees, unspent funds and rounding. Twenty tests pass locally across twenty-seven synthetic scenarios. A public reference-rate connector is included, but the live request received HTTP 403; no real rates or provider tariffs are claimed.

## Grille interne de conception

| Critère | Note / 2 | Justification |
|---|---:|---|
| Utilité | 2 | Explique une différence de coût à budget constant. |
| Reproductibilité | 2 | Fixtures, paramètres et exports sans dépendance réseau. |
| Robustesse | 1 | Calculs et contrôles testés ; collecte réelle et navigateur limités. |
| Preuves | 2 | Tests, 27 calculs et tentative réseau conservés. |
| Documentation | 2 | Formules, unités, hypothèses et limites explicités. |

9/10 selon cette grille interne, ni certification ni validation financière.
