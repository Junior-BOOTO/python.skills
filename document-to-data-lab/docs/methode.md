# Méthode et dictionnaire

Utilisateur : analyste ou association préparant des dépenses pour analyse. Objectif : consolider des lignes compatibles sans masquer les erreurs.

Acceptation : originaux inchangés ; sommes exactes Decimal et séparées par devise ; repères source conservés ; anomalies contrôlées retrouvées ; résultat rechargeables depuis JSON/CSV.

| Colonne | Définition |
|---|---|
| id | Identifiant de dépense, unique supposé dans le lot |
| date | Date ISO, validée au calendrier |
| description | Libellé source, espaces externes retirés |
| amount | Montant non négatif, décimal exact |
| currency | USD ou COP |
| source_file / source_sha256 | Nom du fichier et empreinte de ses octets |
| source_page / source_table / source_row | Page PDF (null pour CSV), tableau, ligne incluant l’en-tête |
| raw | Valeurs avant normalisation dans rows.json |
| status / issues | Décision de ligne et motifs de révision |

Conserver la source et le rapport pour examiner les décisions. Aucune correction automatique des dates ou montants douteux. Les doublons exacts et contradictoires sont distingués ; toutes leurs occurrences sont à revoir. Une erreur de document bloque son extraction, pas celle des autres documents.

Validation de démonstration : cinq lignes PDF comparées à une référence manuelle (25 cellules). Ce petit échantillon ne mesure pas une performance de production. Tests : formats monétaires, dates, devise, identifiant, CSV formula, échappement HTML, conflits, sommes multidevises, source immuable, isolation des erreurs, provenance, sortie existante, largeur de ligne et jeu PDF.
