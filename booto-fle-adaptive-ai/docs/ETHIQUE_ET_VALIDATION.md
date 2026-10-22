# Validation, éthique et limites

## Une démonstration n'est pas une preuve d'efficacité

La logique V1 démontre qu'on peut lier des résultats de questionnaire à des activités ciblées. Elle ne démontre ni gain d'apprentissage, ni justesse psychométrique, ni conformité complète au CECRL. Les seuils 0/1/2 sur trois questions sont **des choix de prototype**. Les douze profils synthétiques ne constituent pas un jeu d'évaluation réelle.

## Critères de validation avant usage avec des élèves

1. **Revue disciplinaire** : un enseignant relit toutes les questions, les distracteurs, la progressivité A1 et les corrections.
2. **Accessibilité** : tester contraste, lisibilité, compréhension et alternatives à la lecture sans imposer un outil numérique unique.
3. **Équité** : des choix de QCM ne suffisent pas à mesurer l'expression orale, les besoins d'apprentissage ou l'ensemble des compétences du CECRL.
4. **Données** : obtenir les autorisations institutionnelles et parentales appropriées avant toute collecte de données d'enfants ; minimiser l'identifiabilité, définir conservation et suppression.
5. **Pilotage prudent** : tester avec des scénarios anonymes et une observation d'enseignant, sans décisions automatiques affectant les notes ou le parcours d'un élève.
6. **Impact pédagogique** : définir ensuite une mesure prétest/post-test, un contexte, un temps d'exposition et des limites méthodologiques.

## Traitement des données

L'interface affiche des profils entièrement synthétiques. Les réponses du quiz sont calculées en mémoire lors de la session ; aucun enregistrement, authentification ou envoi à un service externe n'est implémenté dans le code. Cela ne garantit pas l'absence de collecte par un hébergeur tiers ou des équipements intermédiaires. **Ne pas utiliser le prototype public avec des réponses d'élèves réels.**

## Validation technique

La suite pytest comprend la validation des questions, plusieurs scénarios de réussite/échec, la gestion des données absentes, les recommandations, les profils synthétiques et la sécurité des schémas. Le test d'exécution Python du moteur doit être exécuté dans l'environnement cible. Le test visuel et le test interactif Streamlit sont un contrôle distinct, à réaliser lors du déploiement.

## Feuille de route des versions

**V1** : quiz textuel + recommandation transparente + classe synthétique. **V1.1** : six associations visuelles vérifiables et amélioration de l'accessibilité. **V2** : élargissement du catalogue, évaluation pédagogique indépendante et mécanismes de paramétrage par l'enseignant. **V3 éventuelle** : exploration de méthodes de NLP/ML sur données licites et avec évaluation d'équité ; aucune promesse d'IA autonome.

## Vérification du prototype initial (21 octobre 2026)

- **19 tests Python sur 19 réussis**, exécution locale avec pytest.
- **Script console** lancé : agrégation des 12 profils fictifs et recommandations calculées.
- **Syntaxe Python** vérifiée avec `compileall`.
- **Démonstration HTML** : syntaxe du script vérifiée avec Node.js et validité du JSON embarqué (12 questions, 12 profils).
- **Contrôles non effectués :** lancement réel de Streamlit (dépendance non disponible dans l'environnement d'exécution) et test interactif visuel du navigateur. Aucun service public déployé.

Pour valider l'interface en V1.1 : `pip install -r requirements.txt` puis `streamlit run app/main.py`, scénarios manuel et enseignant, contrôle de l'affichage sur PC et mobile, et contrôle de l'absence de données transmises.
