# BOOTO TalentScreen AI V1.1 — Revue RH structurée et responsable

**BOOTO AI & DATA INNOVATION LAB · prototype fictif · octobre 2026**

## Nouveautés V1.1 : contrôle humain par compétence et rapports

- Vérification **manuelle et explicite** de chaque critère, avec cinq états sans score, affichée dans la fiche du dossier. Aucune déduction automatique de compétence.
- **Rapport individuel imprimable** du dossier fictif, comprenant indices, états de contrôle et commentaires, sans classement.
- **Journal local non certifié** (code, action, horodatage navigateur), conservé dans JSON et exporté dans Excel.
- **Classeur Excel étendu à cinq feuilles**, dont « Contrôle humain » et « Journal local ».
- **Compatibilité avec les anciennes sauvegardes JSON V0/V1** : les états de contrôle manquants deviennent « Non examiné ». Les données restent uniquement dans la mémoire de la page.
- Contrôle supplémentaire de certains éléments personnels dans les notes saisies. Ce filtre heuristique reste insuffisant pour traiter de véritables CV.

## Nouveautés V1

- **Import DOCX sur l'appareil** : extraction du texte de `word/document.xml` dans le navigateur, sans transfert de document vers un serveur, avec limite de 3 Mo. Fonctionne sur les fichiers DOCX contenant du texte standard, pas sur les images scannées ou les documents Word complexes non textuels.
- **Consultation PDF sur l'appareil** : ouverture visuelle du PDF fictif choisi par l'utilisateur, **sans extraction du texte ni OCR**. L'utilisateur recopie manuellement les passages professionnels fictifs dans la fiche. Aucune affirmation mensongère de reconnaissance PDF.
- Lecture des fichiers **TXT/MD** en local, et contrôle heuristique d'éléments identifiants (e-mail, téléphone probable, mention de données sensibles, profils Web). Ce filtre est **incomplet** : utiliser exclusivement des documents entièrement fictifs.
- **Recherche administrative** de dossiers par code, contenu textuel ou terme et **filtre par étape**. Ces filtres ne sont ni un classement par mérite ni un score d'adéquation.
- Conservation de la matrice des indices, des questions d'entretien identiques, de la revue humaine, des exports XLSX/CSV/JSON et de l'impression.

## Essayer en ligne

La V1.1 améliore le même dossier GitHub `booto-talentscreen-ai-v1`, sans créer un troisième service Render. La V0 déployée reste [https://booto-talentscreen-ai.onrender.com/](https://booto-talentscreen-ai.onrender.com/). **La V1 est déjà hébergée sur Render** : https://booto-talentscreen-ai-v1.onrender.com/ ; elle ne remplace pas la V0. Les mises à jour de ce dossier GitHub peuvent déclencher un redéploiement automatique selon les paramètres Render.

Réglages Render : dépôt `Junior-BOOTO/python.skills`, branch `main`, **Root Directory** `booto-talentscreen-ai-v1`, **Build Command** `echo ready`, **Publish Directory** `.`.

## Accès et tests

- Site V1 / aperçu V1.1 : https://booto-talentscreen-ai-v1.onrender.com/
- Code : `Junior-BOOTO/python.skills/booto-talentscreen-ai-v1`.
- Tests : `node --test tests/*.cjs`. Pour le pilote V1.1, 21 tests Node ont été exécutés localement et un scénario navigateur simulé avec DOCX fictif, revue manuelle, rapport imprimable, 5 feuilles XLSX et restauration JSON a réussi. Le comportement du déploiement public après mise à jour doit encore être vérifié.

## Architecture

`index.html`, `src/app.js`, `src/engine.js`, `src/document-reader.js`, `src/export.js`, `src/style.css`, tests Node. Pas d'API, d'authentification, de base de données ni d'IA générative. CSP interdisant les requêtes applicatives `connect-src 'none'` et les ressources externes scriptées.

## Protection des personnes et limites

**Ne jamais charger de véritables CV ni de données identifiables de candidats dans cette démonstration publique.** Une entreprise devrait prévoir base juridique, information des candidats, contrôle d'accès, chiffrement, politique de conservation, droits d'accès et rectification, audit d'équité et revues de sécurité.

Les textes sont conservés en RAM uniquement pendant la séance et disparaissent au rechargement, sauf export volontaire. L'extraction locale DOCX n'est pas une garantie d'anonymisation. Le filtre de données personnelles est volontairement conservateur et imparfait. L'ouverture d'un PDF via `blob:` demeure sur le navigateur de l'utilisateur, sans analyse de contenu. Les fichiers peuvent contenir des contenus malveillants : **uniquement fichiers fictifs de confiance**. Les clics directs sur le site Render produisent néanmoins des journaux techniques classiques d'hébergement.

Aucune décision d'embauche, rejet, présélection, probabilité de performance ou classement automatisé. Un mot-clé repéré n'atteste pas une compétence. Les utilisateurs sélectionnent manuellement les étapes et annotations. Ne pas considérer cette V1 comme un ATS prêt pour des candidats réels.

## Tests

`node --test tests/*.test.cjs` — revue des invariants RH et contrôles de lecture documentaire. Tests navigateur sur dossier DOCX synthétique recommandés ; fonctionnement sur plusieurs navigateurs et PDF à tester manuellement.

## Limites de l’aperçu PRO

La mention PRO est une **orientation de développement** et non une certification de sécurité ou de performance RH. L’application n’a pas de serveur sécurisé, d’authentification, de droits d’accès, d’OCR ou d’extraction automatique des PDF, et ne doit recevoir **aucun CV réel, même pseudonymisé, sans audit et autorisations applicables**. Horodatage du journal local non opposable. Aucun choix d’embauche, rejet ni classement automatique.
