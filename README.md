# Python et analyse de données · Junior BOOTO Waba
**Apprentissage documenté · Automatisation · Applications pédagogiques**

Je développe mes compétences en Python à travers des projets qui répondent à des besoins concrets : organiser des fichiers, relier des constats à des preuves et préparer des ressources FLE. J’explore aussi SQL, la visualisation et les modèles statistiques sur des données publiques ou fictives.

[Profil et CV](https://github.com/Junior-BOOTO) · [Site professionnel](https://junior-booto-fle.juniorbooto.chatgpt.site) · [Portfolio FLE](https://github.com/Junior-BOOTO/portfolio-fle) · [Catalogue complet](CATALOGUE.md)


## BOOTO ScanGrade AI V1 · Correction formative et notes trimestrielles — pilote non déployé

**[🧪 Code, guide et tests du prototype V1](booto-scangrade-ai-v1/README.md)** · [Scanner V0 déjà en ligne](https://booto-scangrade-ai.onrender.com/)

La V1 ajoute un QCM original Grade 4 FLE A1 de 12 questions, des propositions de notes et d'appréciations fondées sur les réponses, leur validation par l'enseignant, un registre T1/T2/T3 et des exports **Excel XLSX / CSV / sauvegarde JSON**. Elle sait aussi prévisualiser les ZIP du scanner V0 dans le navigateur. **Limite essentielle : pas encore de reconnaissance de l'écriture manuscrite ni d'IA générative ; les réponses QCM sont saisies par l'enseignant.** Seulement des documents fictifs. Le déploiement V1 sur Render reste à faire séparément de la V0.

## BOOTO ScanGrade AI · Scanner de copies pour tablette — V0 expérimentale

**[📷 Essayer ScanGrade AI V0 sur Render](https://booto-scangrade-ai.onrender.com/)** · [Code et guide](https://github.com/Junior-BOOTO/python.skills/tree/main/booto-scangrade-ai) · Conçu pour la **Lenovo Tab M11** : première photographie manuelle, détection expérimentale de nouvelles pages stabilisées, regroupement de copies anonymes recto/verso, export ZIP comprenant photos, inventaire CSV et manifeste JSON. **Pas encore de correction IA, de notes, de commentaires ni de synchronisation Excel ou Google Sheets.** Cinq tests automatisés validés localement ; capture réelle sur tablette et sécurité pour données scolaires à évaluer. **Ne pas utiliser de copies identifiables d'élèves dans cette V0.**

## BOOTO WORLD LEARNING BRIDGE · Éducation mondiale multilingue

**[🌍 Ouvrir la plateforme sur Render](https://booto-world-learning-bridge.onrender.com/)** · [Code et documentation](booto-world-learning-bridge/README.md) · [HTML autonome](booto-world-learning-bridge/index.html) · [Protocole de recherche](booto-world-learning-bridge/RECHERCHE_ET_VALIDATION.md)

**V1 immersive publiée sur GitHub** : une mission d’accompagnement FR/ES/EN et le **jeu Éco-Cité 3D WebGL intégré à la même page**, avec un **passeport pédagogique partagé, exportable et importable en JSON sans identité**. Deux chemins écologiques, rétroactions explicables, pas de compte ni d’API. Tests JavaScript et construction statique disponibles ; **déploiement Render V1 confirmé « Live » sur capture le 23 octobre 2026**, sans modification du site Multiverse existant. Le test des missions sur l'URL publique reste à finaliser. Ce prototype ne mesure pas une maîtrise CECRL et n'a pas été évalué en classe.

## BOOTO FLE MULTIVERSE 3D · Mission Éco-Cité francophone

**[🎮 Jouer à Éco-Cité 3D](https://booto-fle-multiverse-3d.onrender.com/)** · [Code WebGL et documentation](booto-fle-multiverse-3d/README.md) · [Démo autonome](booto-fle-multiverse-3d/DEMO_AUTONOME.html) · [Cahier des charges](booto-fle-multiverse-3d/docs/CAHIER_DES_CHARGES_V1.md)

Prototype sérieux Grade 5 / FLE A1 : quatre zones 3D, dialogues avec Amina, Éric et Nadia, deux parcours (rivière ou plantation), transformations visuelles et bilan « Je peux… ». **Rendu 3D observé sur capture utilisateur ; tests des interactions à finaliser sur son appareil.** Code publié sur GitHub ; **[site statique Render mis en ligne](https://booto-fle-multiverse-3d.onrender.com/)** (déploiement « Live » selon capture ; vérifier les parcours en ligne).


## BOOTO Demand & Stock Lab · Prévisions et stocks

[**Explorer le projet et ses résultats**](demand-stock-lab/README.md) : prévision des ventes à quatre semaines, comparaison chronologique à une référence simple et simulation du réapprovisionnement. Démonstration sur **données synthétiques**, **8 tests réussis**. Interface Streamlit vérifiée par tests automatisés ; déploiement Render en attente. [Blueprint dédié](render-demand-stock.yaml).

## Applications à essayer sur Render

| Application | Fonction | Accès direct |
| --- | --- | --- |
| BOOTO NLP LAB | Analyse de documents et de textes multilingues. | [Ouvrir l’application](https://booto-nlp-lab-zuvr.onrender.com/) |
| BOOTO Éval’FLE AI | Création d’évaluations pour l’enseignement du français. | [Ouvrir l’application](https://booto-eval-fle-ai.onrender.com/) |
| BOOTO Correcteur FLE AI | Correction et rétroaction sur les productions écrites en FLE. | [Ouvrir l’application](https://booto-correcteur-fle-ai.onrender.com/) |
| BOOTO LUDO AI | Création d’activités ludiques pour la classe de FLE. | [Ouvrir l’application](https://booto-ludo-ai.onrender.com/) |
| Superstore Dashboard | Exploration des performances commerciales avec des filtres interactifs. | [Ouvrir le tableau de bord](https://booto-superstore-dashboard.onrender.com/) |
| California Housing Lab | Simulation d’estimations immobilières par machine learning sur des données historiques. | [Ouvrir le laboratoire](https://booto-housing-lab.onrender.com/) |

Le premier chargement peut prendre quelques instants. Ces liens renvoient aux services Render ; leur présence ne constitue pas une nouvelle validation fonctionnelle. Les ressources pédagogiques restent à relire par l’enseignant et les estimations immobilières sont des démonstrations sur données historiques.

## BOOTO Correcteur FLE AI V1 · Rétroaction pédagogique écrite A1

**[Moteur Python, application Streamlit et documentation](correcteur-fle-ai/README.md)** · [Démonstration HTML](correcteur-fle-ai/demo/index.html) · [Guide de déploiement Render](correcteur-fle-ai/docs/DEPLOIEMENT_RENDER.md)

Nouveau prototype transparent de correction ciblée pour Grades 4 et 5 : **20 règles explicites**, propositions de reformulation et validation individuelle par l’enseignant. Fiches de rétroaction exportables en **PDF, DOCX et TXT**. **22 tests Python locaux réussis** ; pas de modèle génératif, pas de notation CECRL ni de validation en classe. **[Ouvrir le service Render](https://booto-correcteur-fle-ai.onrender.com/)** — statut `Live` confirmé par capture le 22 octobre 2026 ; les tests fonctionnels et téléchargements restent à vérifier.

## Éval’FLE AI Engine V1 · Évaluations scolaires FLE

**[Consulter le code et la documentation](eval-fle-ai-engine/README.md)** · [Démonstration HTML](eval-fle-ai-engine/demo/EvalFLE_Demo.html) · [Guide du nouveau service Render](eval-fle-ai-engine/docs/DEPLOIEMENT_RENDER.md)

Nouveau prototype Python/Streamlit : **60 QCM originaux de démonstration** pour Grades 4–5, avec variantes reproductibles, corrigés, grilles de réponses et exports **Word + PDF**. **19 tests locaux réussis** lors de la publication. Les contenus doivent être alignés aux programmes avant une évaluation scolaire réelle ; aucune certification CECRL ni performance pédagogique n'est revendiquée. **[Application sur Render](https://booto-eval-fle-ai.onrender.com/)** ; version déployée et affichée, corrigés améliorés à recontrôler après actualisation.

## BOOTO AI & DATA INNOVATION LAB — Page d'accueil française

**[Page d'accueil finale (HTML)](https://github.com/Junior-BOOTO/portfolio-fle/blob/main/projets/booto-ai-lab/index.html)** · [Démonstration BOOTO FLE Adaptive AI](https://github.com/Junior-BOOTO/portfolio-fle/blob/main/projets/booto-ai-lab/demos/adaptive.html) · [Démonstration PhonoFLE AI](https://github.com/Junior-BOOTO/portfolio-fle/blob/main/projets/booto-ai-lab/demos/phonofle.html).

Le laboratoire valorise BOOTO NLP LAB, BOOTO FLE Adaptive AI et PhonoFLE AI dans une présentation en français avec une identité visuelle bleu, turquoise et violet. **[Le laboratoire est accessible sur le site professionnel](https://junior-booto-fle.juniorbooto.chatgpt.site/projets/booto-ai-lab/)**, avec les deux démonstrations FLE interactives.

## PhonoFLE AI · Discrimination auditive et phonétique A1

**[PhonoFLE AI V1](phonofle-ai/README.md)** : prototype FR/ES pour distinguer /y/ (« u ») et /u/ (« ou »), avec **11 paires minimales**, quiz de 10 questions, synthèse vocale côté navigateur, conseils phonétiques et évaluation orale réservée à l'enseignant. [Démonstration HTML](phonofle-ai/demo/phonofle_ai_demo.html) · [Code Python](phonofle-ai/src/phonofle/engine.py) · [Tests](phonofle-ai/tests/test_engine.py). **Ne reconnaît pas la voix ni ne note automatiquement la prononciation. [Essayer la démonstration en ligne](https://junior-booto-fle.juniorbooto.chatgpt.site/projets/booto-ai-lab/demos/phonofle.html).**

## BOOTO FLE Adaptive AI · Différenciation pédagogique A1

**[BOOTO FLE Adaptive AI V1](booto-fle-adaptive-ai/README.md)** relie un quiz formatif de 12 QCM sur « Ma journée typique » à des recommandations d'activités transparentes : vocabulaire, verbes pronominaux, connecteurs temporels et heures. [Démonstration HTML autonome](booto-fle-adaptive-ai/demo/BOOTO_FLE_Adaptive_AI_Demo.html) · [Moteur Python et tests](booto-fle-adaptive-ai/src/booto_fle/engine.py) · [Documentation éthique](booto-fle-adaptive-ai/docs/ETHIQUE_ET_VALIDATION.md). Les 12 profils sont **synthétiques** ; il s'agit d'un moteur à règles, **sans apprentissage automatique ni validation CECRL**.

## Nouveau laboratoire NLP · Prototype multilingue

**[BOOTO NLP LAB V1 — Multilingual Text Analyzer](booto-nlp-lab/README.md)** : import de CSV, détection des langues (français, anglais, espagnol), classification thématique, mots-clés TF-IDF, similarité de documents et export. Application Python et interface Streamlit, avec un corpus **entièrement synthétique** de 300 textes ; performances externes encore à valider. [Guide de déploiement](booto-nlp-lab/docs/DEPLOIEMENT_STREAMLIT.md). **[Ouvrir l’application déployée sur Render](https://booto-nlp-lab-zuvr.onrender.com/).**

## Trois projets phares · Démonstrations et preuves

| Projet | Essayer | Résultat à examiner | Code et reproduction |
|---|---|---|---|
| FLE Resource Studio | [Studio](https://junior-booto-fle.juniorbooto.chatgpt.site/fle-resource-studio.html) | 45 combinaisons vérifiées ; ressources à relire. | [Parcours guidé](fle-resource-studio/README.md#découvrir-le-projet-en-trois-minutes) |
| Portfolio File Guardian | [Rapport synthétique](https://junior-booto-fle.juniorbooto.chatgpt.site/guardian-reports/report.html) | 8 fichiers, 1 groupe de doublons ; originaux conservés. | [Parcours guidé](portfolio-file-guardian/README.md#découvrir-le-projet-en-trois-minutes) |
| AfriFlow Explain | [Démonstration](https://junior-booto-fle.juniorbooto.chatgpt.site/afriflow-explain.html) | 19 scénarios repérés contre 3 à budget égal ; 17 faux positifs. Données synthétiques. | [Parcours guidé](afriflow-explain/README.md#découvrir-le-projet-en-trois-minutes) |

Résultats issus des rapports datés des projets ; aucune nouvelle exécution des modèles ou tests revendiquée ici.


## CV Python & Data · Français · English · Español

[Consulter mes trois CV](cv/README.md) : versions harmonisées de trois pages, avec quatre projets personnels et les liens de certification.

## Certificats SoloLearn en IA et données

J’ai ajouté les [13 certificats et leurs justificatifs](certifications/sololearn/README.md), classés selon leur pertinence pour les données et l’IA. La [galerie du portfolio](https://junior-booto-fle.juniorbooto.chatgpt.site/certificats-ia.html) est disponible en français, anglais et espagnol.

## Quatre projets pour commencer

| Projet | Ce qu’il permet d’examiner | Limite principale |
| --- | --- | --- |
| [FLE Resource Studio](fle-resource-studio/README.md) | Conception de fiches différenciées, catalogue FR/ES/EN, exports et API locale. | Ressources à relire et expérimenter ; lecture vocale dépendante du navigateur. |
| [Portfolio File Guardian](portfolio-file-guardian/README.md) | Inventaire SHA-256, simulation, copie et restauration journalisée. | Prototype local ; pas de suppression automatique des doublons. |
| [Portfolio Evidence Hub](portfolio-evidence-hub/README.md) | Audit documenté, preuves datées et tableau de bord. | Instantané historique, sans certification de qualité du code. |
| [FLE Learning Analytics](fle-learning-analytics/README.md) | Génération et analyse de données d’évaluation fictives. | Aucun effet réel sur les apprentissages mesuré. |

Les README de ces projets donnent les commandes, les preuves disponibles et les limites. Les résultats de tests documentés correspondent à leurs environnements et dates de validation ; cette page ne revendique pas une nouvelle exécution.

## Explorer par domaine

| Domaine | Parcours |
| --- | --- |
| FLE et outils pédagogiques | [fle-resource-studio](fle-resource-studio/) · [fle-learning-analytics](fle-learning-analytics/) |
| Automatisation et qualité des ressources | [portfolio-file-guardian](portfolio-file-guardian/) · [portfolio-evidence-hub](portfolio-evidence-hub/) · [sourcewatch](sourcewatch/) · [document-to-data-lab](document-to-data-lab/) |
| Analyse et visualisation | [superstore-bivariate](superstore-bivariate/) · [global-superstore-dashboard](global-superstore-dashboard/) · [wine-quality-acp](wine-quality-acp/) · [chinook-sql](chinook-sql/) · [adventureworks-sql](adventureworks-sql/) · [employee-performance-analysis](employee-performance-analysis/) |
| Modèles et séries temporelles | [messagelens](messagelens/) · [bitcoin-datalab](bitcoin-datalab/) · [api-open-meteo](api-open-meteo/) · [sales-time-series](sales-time-series/) · [credit-default-classification](credit-default-classification/) · [california-housing-regression](california-housing-regression/) · [mall-customer-clustering](mall-customer-clustering/) · [bike-demand](bike-demand/) |
| Transferts et simulations | [afriflow-explain](afriflow-explain/) · [transfer-cost-observatory](transfer-cost-observatory/) |

[Consulter les descriptions, résultats et limites de tous les projets](CATALOGUE.md).

## Carnets d’apprentissage

[Bases de Python](Exercices_de_python_les_bases.ipynb) · [Pandas](Pandas.ipynb) · [Scikit-learn](sklearn.ipynb)

Ces carnets retracent ma progression ; leurs environnements et données nécessaires restent à préciser. Les projets documentés ne constituent pas une expérience industrielle revendiquée.

## Ressources et méthode

- [Assistants IA pour les données](assistants-ia/README.md) : rôles et limites de coordination ; pas de connexion automatique annoncée entre GPT indépendants.
- [Formations Python, données et IA](certifications-python-data.md) · [Bibliothèque de références](bibliotheque/README.md).
- [Modèle de README](templates/README-PYTHON.md) · [Reproduction du démonstrateur FLE](fle-learning-analytics/README.md).

Les jeux synthétiques sont signalés comme tels ; les données RH originales absentes ne donnent lieu à aucun résultat revendiqué. Les données d’élèves et les documents confidentiels restent exclus des ressources publiques.

## Badges Google · IA générative et Gemini

[Consulter les 12 badges Google, leurs visuels et les liens officiels](certifications/google/README.md).
