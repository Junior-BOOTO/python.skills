# BOOTO ScanGrade AI — V1 de correction formative et de suivi trimestriel

**Auteur : Junior BOOTO Waba · BOOTO AI & DATA INNOVATION LAB · 23 octobre 2026**

## Statut véridique

**Prototype FLE A1 reposant sur un corrigé prédéfini et la validation humaine, sans OCR manuscrit et sans modèle d'IA générative.** Le nom de la marque contient « AI » ; la V1 présentée ne doit pas être décrite comme capable de lire ou corriger automatiquement des copies manuscrites photographiées.

V1 réalisée **dans un dossier indépendant** `booto-scangrade-ai-v1` pour ne pas remplacer la V0 numérisation déjà en ligne `https://booto-scangrade-ai.onrender.com/`. Déploiement V1 non encore effectué tant que les essais sur tablette ne sont pas terminés.

## Fonctionnalités vérifiables

1. Ouvrir dans le navigateur l'archive ZIP exportée par ScanGrade V0 (fichiers ZIP non compressés, avec CRC, manifest V0, photos JPG) ; prévisualiser les pages **localement**, sans stockage ni transfert réseau de ces photographies par le code de la démo.
2. Exercice de démonstration original **Grade 4 · FLE A1 · Ma journée typique** : 12 QCM à correction déterministe et quatre rubriques : vocabulaire, présent, heure et moments, organisation.
3. Saisie manuelle des réponses A/B/C/D à partir de la copie (ou bouton « Exemple fictif »). **Pas de lecture automatique de l'écriture** dans cette version.
4. Proposition de note calculée à partir des 12 items, barème configurable : 7, 10, 20 ou 100. Commentaire de forces, difficultés et recommandations uniquement fondé sur le questionnaire. L'enseignant édite la note et l'appréciation et indique une justification si la note diffère de la proposition.
5. Enregistrement local après **validation explicite** par l'enseignant, sous identifiants anonymes `C001`, etc. Suivi `T1`, `T2`, `T3` ; révision d'une note déjà validée sans créer un doublon pour la même activité et le même trimestre.
6. Export XLSX **réel** : deux onglets `Evaluations`, `Synthese` ; possibilité d'import manuel du `.xlsx` dans Google Sheets. Export CSV et sauvegarde/restauration JSON du registre.
7. Aucun nom d'étudiant, compte, API externe, clé payante ou serveur de données élèves dans ce prototype. Un stockage **localStorage** des notes anonymes est conservé entre les sessions tant que le navigateur ne l'efface pas. Les images du ZIP restent seulement en mémoire pendant la session.

## Tests et lancement

```bash
node --test tests/*.test.cjs
python -m http.server 8000
# Ouvrir http://localhost:8000 depuis cet ordinateur.
```

Ou héberger ce répertoire sur Render comme **nouveau Static Site** :

- Repository `Junior-BOOTO/python.skills`, branch `main`
- Root Directory `booto-scangrade-ai-v1`
- Build Command `echo ready`
- Publish Directory `.`
- Aucun environnement secret requis.

## Sécurité et limites

- **Données fictives exclusivement** jusqu'à mise en place de sécurité, habilitations, contrats et autorisations appropriés pour toute donnée d'élève mineur. Le stockage local du navigateur n'est pas un stockage institutionnel sécurisé.
- La vérification des corrections, du barème, des commentaires et de l'identification des pages relève de l'enseignant ; les résultats QCM ne démontrent pas l'expression orale ou écrite libre ni une maîtrise CECRL.
- Les quatre catégories portent sur douze items de démonstration et ne représentent pas un programme annuel officiel.
- Le scanner V0 reste une application distincte : il exporte le ZIP. La V1 importe ce ZIP pour consultation, mais ne corrige pas les photographies par OCR.
- Seul un exercice est couvert pour l'instant ; les règles d'évaluation ne peuvent pas encore être changées depuis l'interface.
- Pas de synchronisation API Google Sheets : utilisez l'import manuel du `.xlsx` généré.
- La « Moyenne disponible » calcule la moyenne simple des trimestres renseignés, après conversion sur 20, sans pondération particulière.
- La validation réelle sur la Lenovo Tab M11 et le fonctionnement de tous les téléchargements ne sont pas encore confirmés.

## Évolutions possibles après validation

Intégrer, avec consentements et environnement sécurisé, un OCR manuscrit ayant un score de confiance et une revue humaine, un constructeur de barèmes par classe/trimestre, la synchronisation Google Sheets via OAuth, et des rapports PDF individuels.
