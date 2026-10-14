# MessageLens — comprendre une classification de SMS
**Junior BOOTO Waba · NLP, validation par groupes et explications · Prototype expérimental**

[Démonstration sur mon site](https://junior-booto-fle.juniorbooto.chatgpt.site/messagelens.html) · [Résultats exécutés](reports/metrics.json) · [Modèle JSON](reports/model.json)

## Objectif et apport
Associer classification de spam et comparaison textuelle : montrer un score, les contributions des mots et les limites de la décision. Prototype pour examiner une méthode, pas pour certifier qu’un message est sûr ou frauduleux.

Le site exécute réellement le modèle exporté dans le navigateur, sans envoi du texte saisi à un serveur d’inférence. Il permet aussi de comparer deux textes fictifs par Jaccard de trigrammes. Cette comparaison ne constitue pas une preuve de plagiat ni un score de spam.

## Source et périmètre
SMS Spam Collection, Almeida & Hidalgo (2011), UCI, DOI [10.24432/C5CC84](https://doi.org/10.24432/C5CC84), licence CC BY 4.0 selon la fiche UCI. Corpus historique de SMS anglais. Archive publique téléchargée ; empreinte dans `reports/metrics.json`. Les SMS bruts ne sont pas republiés dans ce dépôt ; seuls résultats agrégés, identifiants de lignes retenues et modèle sont distribués. Les exemples d’interface sont originaux et fictifs.

5 574 messages lus ; 3 sans token ASCII exploitable exclus, 5 571 retenus dont 747 spams. Les nombres, URL et courriels sont remplacés par marqueurs. Cette simplification limite l’analyse réelle du phishing.

## Éviter une évaluation trompeuse
Les messages identiques après normalisation et les messages très proches sont regroupés sans leurs étiquettes : hachage caractère 3–5 grammes, 65 536 dimensions, similarité cosinus >= 0,94, composantes connexes. 5 007 groupes ; zéro groupe partagé entre partitions.

Répartition par groupes avec graines fixes : 3 320 messages d’entraînement, 1 103 de validation, 1 148 de test. TF-IDF unigramme (maximum 5 000 termes) et régression logistique équilibrée. Vocabulaire et IDF appris seulement sur entraînement. Seuil choisi parmi 0,3 / 0,5 / 0,7 sur F1 validation, départage par précision : **0,5**. Aucun réglage sur test ni réentraînement après sélection. Ce test est désormais consulté : ne pas le réutiliser pour sélectionner de nouvelles variantes.

## Résultats sur les 1 148 SMS de test
| Méthode | Précision spam | Rappel spam | F1 spam |
|---|---:|---:|---:|
| Référence : toujours ham | 0 % | 0 % | 0 |
| TF-IDF + logistique | 92,74 % | 93,26 % | 0,930 |

Matrice : 957 ham correctement classés, **13 faux positifs**, **12 spams manqués**, 166 spams détectés. 178 spams dans le test. Ces pourcentages décrivent cet échantillon historique ; ils ne garantissent pas une performance sur les SMS actuels, les courriels ou d’autres langues.

## Reproduire
Python 3.10+, installation dans un environnement virtuel conseillé.
```bash
python -m pip install -r requirements.txt
python src/lens.py --out reproduced
python -m unittest discover -s tests -v
```
Pour une archive UCI déjà téléchargée : ajouter `--archive chemin/sms.zip`. Sortie existante non vide refusée. `environment.json` conserve les versions effectivement utilisées.

`model.json` exporte vocabulaire, IDF, coefficients, intercept et seuil. L’inférence JSON rechargée reproduit tous les scores du test à moins de 1e-10. La version JavaScript a également été comparée à Python sur **5 579 cas** (corpus complet + frontières), erreur maximale 4,45e-16. **17 tests Python locaux réussis**. Vérification visuelle navigateur non réalisée.

## Explications et similarité
Contribution d’un terme = TF-IDF normalisé × coefficient. Contribution positive : pousse vers spam ; négative : vers ham. L’intercept intervient aussi ; seules les huit contributions les plus fortes sont affichées. Ces poids expliquent ce modèle linéaire, pas les intentions de l’expéditeur. Le score logistique n’a pas été calibré indépendamment et n’est pas une probabilité de fraude.

Le comparateur de deux textes emploie Jaccard sur ensembles de trigrammes après normalisation. Il diffère du regroupement de corpus, qui utilise le cosinus de hachages 3–5 grammes. Similarité et classement spam sont deux observations distinctes.

## Organisation
| Dossier | Contenu |
|---|---|
| src/ | Entraînement Python, inférence JavaScript et interface |
| tests/ | Normalisation, groupes, métriques, rechargement |
| reports/ | Scores, partitions, prédictions sans texte brut, modèle et exemples fictifs |
| docs/ | Fiche modèle et validation |

## Limites et droits
Modèle anglais historique, normalisation ASCII, regroupement approximatif avec collisions possibles du hachage et similarité transitive. Ni la protection complète contre les doublons sémantiques, ni la robustesse à l’obfuscation ou au changement de langue ne sont démontrées. Pas de connexion à une messagerie, suppression de SMS, blocage automatique ou détection générale de fraude. Les faux positifs imposent une revue humaine.

Inspiration : exercices 6 (spam) et 23 (similarité textuelle) de *Python Projects for Developers*, Edcorner Learning. Implémentation originale assistée par IA, livre et scripts non redistribués. Code/documentation originaux sous MIT ; données UCI et résultats dérivés attribués sous CC BY 4.0. La licence du code ne remplace pas celle des données.

## English overview
An English SMS spam prototype combining grouped holdout evaluation, linear term explanations and a separate text-similarity tool. On 1,148 held-out SMS, it detected 166 of 178 spam messages, with 13 false positives and 12 missed spam messages. Browser-side JSON inference was numerically checked against Python. Historical benchmark performance does not certify message safety or fraud.
