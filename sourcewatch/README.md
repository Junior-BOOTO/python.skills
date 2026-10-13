# SourceWatch — veille documentée
**Junior BOOTO Waba · Python, RSS et provenance · Prototype exécuté**

[Présentation sur mon site](https://junior-booto-fle.juniorbooto.chatgpt.site/sourcewatch.html) · [Collecte enregistrée](demo/live/snapshot.json) · [Preuves de validation](docs/validation.json)

## Ce que fait cette version
Collecter les métadonnées d’un flux RSS officiel, distinguer publication et collecte, expliquer le classement par mots-clés, grouper les URLs identiques sans perdre les observations et comparer deux snapshots.

Version initiale limitée au flux [Python Insider](https://www.python.org/blogs/), sans compte ni clé payante. Aucun corps d’article, commentaire ou profil personnel n’est collecté. Les liens d’articles sont affichés mais pas téléchargés.

## Résultats réellement exécutés
| Vérification | Résultat |
|---|---:|
| Éléments disponibles dans le flux | 50 |
| Éléments examinés et conservés | 20 |
| Erreurs de parsing dans l’échantillon | 0 |
| Groupes d’URLs canoniques | 20 |
| Tests Python locaux | 25 réussis |
| Relecture du cache de métadonnées | Empreintes des métadonnées identiques |

Collecte réelle du 13 octobre 2026 ; heure exacte dans `demo/live/snapshot.json`. Échantillon partiel, pas toutes les actualités Python ni toutes les nouvelles de l’IA éducative. Les mots-clés sont recherchés seulement dans le titre ; leur présence ne mesure ni la fiabilité, ni la qualité, ni le niveau d’intérêt réel.

## Comparaison contrôlée, séparée du réel
Deux flux **fictifs** permettent de vérifier : un élément nouveau, un titre modifié, un élément inchangé et un élément absent du second snapshot. Les dates de collecte seules ne constituent pas une modification. « Absent » n’est jamais présenté comme « supprimé » : un flux limité peut changer de fenêtre.

## Reproduire sans réseau
Python 3.10+ ; aucune dépendance tierce.
```bash
python src/watch.py --offline demo/cache/python_metadata.xml --out reproduced/live
python src/watch.py --offline demo/fixtures/before.xml --out reproduced/before
python src/watch.py --offline demo/fixtures/after.xml --previous reproduced/before/snapshot.json --out reproduced/after
python -m unittest discover -s tests -v
```
Ouvrir un `report.html` produit. Le cache XML est une reconstruction des **métadonnées** collectées, pas la réponse réseau originale. Il n’inclut pas les descriptions. L’empreinte de la réponse réseau complète est conservée dans le snapshot réel.

## Nouvelle collecte ponctuelle
```bash
python src/watch.py --out new_collection --limit 20
python src/watch.py --out next_collection --limit 20 --previous new_collection/snapshot.json
```
Les dossiers de sortie doivent être neufs. Une requête, timeout 20 secondes, réponse limitée à 2 Mo, domaine de redirection limité à blog.python.org. En cas de 429, timeout ou format invalide, l’incident est enregistré et le programme s’arrête sans contournement. Cette version ne relance pas automatiquement les requêtes.

## Architecture
| Dossier | Rôle |
|---|---|
| src/ | Collecte RSS, normalisation, classement, comparaison et rapport |
| tests/ | Erreurs HTTP, limites, provenance, dates, URLs et changements |
| demo/live/ | Métadonnées réelles et rapport figé |
| demo/cache/ | Cache minimal de métadonnées pour reproduction |
| demo/fixtures/ | Flux fictifs avant/après |
| demo/before et demo/after | Comparaison fictive exécutée |
| docs/ | Méthode, droits et résultats de validation |

Chaque observation conserve source, GUID, URL canonique, date publiée si disponible, date de collecte, raisons de classement et empreinte des métadonnées. La clé combine source et GUID (URL comme repli). Les paramètres utm_*, fbclid et gclid ainsi que fragments sont retirés ; les autres paramètres sont conservés. Deux titres identiques avec des URLs distinctes ne sont pas fusionnés. Les groupes d’URLs gardent les observations de toutes leurs sources.

## Limites
RSS 2 seulement, source fixe. Pas d’Atom, pagination de flux, extraction HTML générique, résumé génératif, lecture vocale ou serveur de veille permanent. La comparaison suit les métadonnées, pas les modifications du corps d’un article. Une clé répétée rend la comparaison ambiguë et la bloque. Liens publics filtrés mais destinations d’articles non vérifiées. Aucun calendrier automatique installé.

Le rapport web affiche des résultats enregistrés. Son filtre est exécuté dans le navigateur ; il ne lance pas de collecte. Vérification visuelle navigateur non effectuée dans l’environnement de réalisation.

## Inspiration et droits
Familles de projets 11, 12 et 41 de *Python Projects for Developers*, Edcorner Learning : actualités, collecte et veille. Implémentation originale assistée par IA ; aucun code ou livre tiers redistribué.

Code et fixtures fictives : MIT. Métadonnées Python Insider : attribution à la Python Core Team ; la page Python.org annonce CC BY-NC-SA 3.0 pour Python Insider. Voir [droits et méthode](docs/methode.md). La licence MIT du code ne s’étend pas aux données tierces.

## English overview
SourceWatch is a local Python RSS prototype with a real, bounded Python Insider metadata collection and a separate synthetic snapshot comparison. Twenty real entries were retained from fifty available feed items; twenty-five local tests passed. Source links, UTC publication/collection dates and explainable title keywords are preserved. No article bodies, background monitoring or live web service are provided.
