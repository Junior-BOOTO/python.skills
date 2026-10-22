# Cahier des charges — PhonoFLE AI V1

**Document de cadrage du prototype · 22 octobre 2026**  
**Responsable : Junior BOOTO Waba**  
**Projet : BOOTO AI & DATA INNOVATION LAB / PhonoFLE AI V1**  
**Statut : phase de développement / validation formative, pas un produit certifié**

## 1. Vision et problème

Favoriser l'apprentissage de la phonétique du français par une démarche progressive : perception, choix d'un mot entendu, explicitation de l'erreur, remédiation articulatoire, observation humaine de la production. Le premier contraste est /y/ (« u ») face à /u/ (« ou »), particulièrement utile chez les apprenants hispanophones mais sans limiter le public à une langue maternelle.

La proposition de valeur est la **traçabilité pédagogique de chaque recommandation** : un conseil découle d'une confusion observée dans des réponses explicites. Il ne s'agit pas d'un système de diagnostic de troubles de la parole.

## 2. Publics cibles

- Apprenants du primaire (grades 3–5) au niveau A1, sous accompagnement d'un enseignant ; adaptation aux adolescents et adultes débutants.
- Enseignants FLE souhaitant un atelier phonétique court, des critères « Je peux » et un suivi formatif sans traitement de voix d'élèves.
- Formateurs et responsables pédagogiques souhaitant évaluer l'intérêt du concept sur une démonstration contrôlée.

## 3. Objectifs d'apprentissage

**Perception :** sélectionner le mot correct dans au moins 8 stimuli sur 10 dans un diagnostic guidé (objectif pédagogique de travail ; non atteint de facto). **Compréhension phonologique :** relier le changement /y/ → /u/ à deux mots de sens différent. **Production :** répéter au moins trois mots contrastés sous observation de l'enseignant. **Métacognition :** reconnaître les deux placements articulatoires principaux.

## 4. Périmètre fonctionnel obligatoire

| ID | Fonction | Critère d'acceptation |
|---|---|---|
| F01 | Banque de paires minimales | Au moins 10 paires identifiées, transcrites en API, relues par l'enseignant |
| F02 | Diagnostic interactif | 10 items, chaque item présente 2 choix ; cibles /y/ et /u/ équilibrées |
| F03 | Écoute | Déclenchement par clic, vitesse normale et lente ; message si voix indisponible |
| F04 | Feedback | Affiche immédiatement la bonne réponse, le mot cible et sa transcription |
| F05 | Analyse des confusions | Distingue les erreurs portant sur les cibles /y/ et /u/ |
| F06 | Recommandations explicables | Les exercices proposés dépendent des confusions observées |
| F07 | Observation humaine | Grille orale à 3 critères de 0 à 2, clairement séparée du quiz |
| F08 | Résultat anonymisé | Score global, score par cible, export JSON sans identifiant élève |
| F09 | Mode bilingue | Instructions en français et espagnol dans la démonstration HTML |
| F10 | Qualité et transparence | Tests unitaires ; limites du moteur vocal et absence de reconnaissance vocale visibles |

## 5. Architecture technique

**Frontend démonstration** : HTML/CSS/JavaScript autonome, responsive, sans librairie ni serveur de base de données. **Voix** : API Web Speech, `SpeechSynthesisUtterance` paramétrée `fr-FR`; sélection préférentielle d'une voix française disponible. **Backend réutilisable** : Python 3.11+ avec `dataclasses`, `json`, `random` et fonctions pures ; tests `pytest`. **Frontend alternatif** : Streamlit, avec boutons audio déclenchés côté navigateur dans un composant isolé. **Données** : JSON didactique de paires minimales.

## 6. Contraintes pédagogiques

Chaque mot du corpus doit être revu pour son exactitude lexicale, son API et son adéquation A1. La qualité de la voix synthétique doit être vérifiée : si les contrastes sont déformés, substituer des modèles vocaux humains autorisés. L'enseignant décide des aides et conserve l'interprétation des observations orales. Ne pas inférer un trouble de la parole, un handicap, l'origine d'un accent ni les aptitudes de l'apprenant à partir de dix réponses.

## 7. Contraintes juridiques et de confidentialité

- Aucun microphone ni transcription automatique dans cette version.
- Aucun nom, e-mail, identifiant d'élève, photo, diagnostic ou profil personnel traité.
- Export local facultatif, sans sauvegarde automatique côté serveur.
- Les voix installées par l'utilisateur ou son fournisseur système/navigateur ont leur propre fonctionnement ; le développeur ne peut pas garantir qu'elles sont entièrement hors ligne.
- Toute V2 avec enregistrement ou API vocale externe exigera un cadrage indépendant : consentement, protection des mineurs, conservation, sous-traitants, sécurité et droit de retrait.

## 8. Mesures d'acceptation technique et pilote

**Technique V1 :** tests unitaires passant ; zéro exception JavaScript constatée lors d'un essai navigateur manuel ; score reproductible à réponses identiques ; quiz de dix items et bilan exportable ; fonctionnement smartphone/ordinateur dans au moins deux navigateurs. **Pédagogique :** un enseignant valide les 11 paires et au moins 20 écoutes synthétiques avec de véritables voix françaises ; l'utilisateur comprend les consignes ; l'aidant interprète correctement la grille orale. **Pilote futur :** tests consentis avec des adultes volontaires ou dans un cadre scolaire autorisé ; documenter erreurs, appréciation de l'audio et progression sans prétendre établir un effet causal sans protocole adapté.

## 9. Hors périmètre

Reconnaissance automatique de la parole, transcription d'audio, évaluation automatique du phonème produit, détection de pathologies, comptes utilisateurs, classement d'élèves, entraînement d'un grand modèle, personnalisation par données biométriques, diagnostics sommative ou certifiante.

## 10. Livrables et avancement

| Livrable | État au lancement |
|---|---|
| Concept et cahier des charges | Rédigés |
| Moteur de discrimination et de remédiation | Développé, tests unitaires réussis |
| Corpus de 11 paires /y/–/u/ | Créé, revue enseignante nécessaire |
| Démonstration HTML bilingue | Développée, vérification sur navigateurs nécessaire |
| Prototype Streamlit | Code créé, pas de déploiement confirmé |
| Validation de la qualité de la synthèse vocale | Non réalisée |
| Publication GitHub ou mise en ligne | Non réalisée à ce stade |

## 11. Critères de réussite du projet

La V1 sera considérée comme *acceptable pour expérimentation pédagogique* après les vérifications techniques et la revue experte du corpus/du rendu vocal. Elle ne sera **pas** qualifiée d'outil mesurant la prononciation de manière automatisée tant que l'analyse de production orale n'existe pas et n'a pas été évaluée de façon indépendante.
