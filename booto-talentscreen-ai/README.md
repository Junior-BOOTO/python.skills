# BOOTO TalentScreen AI — Talent Intelligence Workspace (Prototype V0)

**BOOTO AI & DATA INNOVATION LAB · Junior BOOTO Waba · 23 octobre 2026**

## Pourquoi cette application ?

Premier projet hors éducation : une démo visuelle de gestion du recrutement, avec **trois dossiers entièrement fictifs**. L’application permet de concevoir un poste, configurer jusqu’à 15 compétences professionnelles, retrouver des **indices textuels littéraux** dans les exemples, préparer des questions d'entretien communes, annoter chaque dossier, suivre un pipeline *uniquement par action humaine*, et exporter un tableau **XLSX (3 onglets), CSV ou JSON**. Présentation adaptée à un ordinateur et une tablette.

**Important — exactitude technique :** cette V0 **n'utilise ni IA générative ni apprentissage automatique**. Elle ne lit pas automatiquement les PDF/DOCX et n'effectue **aucun score, classement, sélection ou rejet automatique** de candidats. Le nom « TalentScreen AI » décrit la ligne de produits envisagée, pas une capacité d'évaluation automatique de cette V0. Une simple occurrence de mot-clé ne prouve aucune compétence.

## Accès et technologie

Site statique sans serveur ni API. Lancer `python -m http.server 8000` à la racine du dossier puis ouvrir `http://localhost:8000`. Pour héberger sur Render **Static Site** : dépôt `Junior-BOOTO/python.skills`, racine `booto-talentscreen-ai`, Build `echo ready`, Publish `.`. Aucune clé API.

Fichiers : `index.html`, `src/style.css`, `src/engine.js`, `src/export.js`, `src/app.js`, `tests/engine.test.cjs`. Tests : `node --test tests/*.test.cjs`.

## Sécurité et limites

- Exemples fictifs exclusivement ; aucune autorisation d'importer de véritables CV ou des données nominatives dans une démonstration publique.
- Les textes d'exemple, notes et critères personnalisés sont conservés dans **la mémoire de la page** (aucun localStorage ni serveur), perdus au rechargement. Export explicite possible au format JSON/XLSX/CSV.
- Politique CSP bloquant les appels réseau depuis les scripts (`connect-src 'none'`). Dépendances 100 % locales. En revanche, le chargement de la page sur Render donne naturellement lieu à des journaux techniques d'hébergement.
- Aucun genre, âge, origine, santé ou autre caractéristique sensible ne doit être collecté ou utilisé comme critère ; une liste partielle de termes explicites est bloquée, **mais ce filtre n'est pas une garantie exhaustive**. Ne saisir que des descriptions professionnelles pertinentes et fictives.
- Pas de connexion ATS, de comptes, de journal d'audit institutionnel, de suppression de données candidates ou d'analyse d'impact. Les rapports sont des supports organisationnels pour revue humaine, et non des recommandations d'embauche.
- Un usage commercial réel nécessitera une analyse juridique et technique locale (par exemple loi colombienne 1581/2012, cadre UE AI Act en cas de déploiement concerné), contrôles d'équité, accès autorisés, chiffrement, consentement, rétention et droits des personnes.

## Prochaine étape

Entretiens utilisateurs auprès de RH, tests d’utilité et de compréhension, recherche de différenciation par les preuves projet, PDF/DOCX traités de manière appropriée, authentification, journalisation et conformité. **Éviter les scores de compatibilité non validés** et toute décision automatique sur l’accès à l’emploi.
