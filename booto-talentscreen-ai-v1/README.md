# BOOTO TalentScreen AI V1 — Atelier RH documentaire responsable

**BOOTO AI & DATA INNOVATION LAB · prototype fictif · octobre 2026**

## Nouveautés V1

- **Import DOCX sur l'appareil** : extraction du texte de `word/document.xml` dans le navigateur, sans transfert de document vers un serveur, avec limite de 3 Mo. Fonctionne sur les fichiers DOCX contenant du texte standard, pas sur les images scannées ou les documents Word complexes non textuels.
- **Consultation PDF sur l'appareil** : ouverture visuelle du PDF fictif choisi par l'utilisateur, **sans extraction du texte ni OCR**. L'utilisateur recopie manuellement les passages professionnels fictifs dans la fiche. Aucune affirmation mensongère de reconnaissance PDF.
- Lecture des fichiers **TXT/MD** en local, et contrôle heuristique d'éléments identifiants (e-mail, téléphone probable, mention de données sensibles, profils Web). Ce filtre est **incomplet** : utiliser exclusivement des documents entièrement fictifs.
- **Recherche administrative** de dossiers par code, contenu textuel ou terme et **filtre par étape**. Ces filtres ne sont ni un classement par mérite ni un score d'adéquation.
- Conservation de la matrice des indices, des questions d'entretien identiques, de la revue humaine, des exports XLSX/CSV/JSON et de l'impression.

## Essayer en ligne

**[🌐 Ouvrir la V1 sur Render](https://booto-talentscreen-ai-v1.onrender.com/)** · [V0 sur Render](https://booto-talentscreen-ai.onrender.com/). Le premier déploiement V1 a été confirmé « Deploy succeeded · Live » sur une capture du 23 octobre 2026 à 19 h 11 (Bogotá). Le chargement de la page et ses fonctions restent à tester sur le navigateur de l'utilisateur. La V1 ne remplace pas la V0.

Réglages Render : dépôt `Junior-BOOTO/python.skills`, branch `main`, **Root Directory** `booto-talentscreen-ai-v1`, **Build Command** `echo ready`, **Publish Directory** `.`.

## Architecture

`index.html`, `src/app.js`, `src/engine.js`, `src/document-reader.js`, `src/export.js`, `src/style.css`, tests Node. Pas d'API, d'authentification, de base de données ni d'IA générative. CSP interdisant les requêtes applicatives `connect-src 'none'` et les ressources externes scriptées.

## Protection des personnes et limites

**Ne jamais charger de véritables CV ni de données identifiables de candidats dans cette démonstration publique.** Une entreprise devrait prévoir base juridique, information des candidats, contrôle d'accès, chiffrement, politique de conservation, droits d'accès et rectification, audit d'équité et revues de sécurité.

Les textes sont conservés en RAM uniquement pendant la séance et disparaissent au rechargement, sauf export volontaire. L'extraction locale DOCX n'est pas une garantie d'anonymisation. Le filtre de données personnelles est volontairement conservateur et imparfait. L'ouverture d'un PDF via `blob:` demeure sur le navigateur de l'utilisateur, sans analyse de contenu. Les fichiers peuvent contenir des contenus malveillants : **uniquement fichiers fictifs de confiance**. Les clics directs sur le site Render produisent néanmoins des journaux techniques classiques d'hébergement.

Aucune décision d'embauche, rejet, présélection, probabilité de performance ou classement automatisé. Un mot-clé repéré n'atteste pas une compétence. Les utilisateurs sélectionnent manuellement les étapes et annotations. Ne pas considérer cette V1 comme un ATS prêt pour des candidats réels.

## Tests

`node --test tests/*.test.cjs` — revue des invariants RH et contrôles de lecture documentaire. Tests navigateur sur dossier DOCX synthétique recommandés ; fonctionnement sur plusieurs navigateurs et PDF à tester manuellement.
