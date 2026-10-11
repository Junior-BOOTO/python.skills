# Journal des transformations

1. Lecture des deux CSV avec séparateur `;`, préservation de `raw/`.
2. Vérification des 11 colonnes chimiques et de `quality` ; conversion effectuée par le lecteur CSV, sans changement des valeurs.
3. Ajout de `color` et `source_row`, puis concaténation : 1 599 + 4 898 = 6 497 lignes.
4. Aucun champ absent, aucune valeur non finie. Pas d’imputation, pas de retrait d’observation extrême.
5. Marquage conceptuel des 1 177 profils répétés ; conservation dans l’analyse principale et comparaison avec les 5 320 profils uniques.
6. Pour l’ACP descriptive seulement, ajustement de StandardScaler sur les 11 variables de toutes les observations. Ce prétraitement ne doit pas être repris tel quel dans une future évaluation prédictive.
