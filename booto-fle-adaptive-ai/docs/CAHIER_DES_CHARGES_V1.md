# Cahier des charges officiel — BOOTO FLE Adaptive AI V1

**Statut : spécification du prototype expérimental**  
**Responsable : Junior BOOTO Waba**  
**Version : 0.1 / 21 octobre 2026**

## 1. Contexte et ambition

Créer une aide à la différenciation formative en FLE, en combinant ingénierie pédagogique et programmation Python. Point de départ : la séquence PYP « Qui nous sommes », thème « Ma journée typique », niveau A1, Grade 4, 45 minutes. Le logiciel ne remplace pas l'évaluation humaine.

## 2. Utilisateurs cibles

**Apprenant** : répondre à un court questionnaire textuel et consulter des activités proposées. **Enseignant FLE** : observer les besoins par compétence, comprendre les recommandations et préparer les activités suivantes. **Évaluateur/portfolio** : inspecter la logique, les tests, les données fictives et les limites.

## 3. Objectifs pédagogiques

- Reconnaître les actions quotidiennes courantes.
- Employer **je me lève / je me prépare / je me couche**.
- Organiser une routine avec **le matin / ensuite / enfin**.
- Donner une heure avec **à** (précis) ou **vers** (approximatif).
- Décrire oralement sa journée en **trois phrases et une heure** : observation manuelle.

**Limite majeure :** le critère initial d'association d'au moins six activités à des images n'est pas encore couvert dans V1 ; les questions de vocabulaire sont textuelles.

## 4. Exigences fonctionnelles

| Code | Exigence | Vérification |
| --- | --- | --- |
| F01 | Questionnaire A1 de 12 questions avec 3 options | Banque chargée et contrôlée |
| F02 | Quatre domaines écrits, chacun avec 3 questions | Validation du schéma |
| F03 | Corrigé et explications individualisés par réponse | Correspondance question/réponse |
| F04 | Ne pas tirer de conclusion si une question d'une compétence manque | Statut « non évalué » |
| F05 | Entrée d'observation orale volontaire de 0 à 2 | Pas d'inférence de voix |
| F06 | Jusqu'à trois recommandations ordonnées par priorité | Motif de recommandation affiché |
| F07 | Activités courtes avec aide, approfondissement et réussite | Catalogue JSON vérifié |
| F08 | Tableau de bord d'une classe **entièrement fictive** | 12 profils SYN-* et répartition des statuts |
| F09 | Interface Streamlit avec deux espaces et explication des règles | Navigation locale |
| F10 | Tests automatisés reproductibles | pytest et script sans interface |

## 5. Règles d'adaptation V1

Pour **chaque groupe complet de trois réponses** : 2 à 3 justes -> acquis sur ces tâches ; 1 juste -> en cours ; 0 juste -> à renforcer. Groupe incomplet -> non évalué. Pour l'oral, seule une observation **humaine** attribue 0, 1 ou 2 ; sans observation -> non évalué. Les activités sont proposées en commençant par les catégories « à renforcer », puis « en cours ». Aucune décision cachée ou automatisation de suivi des enfants.

## 6. Contraintes techniques

Python 3.11+, moteur fondé sur la bibliothèque standard, interface Streamlit, banque et ressources JSON, tests pytest. Hors réseau pour le moteur, sans compte, sans API payante, sans base de données et sans stockage persistant des réponses. Architecture facile à auditer et extensible à d'autres thèmes et niveaux après validation.

## 7. Critères de réussite V1

- Les **12 items** s'affichent et donnent un corrigé exact.
- Les cinq compétences ont un statut descriptif et une raison compréhensible.
- Les compétences non suffisamment évaluées ne sont pas classées à tort en difficulté.
- Les recommandations sont cohérentes avec les résultats et incluent une activité, une durée, un soutien et un indicateur de réussite.
- Le tableau de bord fictif présente 12 profils sans données personnelles.
- Les tests passent, le script console fonctionne ; l'interface web doit être vérifiée séparément après installation de Streamlit.

## 8. Hors périmètre V1

Reconnaissance vocale, correction libre par LLM, analyse d'images, génération de contenu personnalisée, suivi d'élèves réels, indicateur CECRL certifié, classement d'enfants, automatisation des décisions pédagogiques, impact pédagogique démontré. Ces fonctionnalités nécessitent cadrage, consentement, évaluations et garanties spécifiques.

## 9. Livrables

Code source, interface Streamlit, banque de questions, catalogue d'activités, douze profils fictifs, scénarios de tests, cahier des charges, architecture et note de validation/éthique.
