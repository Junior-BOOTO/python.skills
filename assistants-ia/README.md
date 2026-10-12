# Mes assistants IA · Python et science des données

**Junior BOOTO Waba · Apprentissage documenté et conception d’assistants spécialisés**

Cinq assistants pour concevoir des projets Python et organiser un parcours de données. Les trois assistants spécialisés peuvent être utilisés séparément ; DataLab Coordinateur applique les rôles de collecte, analyse et modélisation dans une même session. Il ne contacte pas automatiquement les trois GPT indépendants.

| Assistant | Mission | Livrables attendus | Accès |
| --- | --- | --- | --- |
| Python Project Studio | Concevoir, réaliser, tester et documenter des projets Python destinés au portfolio. | Code, tests, README, manifeste et démonstration vérifiable selon le projet. | [Ouvrir dans ChatGPT](https://chatgpt.com/plugins/plugin_a1fd10f0a7288191960abcbcc94ddc2f) |
| DataLab Coordinateur | Enchaîner collecte, analyse et machine learning dans une même session, avec fichiers partagés. | Dossier raw/collected/analysis/models/reports, manifeste et résultats vérifiés selon les outils disponibles. | [Ouvrir dans ChatGPT](https://chatgpt.com/plugins/plugins_6acc1a3105588191a32cb56660adede3) |
| DataCollect | Collecter, extraire et structurer les données ; vérifier provenance et qualité. | CSV/Excel, dictionnaire des variables, sources, rapport qualité et code de collecte si pertinent. | [Ouvrir dans ChatGPT](https://chatgpt.com/plugins/plugin_051bd96a84d48191a91007bb136e1ac6) |
| DataAnalyse | Nettoyer avec traçabilité, explorer, calculer des statistiques et visualiser. | Données préparées, rapport, graphiques, journal de nettoyage et code Python. | [Ouvrir dans ChatGPT](https://chatgpt.com/plugins/plugin_5644d9a5e96481918687859749a3c4b3) |
| DataML | Définir une cible, prévenir les fuites, entraîner et comparer des modèles. | Protocole de validation, référence simple, scores calculés, code et modèle exporté si l’exécution a réussi. | [Ouvrir dans ChatGPT](https://chatgpt.com/plugins/plugin_6fa27fa0a8008191ad0368e37384da58) |

## Utilisation
1. Fournir les sources à DataCollect et récupérer les données documentées.
2. Transmettre les fichiers et le dictionnaire à DataAnalyse.
3. Fournir le dossier d’analyse à DataML avec un objectif de prédiction précis.

Pour les trois assistants indépendants, la transmission est manuelle. Avec DataLab Coordinateur, les fichiers intermédiaires sont réutilisés dans la même session ; aucune exécution permanente entre sessions n’est garantie. Les connexions API dépendent des outils configurés ; aucun accès automatique aux bases de données n’est garanti.

Chaque assistant propose un mode **Apprentissage**, avec explications progressives, et un mode **Réalisation**, avec code et livrables vérifiables.

## Commencer un projet

- **Python Project Studio** : « Réalise un projet Python avec jeu de démonstration, tests et documentation pour mon portfolio. »
- **DataLab Coordinateur** : « À partir de mon CSV, coordonne la collecte, l’analyse et une modélisation pertinente, avec manifeste et résultats vérifiables. »

Python Project Studio : version 0.3.0. DataLab Coordinateur : version 0.1.0. Métadonnées consultées le 12 octobre 2026 ; ces versions ne constituent pas une preuve de résultats exécutés.

## Principes de conception
- Préserver les sources et documenter les transformations.
- Distinguer observations, hypothèses et résultats réellement exécutés.
- Séparer entraînement, validation et test ; apprendre les prétraitements uniquement sur l’entraînement.
- Comparer les modèles à une référence simple et exposer leurs limites.
- Utiliser des données fictives ou anonymisées pour les démonstrations publiques.

## Statut et accès
Assistants créés et documentés. Les fiches de ce portfolio sont publiques ; l’utilisation des assistants dépend du compte et des droits de partage ChatGPT. Les intégrations consultées sont actuellement privées. Aucun accès public universel n’est garanti.

Les prochaines étapes sont de tester la chaîne sur un jeu de données de démonstration et de publier les résultats après exécution vérifiée.

[Retour au portfolio Python](../README.md) · [Mon site professionnel](https://junior-booto-fle.juniorbooto.chatgpt.site/#python)
