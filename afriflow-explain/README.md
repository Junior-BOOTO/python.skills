# AfriFlow Explain — Junior BOOTO Waba

**Explorer les parcours, expliquer les alertes, mesurer les limites.** Projet de portfolio original dans sa réalisation, inspiré de méthodes de réseaux financiers existantes. Démonstration 100 % synthétique : aucune banque connectée, aucun partenariat, aucune donnée personnelle réelle.

## Expérience interactive
[Ouvrir la démonstration](https://junior-booto-fle.juniorbooto.chatgpt.site/afriflow-explain.html).
Choisir un dossier, avancer dans la chronologie, cliquer sur un motif, voir les identifiants de ses opérations et consulter la qualité des horodatages. La vérité de simulation est masquée dans un volet séparé ; elle sert à l'évaluation, pas aux explications.
38 dossiers illustratifs sont inclus dans la page : 20 aux scores parcours les plus élevés, des exemples de chaque scénario et de données temporelles partielles. Cet échantillon n'est pas représentatif. Les scores globaux portent sur tous les 360 dossiers de test. Le ZIP complet contient les 1 800 dossiers, modèles et sources.

## Trois rôles coordonnés
| Rôle | Travail réellement exécuté |
|---|---|
| DataCollect | Génération et conservation de la source, types, identifiants, devises et couverture temporelle |
| DataAnalyse | Composantes connexes, motifs temporels, preuves par identifiants, qualité et dossiers explicatifs |
| DataML | Deux Isolation Forest, même configuration et budget d'alertes, test chronologique et modèles rechargés |

Le script partagé lit les fichiers des étapes précédentes sans transfert manuel. Aucun appel aux GPT indépendants, aucune Action GPT installée et aucun échange automatique entre leurs conversations n'est revendiqué.

## Reproduction
Python 3.12 testé.
```sh
python -m pip install -r requirements.txt
python pipeline.py
python build_demo.py
python -m unittest discover -s tests -v
```
Ouvrir dashboard.html. Les liens vers le portfolio et le téléchargement désignent la version publique du site ; les interactions de la page sont autonomes et ne nécessitent pas Internet. Les versions exactes sont enregistrées dans reports/versions.json.

## Données, unité et chronologie
11 775 transferts, 1 800 composantes, 60 jours à partir du 1er janvier 2025. Générateur original local seed=73 ; **ce ne sont ni PaySim ni des données Ecobank**. Institutions A/B/C et comptes fictifs. Contextes Nigeria, Ghana, Kenya et Rwanda, devises NGN/GHS/KES/RWF ; distributions arbitraires, aucune représentativité économique ou taux de change revendiqués.
Une unité d'analyse est une composante connexe non orientée, dans une devise et une fenêtre UTC de 24 heures. L'orientation des transferts est ensuite conservée pour les motifs. Analyse rétrospective une fois la fenêtre close, pas alerte instantanée. Pas d'addition entre devises, ni d'analyse de conversion.
Les groupes de comptes du générateur sont disjoints : ils facilitent artificiellement la séparation des dossiers. Le code calcule les composantes à partir des relations, puis rapproche les labels de simulation ; les identifiants de dossiers ne sont pas des features. Les réseaux réels, beaucoup plus interconnectés, exigent un autre découpage et des vérifications métier.
205 opérations ont un horodatage volontairement masqué, indépendamment du scénario. Elles restent dans le dossier et les statistiques descriptives ; elles sont exclues des motifs temporels. Les dates ISO à précision variable sont parsées avec format='mixed', et le test vérifie que le compteur d'heures absentes égale le nombre d'absences source. Le score de couverture mesure seulement les horodatages présents parmi les opérations observées ; il n'établit pas l'exhaustivité.

## Motifs et interprétation
Deux motifs explicatifs : circuit d'au moins trois transferts revenant vers le compte de départ, ou chaîne d'au moins trois transferts reliés. Ordre strict des dates, moins de 10 minutes entre étapes, durée totale ≤30 minutes et ratio de montants entre 0,7 et 1,3. Ces paramètres sont des critères de démonstration fixés avant l'évaluation, **pas des seuils réglementaires**.
Les identifiants exacts des opérations constituent les preuves observables. Les montants compatibles ne prouvent pas le passage des mêmes fonds : comptes fongibles, historique incomplet et autres activités peuvent expliquer le motif. Les parcours sont des explications du dossier ; ils ne sont pas des attributions causales du score Isolation Forest.
Scénarios injectés : rapid_cycle et rapid_relay. Situations légitimes difficiles : circuits, chaînes, paie groupée, collecte et opérations aléatoires. Certains parcours légitimes sont aussi rapides. Pas de jugement sur un pays, une devise ou une institution.

## Évaluation indépendante à budget égal
Entraînement avant le 6 février : 1 080 dossiers. Validation 6–17 février : 360. Test 18 février–1er mars : 360. Comptes disjoints ; pas d'identifiant commun entre périodes.
Deux Isolation Forest : 160 arbres, max_samples=256, seed=73. Aucune étiquette d'anomalie utilisée pour apprendre ni régler. Normalisation des montants par la médiane d'entraînement de chaque devise. Configuration et features fixées avant test ; aucune recherche d'hyperparamètres. Les deux méthodes sont comparées, sans sélection postérieure d'une nouvelle configuration.
- **Transactions seules** : médiane, maximum, écart type des montants normalisés, nombre d'opérations du dossier.
- **Transactions + parcours** : mêmes features, circuits et chaînes temporels, degrés entrants/sortants, nombre de comptes, durée observée.
Budget fixé à 10 % des dossiers, soit 36 alertes par méthode sur validation et sur test. Priorisation par rang décroissant, départage stable. Ce seuil de rang utilise les scores du lot de test, jamais ses labels ; c'est une revue par lot, pas un seuil de production figé.

| Test synthétique (42 scénarios injectés) | Alertes | Vrais positifs | Faux positifs | Anomalies manquées | Rappel |
|---|---:|---:|---:|---:|---:|
| Transactions seules | 36 | 3 | 33 | 39 | 7,1 % |
| Transactions + parcours | 36 | 19 | 17 | 23 | 45,2 % |

Précision : 8,3 % contre 52,8 %. Average Precision : 0,130 contre 0,547. Proportion d'anomalies test : 42/360 = 11,7 %. Le gain de rappel est 38,1 points, pas 38,1 % de précision globale. Intervalle exploratoire bootstrap 95 % : [23,8 ; 57,8] points, 300 rééchantillonnages de dossiers, conditionnel au générateur. Il n'intègre pas l'incertitude du simulateur ni celle de nouveaux établissements.
Les modèles ne sont pas calibrés en probabilités de fraude. Les résultats portent sur des scénarios conçus avec des motifs que les features cherchent à détecter ; ce biais favorable est explicite. **Aucune performance bancaire réelle ou détection de blanchiment n'est démontrée.**

## Vérifications et livrables
Six tests : ordre temporel, opérations simultanées, cycle invalide, budget égal, composantes, absence des labels/identifiants des features et ancrage de toutes les preuves. Modèles exportés et rechargés, scores reproduits sur 20 dossiers test. Syntaxe JavaScript vérifiée ; la disponibilité d'un outil de navigateur conditionne la vérification visuelle complète (non réalisée dans cette session).
models/ contient les modèles avec normalisation et noms des variables, metrics.json et test_cases.csv. analysis/cases.json contient les dossiers et la vérité de simulation clairement séparée des motifs. raw/ conserve les données et labels. manifest.json décrit le statut et l'empreinte source. Ne charger que les joblib de provenance fiable.

## API et prochaine étape bancaire
Aucune API bancaire connectée. Ce projet ne dépend pas d'un compte bancaire pour être essayé. Le prototype AfriTransfer Watch contient un connecteur Flutterwave sandbox de lecture d'une page ; son authentification et son mapping restent à vérifier avec des accès de test. Ecobank est une cible de future intégration, sans endpoint opérationnel supposé.
Pour raccorder une source réelle : vérifier historique autorisé, identifiants interinstitutions, dates/fuseaux, unités, devises, pagination et conditions d'usage ; pseudonymiser ; séparer les réponses privées de la démonstration publique ; reconstruire et recalibrer les fenêtres, sans transférer les scores synthétiques. Pour des parcours entre banques, une API de son seul compte ne donne pas automatiquement une vue interbancaire complète.
Pas de blocage de fonds, pas de qualification juridique automatique, pas de traitement réel en continu. Les anomalies restent des dossiers pour revue humaine.

## Références
Les méthodes de réseaux financiers existent : BIS Project Aurora (https://www.bis.org/project/aurora), Project Hertha (https://www.bis.org/project/hertha), IBM AMLSim (https://github.com/IBM/AMLSim). Ces projets inspirent la méthode ; leurs jeux et modèles ne sont pas intégrés ici. Documentation consultée le 12 octobre 2026. L'apport de ce portfolio est la réalisation d'une revue interactive, l'ancrage des motifs dans les opérations et la comparaison honnête à budget égal.
