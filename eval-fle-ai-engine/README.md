# BOOTO Éval’FLE AI Engine — V1

**Laboratoire BOOTO AI & DATA INNOVATION LAB** · **Auteur : Junior BOOTO Waba** · **Statut : prototype pédagogique à valider**

Générateur d'évaluations imprimables pour l'enseignement du français langue étrangère, Grade 4 et Grade 5, avec **30 QCM par classe**, corrigés détaillés, grilles de réponses, indicateurs « Je peux… » et exports Word et PDF. Versions abrégées de 12 et 15 questions disponibles.

## Fonctions effectivement développées

- Banque éditoriale de **60 items originaux** au total, répartie par grade et thème ; **données de démonstration**, pas programme annuel officiel.
- Variantes reproductibles : questions et options mélangées, réponses recalculées automatiquement.
- Interface **Streamlit**, couleur bleu/turquoise/violet, aperçu des questions, critères pédagogiques et vérification anonyme des réponses.
- Sujet apprenant + corrigé enseignant en **PDF et DOCX** (quatre exports par variante).
- Aucune donnée nominative requise, aucune API externe.

## Démarrage rapide

Sous Python 3.11 ou 3.12 :

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Puis ouvrir l'adresse locale affichée par Streamlit.

Pour vérifier le moteur et les exports :

```bash
python -m pip install pytest
python -m pytest -q
```

## Déploiement Render (Web Service)

1. Choisir **New → Web Service** et connecter le dépôt `Junior-BOOTO/python.skills`.
2. Sélectionner la branche `main`, le **Root Directory** `eval-fle-ai-engine`.
3. Indiquer **Build Command** : `pip install -r requirements.txt`.
4. Indiquer **Start Command** : `python -m streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`.
5. Sélectionner un plan autorisé pour votre compte (gratuit si proposé), puis lancer le déploiement.

**Ne pas réutiliser ni renommer vos services Render BOOTO NLP LAB existants.** Créer un **nouveau service** et vérifier sa propre URL. Le dépôt racine dispose déjà d'un `render.yaml` pour un autre projet, ne pas le modifier.

### Structure

```text
app.py                       Interface Streamlit
src/evalfle/engine.py        Banque, mélange et correction
src/evalfle/exports.py       Génération Word et PDF
data/banque_demo_a1.json     60 questions originales de démonstration
tests/test_engine.py         Tests de génération/correction/exports
docs/CONCEPTION_ET_LIMITES.md
requirements.txt
.streamlit/config.toml
```

## Protocole avant utilisation réelle

Lire [Conception et limites](docs/CONCEPTION_ET_LIMITES.md). Les thèmes sont **illustratifs** et ne prétendent pas reproduire vos trois périodes annuelles ; revoir les contenus avec les programmes scolaires avant une évaluation sommative. Les QCM mesurent principalement la reconnaissance linguistique, pas directement les quatre compétences CECRL. Aucune efficacité ni fiabilité en classe n'est revendiquée.

© 2026 Junior BOOTO Waba. Le code est visible publiquement une fois publié sur GitHub, mais aucune licence de réutilisation n'est accordée par défaut.
