# Fiche modèle

Auteur : Junior BOOTO Waba ; développement assisté par IA.
Usage : démonstration NLP sur SMS anglais fictifs et benchmark historique UCI.
Non validé pour : français, espagnol, courriels récents, fraude financière ou suppression automatique.

Modèle : TF-IDF unigramme + régression logistique C=1, class_weight=balanced, solver=liblinear. Vocabulaire/IDF entraînement seulement. Score non calibré indépendamment. Seuil 0,5 retenu sur validation. Pas de réglage de C ou d’autres hyperparamètres sur test.

Préparation : minuscules, URL→url, courriels→email, séries de chiffres→number, mots ASCII d’au moins deux lettres. Trois messages sans tokens écartés. Identifiants des rapports : position dans la liste retenue, pas ligne de l’archive originale.

Validation : groupes de templates et cosinus char-hashing >=0,94 créés sans labels ; split approximatif 60/20/20 par groupes. Cette contrainte n’est pas une garantie d’absence de similarité sémantique. Matrice et effectifs réels dans metrics.json.

Persistance : export JSON complet, sans pickle ; rechargement et prédictions vérifiés. JS/Python équivalents sur 5 579 cas. Le navigateur charge le modèle public puis calcule localement ; aucun texte utilisateur n’est envoyé par le code de démonstration à un service d’inférence. Les visiteurs doivent utiliser des exemples fictifs.

Droits : Almeida, T. & Hidalgo, J. (2011), SMS Spam Collection, UCI, https://doi.org/10.24432/C5CC84 . Licence CC BY 4.0 annoncée sur https://archive.ics.uci.edu/dataset/228/sms+spam+collection . Aucun SMS brut redistribué.
