# BOOTO Correcteur FLE AI — Cahier des charges V1

## Public, objectif et contexte

Enseignants de français langue étrangère, Grade 4/5 A1 et cours privés débutants. Offrir un **assistant de rétroaction** pour de courtes productions, et non un évaluateur automatique des apprenants.

## Parcours utilisateur

1. Choisir un thème : routine quotidienne (4e A1) ou écoresponsabilité (5e A1).
2. Saisir un texte fictif/anonymisé de 900 caractères maximum.
3. Consulter le texte initial et les pistes de corrections explicables par catégorie.
4. Vérifier chaque suggestion (checkbox) et refuser les corrections non souhaitées.
5. Rédiger une observation facultative.
6. Exporter une fiche Word, PDF ou TXT avec le texte initial, la version révisée et les pistes effectivement acceptées.

## Ingénierie pédagogique

Indicateurs « Je peux… » : conjuguer quelques verbes au présent, utiliser des verbes pronominaux avec « je », indiquer une heure, nommer des actions écoresponsables, reconnaître certains pluriels. Ces indices sont localisés ; ils ne constituent pas une grille exhaustive d'expression écrite CECRL.

## Architecture et périmètre

- Python standard library / expressions régulières : moteur déterministe, 20 règles ciblées, priorité aux expressions longues sans chevauchement ; chaque suggestion identifie un intervalle de texte original.
- Streamlit : consultation/révision humaine, exports ; aucune API ni base externe.
- Formats d'exports : docx (python-docx), PDF (ReportLab), TXT UTF-8.
- HTML JavaScript autonome : démo plus légère et pédagogique, pas une reproduction parfaite du moteur Python.
- Tests : entrées invalides, stabilité des suggestions, cas d'acceptation/refus, encodage, documents exportés.

## Validation et critères de réception

- Les suggestions portent sur des erreurs précisément définies ; absence de résultat ne signifie pas absence d'erreur.
- Les modifications rejetées ne doivent jamais apparaître dans le document final.
- Les sorties Word/PDF doivent préserver le texte original, montrer la version révisée, et préciser la supervision humaine.
- Aucune donnée personnelle stockée dans une base par le code ; tester uniquement avec exemples anonymisés.
- Le déploiement Render est distinct de la publication GitHub et ne doit pas modifier les services déjà existants.

## Limites et perspectives

- Pas de NLP universel ni d'analyse syntaxique complète ; fautes non prévues, accents Unicode décomposés, expressions ambiguës et autres niveaux CECRL non couverts.
- Pas de modèle ML ni de vérification externe des performances.
- V2 envisageable : règle personnalisables par enseignant, annotation des phrases, véritable grille critériée PE, validation par des relecteurs FLE, corpus anonymisé après consentement et gouvernance ; V3 : évaluation de modèles IA sur données synthétiques et sur jeux autorisés, seulement si une justification pédagogique et une politique de confidentialité solides existent.
