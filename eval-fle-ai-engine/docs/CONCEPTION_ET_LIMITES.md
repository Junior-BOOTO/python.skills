# Conception pédagogique et limites — Éval’FLE AI Engine V1

## Objectif de la V1

Créer des QCM imprimables avec un **corrigé séparé**, une **grille de réponses**, un **barème uniforme** et des critères « Je peux… ». L'enseignant sélectionne le grade, le nombre de questions et une variante reproductible. Le projet ne prétend ni certifier un niveau CECRL ni remplacer l'expertise d'un professeur.

## Contenu disponible

- Grade 4 A1 : maison (10), paysages naturels (10), journée typique (10).
- Grade 5 A1 : droits et devoirs (10), écoresponsabilité (10), communication quotidienne (10).
- Chaque QCM comporte **quatre choix** et **exactement une réponse prévue**.
- 12, 15 ou 30 questions ; répartition équilibrée en trois domaines, ordre mélangé, options mélangées, corrigé synchronisé.
- Formats de sortie : Word `.docx` et PDF, versions élève et enseignant.

## Ce que ce projet ne démontre pas

Les thèmes de cette banque sont **illustratifs**, même si certains sont cohérents avec les ressources pédagogiques développées par l'auteur. Ils ne constituent pas une transcription validée des programmes annuels de Grade 4 et de Grade 5 ni une couverture garantie des trois périodes scolaires. L'enseignant doit vérifier les consignes, le lexique, les distracteurs, la pertinence culturelle et la correspondance avec ses propres objectifs.

La V1 est **un moteur de règles et de mise en page, sans IA générative ni système adaptatif**. L'acronyme « AI » correspond à l'orientation du laboratoire et à la feuille de route, pas à une capacité d'évaluation automatique fondée sur des modèles entraînés.

Les QCM sans audio ni production libre examinent surtout des reconnaissances et connaissances linguistiques : ils ne mesurent pas directement la compréhension orale, la production orale ou la production écrite. Aucun diagnostic CECRL officiel n'est inféré d'un score. Aucun élève réel n'a participé à une validation expérimentale.

## Confidentialité

Pas d'API externe, de base de données, de compte apprenant ou d'upload de copies dans le projet. La saisie de réponses anonyme dans la session Streamlit ne génère aucune sauvegarde par le code de l'application. L'hébergeur peut conserver des traces techniques selon sa propre politique ; éviter toute donnée personnelle d'élève.

## Roadmap raisonnable

1. Faire relire la banque par un enseignant FLE et corriger les items discutables.
2. Importer les programmes officiels des trois périodes avant de présenter les évaluations comme « annuelles ».
3. Ajouter la création éditoriale guidée d'items, avec relecture humaine obligatoire.
4. Intégrer ultérieurement les quatre compétences avec supports et observations séparés.
5. Expérimenter en contexte avec accord institutionnel et protections des mineurs.
