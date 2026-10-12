# Transfer Cost Observatory

**Junior BOOTO Waba · Python / analyse de données · MVP 1.0.0**

Comparer le montant reçu après frais et conversion, à **budget total identique**. Le programme utilise Decimal, explique les composantes de l'écart et ne classe jamais des résultats de devises différentes entre eux.

## Démonstration effectivement exécutée

3 corridors fictifs : USD→COP (Colombie), USD→CDF (RDC), USD→ZAR (Afrique du Sud). 3 budgets source (100, 500, 1 000 USD), 3 profils tarifaires A/B/C : **27 calculs**. Taux et tarifs de démonstration entièrement fictifs, sans données de clients, offres bancaires ou partenaires.

Pour le budget de 100 USD, le profil fictif C délivre le montant le plus élevé des trois ; pour 500 et 1 000 USD, le profil A passe devant. Ce changement illustre l'effet des frais fixes et proportionnels dans ce jeu de paramètres ; il ne recommande aucun prestataire réel.

Ouvrir `reports/dashboard.html` : sélectionner corridor et budget, puis déplier les calculs. Les résultats ont été calculés par Python ; le navigateur les filtre sans recalcul monétaire flottant.

## Reproduction

Python **3.10+**, aucune dépendance tierce à l'exécution. Depuis le dossier du projet :

```bash
export PYTHONPATH=src
python -m transfer_cost compare --as-of 2026-10-12
python -m unittest discover -s tests -v
```

PowerShell : remplacer la première ligne par `$env:PYTHONPATH = "src"`.

Sorties : `reports/comparison.json`, `reports/comparison.csv`, `reports/dashboard.html`. Le CSV et le JSON permettent de vérifier les résultats dans un autre outil. L'export remplace les rapports présents dans le dossier choisi ; utiliser `--output reports/new-run` pour conserver une analyse précédente.

Modifier les tarifs, budgets et précisions dans `data/scenarios.json`, puis relancer Python. Les trois lettres désignent des profils abstraits fictifs, pas des banques ou opérateurs.

## Modèle de coût et unités

Le budget total source comprend le principal envoyé, un frais fixe et un frais proportionnel appliqué au principal.

1. Principal = arrondi inférieur((budget − frais fixe) / (1 + pourcentage de frais)).
2. Frais proportionnel = arrondi demi-supérieur(principal × pourcentage).
3. Taux appliqué = taux de référence × (1 − marge de change).
4. Montant reçu = arrondi demi-supérieur(principal × taux appliqué − frais réception).

Les champs `sender_percent` et `fx_margin_percent` sont exprimés en pourcentage humain : « 2 » signifie 2 %, pas 200 %. Le frais fixe à l'envoi est en devise source ; le frais de réception est en devise cible. Le taux signifie unités de devise cible pour une unité de devise source.

Le principal est arrondi vers le bas, afin de respecter le budget. Un reliquat non dépensé peut rester (par exemple 0,01 USD). Il est affiché. Le programme n'affirme pas que le budget entier est débité si un reliquat existe.

Précision source/cible configurable de 0 à 4 décimales ; la démonstration utilise deux décimales partout. **Cette convention de démonstration ne prétend pas reproduire les règles d'arrondi d'un opérateur ou les règles spécifiques de paiement en espèces.** Les tarifs dont la précision est incompatible sont refusés. Les montants excessifs, négatifs, non finis, floats et taux nuls sont refusés.

L'écart au scénario de référence sans frais est exprimé en devise cible et en pourcentage de ce scénario. Décomposition exacte : frais source convertis au taux de référence + reliquat converti + effet de marge de change + frais réception + effet d'arrondi. L'effet d'arrondi peut être négatif ; ce n'est pas une marge de bénéfice mesurée.

Classement à montant reçu décroissant, seulement pour le même corridor et le même budget. Les égalités partagent le rang. Un scénario infaisable est expliqué et exclu du classement. Un taux manquant n'est pas remplacé par un taux fictif.

## Collecteur de taux publics : état exact

Documentation Frankfurter v2 consultée le 12 octobre 2026. Les routes `/v2/rates?base=USD&quotes=COP,CDF,ZAR` sont prévues pour des références quotidiennes. Par défaut, Frankfurter combine plusieurs sources ; le connecteur indique « default blend » et n'attribue pas chaque taux à une banque unique.

```bash
python -m transfer_cost collect --base USD --quotes COP CDF ZAR --output data/live
python -m transfer_cost compare --rates data/live/rates-reference.json --output reports/reference-scenarios
```

Une tentative HTTP réelle dans cette session a reçu **403**. Elle est consignée dans `data/collection.json`. Aucun taux réel n'a été collecté et la couverture effective des trois paires n'a pas été validée par une réponse API réussie. Le connecteur est fourni ; les contrôles de réponses sont testés avec des exemples contrôlés.

Lors d'une collecte réussie : préserver réponse brute, URL, date du taux, date de collecte et provenance ; refuser les paires inattendues ou dupliquées ; signaler celles qui ne sont pas renvoyées. Une référence âgée de plus de sept jours est signalée avec le seuil configurable ; ce seuil de démonstration n'est pas une norme métier. Week-ends, fuseaux et calendriers des sources peuvent expliquer un décalage de publication.

La collecte est distincte des calculs. Même si des références publiques sont disponibles, les profils tarifaires restent fictifs. Le MVP refuse les tarifs déclarés « réels » : une extension avec des offres authentiques devra aussi vérifier dates de validité, conditions et comparabilité.

Les taux de référence ne sont pas des offres exécutables. En particulier, la BCE publie ses références à titre informatif et déconseille de les utiliser pour des transactions. Aucun transfert, compte bancaire, décision financière individuelle ou alerte de fraude n'est implémenté.

## Preuves et limites

20 tests réussis localement sous Linux : calculs sans frais, unités, pourcentage appliqué au principal, décomposition, arrondis, budget conservé, entrées interdites, classement et égalités, taux manquants/futurs/anciens, provenance, scénarios impossibles et exports.

La syntaxe JavaScript du tableau de bord est vérifiée ; le rendu visuel complet en navigateur reste non réalisé. Les données fictives rendent le calcul reproductible sans clé ni accès réseau.

Taxes, frais d'intermédiaires, délais, plafonds, méthodes de paiement et garanties de réception ne sont pas modélisés. Pas de surveillance continue ni de notifications envoyées. Ce projet apporte un calcul transparent et des preuves, pas un comparateur commercial exhaustif.

## Attribution et références

Conçu pour Junior BOOTO Waba avec assistance de ChatGPT. Inspiration conceptuelle : chapitre conversion monétaire de *Python Projects With API*, Minal Pandey. Aucun code ou PDF du document n'est redistribué. Les fixtures tarifaires et de taux sont originales et synthétiques.

- https://frankfurter.dev/ — documentation v2, sources et mélange par défaut.
- https://frankfurter.dev/javascript/ — filtres base/quotes et fournisseur.
- https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html — portée informative des références.

Licence du code original à choisir par l'auteur avant redistribution sous licence ouverte. Projet présenté dans le portfolio Python/data : [tableau de bord](https://junior-booto-fle.juniorbooto.chatgpt.site/transfer-cost-observatory.html) · [code et tests](https://github.com/Junior-BOOTO/python.skills/tree/main/transfer-cost-observatory). La démonstration reste entièrement synthétique.
