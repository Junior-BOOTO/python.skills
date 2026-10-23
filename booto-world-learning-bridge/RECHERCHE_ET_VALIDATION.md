# BOOTO WORLD LEARNING BRIDGE V1 — Recherche, protocole et limites

## Hypothèse de conception

**À vérifier :** conserver des observations d'activités d'apprentissage quand l'apprenant passe d'une modalité 2D guidée à un jeu 3D réduit la fragmentation du retour pédagogique et améliore la compréhension de son parcours. Cela ne signifie pas que l'apprentissage s'améliore automatiquement.

## Innovation testable

Une **même mission écologique francophone** sur deux supports, avec les mêmes intentions didactiques (identifier, demander, proposer, transmettre), trois langues d'accompagnement pour le mode guidé et un **passeport pédagogique portable, explicable et sans identité**.

Il s'agit d'une combinaison expérimentale, pas de l'affirmation qu'aucun outil équivalent existe.

## Démonstration V1

1. Compléter la mission 2D guidée avec la langue d'interface ES puis recommencer en FR.
2. Ouvrir le monde 3D ; compléter une fois la mission de recyclage et une fois la plantation.
3. Vérifier que le passeport 3D distingue les chemins, compte les indices et propose trois répliques pertinentes de chaque parcours.
4. Vérifier qu'une réponse erronée n'est pas enregistrée comme preuve de réussite.
5. Exporter le JSON unifié ; vérifier ses deux sources et le champ `learner_identity: null`.
6. Essayer l'import depuis un fichier exporté par la démo 3D séparée, ainsi que le refus d'un fichier invalide.
7. Vérifier les contrôles clavier, le mode essentiel, la lisibilité mobile et l'expérience lorsque WebGL manque.

## Critères et données

Éléments techniques contrôlables : cohérence du chemin, présence de traces en français, compteurs d'aide et de tentatives, validation du schéma, export hors ligne. **Aucune compétence CECRL ne peut être certifiée par ces exercices guidés.**

Aucune donnée nominative ni histoire personnelle d'élève ; l'hébergement statique n'impose pas de base de données, mais Render peut enregistrer des logs de consultation. En cas d'expérimentation avec enfants, prévoir consentement institutionnel et parental, revue éthique et validation par des enseignants indépendants.

## Conditions de validation scientifique future

Étude exploratoire : observer les erreurs, recueillir un retour des enseignants et des apprenants, mesurer la clarté du feedback et l'accessibilité. Ensuite seulement, concevoir une expérimentation comparative avec mesures pré/post et critères prédéfinis. Ne pas qualifier les indicateurs internes du logiciel d'amélioration effective de l'apprentissage.