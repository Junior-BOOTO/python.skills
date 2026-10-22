# Architecture technique — BOOTO FLE Adaptive AI V1

```text
JSON banque d'items ───────┐
                          ├─> questionnaire Streamlit ──> réponses facultatives
JSON activités ───────────┘                                   │
                                                              v
                                  engine.evaluate() : preuves / statuts
                                                              │
                                                              v
                                  engine.recommend() : règles transparentes
                                                              │
                                                              v
                                  parcours d'activités + corrigé détaillé

JSON profils SYN-* ──> engine.group_summary() ──> tableau de bord fictif
```

## Décisions de conception

1. **Moteur séparé de l'interface** : le fichier `src/booto_fle/engine.py` ne dépend pas de Streamlit et peut être testé isolément.
2. **Règles descriptives, explicables et inspectables** : aucune prétention d'IA prédictive. Le nom « Adaptive AI » est une ambition de programme, et cette V1 se limite à une adaptation par règles.
3. **Absence de données personnelles** : profils artificiels `SYN-01` à `SYN-12`; aucun nom ou identifiant d'élève réel.
4. **Banques de questions et activités hors du code** : JSON révisables, permettant une revue linguistique/pédagogique avant usages réels.
5. **Aucune réponse persistée** : le quiz ne réalise aucun enregistrement vers une base, fichier ou API.
6. **Signalement des données insuffisantes** : un item absent rend la compétence correspondante non évaluée.

## Chemins critiques à tester

- Lecture et validation des fichiers de contenu ; doublons et items incomplets.
- Note orale manuelle indépendante de la correction automatique.
- Vérification qu'une réponse manquante n'est pas assimilée à une erreur.
- Classe fictive à exactement 12 identifiants `SYN-*`.
- Cohérence de chaque recommandation avec la compétence et ses preuves.

## Évolutions possibles après validation

- Association véritable entre photos et verbes, avec illustrations sous licence appropriée.
- Production orale enregistrée **uniquement sous consentement** et conservation maîtrisée, sans notation automatique en première intention.
- Suivi formatif longitudinal pseudonymisé, avec étude éthique et cadre institutionnel.
- Comparaison expérimentale et prudente de stratégies de recommandation, sans inférence de caractéristiques sensibles ni profilage opaque.
