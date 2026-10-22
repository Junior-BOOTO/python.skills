# BOOTO Correcteur FLE AI · V1 — Assistant de rétroaction écrite A1

**Junior BOOTO Waba · BOOTO AI & DATA INNOVATION LAB**

**[🌐 Ouvrir l'application Streamlit sur Render](https://booto-correcteur-fle-ai.onrender.com/)** — Render affiche `Deploy succeeded · Live` le 22 octobre 2026, selon la capture du propriétaire. Le chargement et les exports PDF/DOCX/TXT restent à vérifier côté utilisateur. Hébergement gratuit : un temps de réveil peut être nécessaire.

[![BOOTO Correcteur FLE — tests](https://github.com/Junior-BOOTO/python.skills/actions/workflows/correcteur-fle-ai-tests.yml/badge.svg)](https://github.com/Junior-BOOTO/python.skills/actions/workflows/correcteur-fle-ai-tests.yml)


> **Prototype transparent à base de règles, pas un modèle d'IA générative ni un correcteur général du français.** Les propositions sont des pistes à valider par un enseignant ; aucune note CECRL ni mesure d'efficacité n'est revendiquée.

## Pourquoi ce projet ?

Aider les enseignants de FLE à **repérer quelques erreurs récurrentes**, expliquer les corrections et créer une fiche de retour sans stocker de copies nominatives. Les exemples concernent **Grade 4 A1 — Ma journée typique** et **Grade 5 A1 — Écoresponsabilité / droits et devoirs**.

## Fonctions V1

- Moteur Python standard library : règles explicables avec identifiants, localisation des expressions, critères « Je peux… », propositions de reformulation.
- Affichage **original → proposition → validation par l'enseignant**. On peut refuser individuellement une suggestion ; la version finale applique uniquement les suggestions approuvées.
- **PDF, Word et TXT** : fiche de rétroaction téléchargeable avec texte initial, texte révisé et observations facultatives du professeur.
- Deux thèmes et exemples **fictifs** ; jusqu'à 900 caractères.
- Interface Streamlit et **démonstration HTML autonome** (celle-ci couvre un sous-ensemble des règles Python).
- Tests automatisés sans compte, base de données ou API externe.

## Tester la démonstration

Ouvrir `demo/index.html` dans votre navigateur (autonome, sans installation). Cette démo n'analyse ni l'audio ni les images et n'envoie pas les textes à un serveur.

## Exécuter l'application Python

Depuis la racine du dossier du projet, avec Python 3.11 ou 3.12 :

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Pour exécuter les tests :

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Déploiement sur Render, service indépendant

**Attention : ne pas remplacer un service existant** (BOOTO NLP LAB, PhonoFLE, Éval'FLE AI Engine).

- Source GitHub : `Junior-BOOTO/python.skills`, branche `main`.
- New → **Web Service** ; Name : `booto-correcteur-fle-ai`.
- **Root Directory** : `correcteur-fle-ai`.
- Language : Python 3 ; Python version : `PYTHON_VERSION=3.11.11`.
- Build : `python -m pip install -r requirements.txt`.
- Start : `python -m streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`.
- Plan gratuit si proposé. Le service Render a été créé et son premier déploiement confirmé par une capture du propriétaire ; les essais fonctionnels dans le navigateur restent à terminer. Un fichier `render.yaml` propre au dossier décrit la configuration, mais le Blueprint racine du dépôt appartient à BOOTO NLP LAB et ne doit pas être remplacé.

## Confidentialité et limites

- Aucune donnée nominative nécessaire. Ne collez **jamais de productions identifiables d'élèves** dans la démo publique.
- Le code ne prévoit pas de stockage ni de requête à une API tierce. Un hébergeur peut néanmoins conserver des journaux techniques.
- Le moteur analyse uniquement des segments correspondant à **quelques règles préprogrammées** ; il peut manquer des erreurs et faire des suggestions inappropriées hors contexte.
- Les compétences CECRL (CE, CO, PE, PO) ne sont **pas** certifiées. L'enseignant est responsable de la validation des corrections et de la rétroaction.
- Aucune licence libre accordée par défaut. Un dépôt public donne accès au code mais pas automatiquement le droit de le redistribuer.

## Arborescence

- `app.py` — interface Streamlit
- `src/correcteur_fle/engine.py` — règles, analyse, choix enseignant
- `src/correcteur_fle/exports.py` — fiches Word/PDF/TXT
- `demo/index.html` — version autonome avec exemples fictifs
- `tests/test_engine.py` — tests de non-régression
- `docs/CAHIER_DES_CHARGES_V1.md` — conception, limites, prochaines étapes
- `.github/workflows/correcteur-fle-ai-tests.yml` (à la racine du dépôt) — tests et vérification du démarrage Streamlit

© 2026 Junior BOOTO Waba.
