# HR Analytics: Employee Performance Distribution and Outlier Detection

Projet d'analyse exploratoire des performances des employés avec Python, pandas, seaborn et matplotlib. Il reprend le scénario détaillé dans le travail de portfolio de mars 2026 : statistiques descriptives, distributions, comparaison par département et heures supplémentaires, corrélations et détection des valeurs atypiques par la règle IQR (1,5 × intervalle interquartile).

## Statut des données

Le fichier original `HR_Analytics.csv` et ses résultats n'étaient pas disponibles dans les ressources accessibles lors de cette publication. **Aucun chiffre, graphique d'entreprise ni résultat d'employé n'est présenté comme observé.** Le script et le notebook sont prêts à fonctionner avec un CSV que vous êtes autorisé à utiliser. Les données RH réelles ne doivent pas être publiées sans autorisation et anonymisation adaptées.

## Structure

- `scripts/analysis.py` : chargement, nettoyage léger, tableaux et graphiques.
- `notebooks/01_employee_performance_analysis.ipynb` : parcours interactif de l'analyse.
- `data/` : emplacement local du CSV, ignoré par Git.
- `outputs/` : figures et tableaux générés localement, ignorés par Git.

## Reproduire l'analyse

```bash
python -m pip install -r employee-performance-analysis/requirements.txt
python employee-performance-analysis/scripts/analysis.py --input /chemin/vers/HR_Analytics.csv
```

Depuis la racine du dépôt, les résultats sont écrits dans `employee-performance-analysis/outputs/`. Pour le notebook, ouvrez `notebooks/01_employee_performance_analysis.ipynb` et adaptez la cellule indiquant le chemin du CSV.

La seule colonne obligatoire est `PerformanceScore` (alias `PerformanceRating` ou `Performance Score`). `HoursWorked`, `Department` et `OverTime` sont facultatives ; les analyses correspondantes sont omises si elles manquent. Les valeurs non numériques des colonnes quantitatives deviennent manquantes. Un jeu de données portant le nom « HR Analytics » peut avoir un schéma différent : inspectez ses colonnes avant d'interpréter les sorties.

## Méthode et limites

L'algorithme IQR marque les valeurs sous Q1 − 1,5 × IQR ou au-dessus de Q3 + 1,5 × IQR. Une valeur atypique n'est pas une erreur ni une preuve de mauvaise performance. Les corrélations sont descriptives, sans lien de causalité. Le contexte, les échelles, les données manquantes et les petits groupes doivent être examinés avant toute conclusion RH.

**Provenance :** reconstitution exécutable du projet conçu dans les échanges de mars 2026. Le CSV, les résultats et l'éventuel notebook original n'ont pas été récupérés ; ce dépôt ne prétend pas les reproduire à l'identique.
