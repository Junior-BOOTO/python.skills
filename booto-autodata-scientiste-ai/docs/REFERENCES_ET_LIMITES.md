# Fondements bibliographiques et limites

Conception inspirée par **les thèmes** des huit ouvrages transmis par l'auteur du projet, sans copie de code ni reproduction du texte, des chapitres ou des PDF.

- *Building ETL Pipelines with Python* — ingestion, validation, nettoyage, tests et fiabilité des workflows.
- *Essentials of Python for Artificial Intelligence and Machine Learning* — manipulation Pandas, EDA, écosystème scikit-learn.
- *Machine Learning with Python* — fondamentaux et comparaison de modèles supervisés ; référence simple.
- *The Art of Feature Engineering* — imputation, encodage, variables dérivées et contrôle de la fuite.
- *Mastering MLOps Architecture: From Code to Deployment* — conception MLOps, versionnement, monitoring et déploiement ultérieur.
- *AI and ML Techniques in Engineering and Management* — principes et métriques appliquées.
- *Machine Learning and Data Science: Fundamentals and Applications* — diversité des cas d'usage et limites de généralisation.
- *TensorFlow 2.0 Computer Vision Cookbook* — futur module vision, **absent de V1**.

## Limites concrètes V1
- Pas d'appel API, de scraping ou de RAG sur les livres ; pas de traitement d'images.
- Modèles supervisés tabulaires uniquement. Pas de gestion spécifique des séries temporelles, de régression causale ni d'inférence métier.
- Comparaison sur validation croisée train, puis évaluation sur un test réservé ; scores non validés en production.
- Vérification manuelle nécessaire pour identifiants et variables de fuite ; absence de détection automatique garantie.
- Aucun stockage volontaire de données utilisateur, aucune authentification, et aucune garantie de protection contre les journaux d'un hébergeur tiers.
- Aucun réentraînement automatique ou API de prédiction publique.
- La bonne reproductibilité exige le **même fichier source**, les versions des packages et la graine ; les sorties numériques peuvent varier entre plateformes.
