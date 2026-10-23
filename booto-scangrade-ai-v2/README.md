# BOOTO ScanGrade AI — V2 pilote unifié

**Auteur : Junior BOOTO Waba · BOOTO AI & DATA INNOVATION LAB · 23 octobre 2026**

**[📱 Essayer BOOTO ScanGrade AI V2 en ligne](https://booto-scangrade-ai-v2.onrender.com/)** — Render a confirmé « Deploy succeeded · Live » le 23 octobre 2026 d'après la capture du propriétaire. Le fonctionnement complet sur la tablette Lenovo Tab M11 doit encore être testé. **Utiliser uniquement des documents fictifs/anonymisés, sans données d'élèves identifiables.**

## Ce que cette V2 réalise

Une application statique unique, à destination d'une tablette Android Lenovo Tab M11 :

1. **Numérisation en continu** avec caméra arrière et stabilisation après mouvement, première photo manuelle puis tentatives automatiques. Alternance recto-verso dans l'ordre des pages, regroupement par copie anonyme `C001` etc., masquage facultatif des 20 % supérieurs de l'image (activé par défaut), export ZIP local.
2. **Passage direct vers l'évaluation** : les photographies capturées restent en mémoire du navigateur et sont immédiatement consultables dans l'onglet Évaluer, sans export ZIP préalable. Import facultatif d'un ZIP V0 pour consultation.
3. **Évaluation mixte configurable** : QCM, vrai/faux, réponse courte, identification d'image et question ouverte. L'enseignant saisit les réponses observées (aucun OCR). Image pédagogique optionnelle locale par question ; aucune image externe n'est téléchargée.
4. **Propositions déterministes** : égalité texte pour QCM et vrai/faux ; comparaison accent-insensible très prudente pour réponses courtes ; **aucune notation automatique des images ou questions ouvertes**. Toute réponse courte, image ou ouverte exige une vérification manuelle ; **tous les scores** doivent être confirmés un par un.
5. **Valider et suivre** : commentaire pédagogique généré à partir des domaines et points **validés par le professeur**, modifiable ; note sur 7/10/20/100 ; suivi anonyme T1/T2/T3 et révision sans doublons pour une activité donnée ; fichier Excel réel (onglets `Evaluations`, `Synthese`), CSV et sauvegarde/restauration JSON. Pour plusieurs activités dans un même trimestre, la moyenne simple est utilisée (aucune pondération institutionnelle).

**AUCUNE lecture de l'écriture manuscrite, aucune reconnaissance visuelle automatique des réponses aux images, aucune IA générative, aucun Google Sheets connecté et aucune certification CECRL.** Le mot « AI » correspond à la marque, pas à une fonctionnalité d'IA prouvée dans cette V2.

## Protection renforcée — mais pilote non autorisé pour dossiers réels d'élèves

- **Verrou préalable** : la capture, les imports et l'évaluation demandent de confirmer l'emploi de documents fictifs ou anonymisés. Cette déclaration n'est **pas** un mécanisme d'authentification ni un consentement juridiquement valable.
- **Pas de compte ni serveur de collecte** : JavaScript statique, aucun formulaire réseau, aucun CDN, politique CSP bloquant `connect-src`. Attention : le fournisseur d'hébergement conserve potentiellement des journaux techniques de navigation (ex. adresse IP) et le navigateur peut conserver des fichiers dans ses téléchargements.
- **Pas de `localStorage`, cookies applicatifs ni base distante** : photos et notes maintenues dans la mémoire de la page uniquement. Elles sont perdues à l'actualisation/fermeture ; exporter de manière volontaire vers une destination approuvée. Les fichiers téléchargés subsistent sur l'appareil jusqu'à suppression.
- **Caméra sur autorisation** et arrêt explicite, détection limitée à 120 pages, images importées max 12 Mo, 1600 px, compression JPEG qui élimine les EXIF ; ZIP importé max 120 Mo, JSON registre max 5 Mo. Les contenus sont affichés via `textContent` plutôt que HTML non filtré.
- **Masquage du bandeau supérieur par défaut**, mais il est approximatif et **ne suffit pas** pour anonymiser une copie réelle : noms et autres indices peuvent figurer ailleurs. La graphie d'un enfant peut elle-même être identifiable.
- **Validation humaine de chaque item et confirmation globale** avant d'inscrire la note ; aucun transfert automatique des notes à des systèmes scolaires.

### Conditions avant toute expérimentation sur copies scolaires identifiables

- Obtenir l'accord explicite de la direction et du responsable de traitement, vérifier la base légale et les autorisations/informations applicables aux responsables légaux et élèves, et documenter l'intérêt supérieur des mineurs.
- Établir une politique de confidentialité, des engagements de confidentialité, la durée de conservation, les modalités de suppression et la procédure de réponse aux incidents.
- Déployer l'usage réel sur une infrastructure approuvée avec authentification, contrôles d'accès par rôle, chiffrement au stockage, journalisation contrôlée, sauvegardes sécurisées et conventions avec hébergeurs/prestataires.
- Définir les autorisations de transfert transfrontalier au besoin ; éviter tout compte personnel pour les résultats d'élèves ; ne pas utiliser les photos ni les productions pour entraîner une IA sans base légale adéquate.
- Vérifier les programmes officiels, les barèmes et la fiabilité des commentaires et des corrections au moyen d'essais documentés sous contrôle pédagogique.

**Références officielles (Colombie)** :
- Ley 1581 de 2012 : https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981
- Superintendencia de Industria y Comercio, exigences pour les mineurs : https://sedeelectronica.sic.gov.co/publicaciones/boletin-juridico/concepto/tratamiento-excepcional-y-autorizacion-del-representante-legal-con-interes-superior
- OWASP, contrôle des fichiers reçus : https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html

Ces exigences doivent être adaptées et revues par l'établissement et un responsable de conformité ; ce prototype n'est pas certifié.

## Essai sur Lenovo Tab M11 — lundi 26 octobre 2026

1. Ouvrir l'URL HTTPS du **nouveau** site statique V2 dans Chrome sur la tablette et cocher la case d'usage fictif.
2. **Scanner** : stabiliser la tablette, activer la caméra et photographier une première feuille fictive, puis faire tourner/retourner des feuilles d'essai. Vérifier les miniatures, le recto-verso et l'archive ZIP. Si plusieurs copies, cliquer sur Nouvelle copie entre les lots.
3. Cliquer « Consulter et corriger ces copies » : onglet Évaluer avec les photos **sans transfert ZIP**.
4. Utiliser l'exercice fictif mixte de cinq questions ; cliquer « Réponses fictives » pour simuler les réponses ; calculer ; contrôler chaque note et cocher chaque validation. Pour les réponses ouvertes et images, attribuer vous-même les points.
5. Valider le commentaire et la note, puis exporter le fichier XLSX ; le réimporter manuellement dans Google Sheets **avec un compte et un environnement approuvés** si nécessaire.
6. Tester les erreurs : absence de validation = aucune nouvelle note ; deuxième correction d'une même activité/trimestre = révision, pas de doublon. Vérifier l'arrêt de la caméra et l'effacement.

**Limites d'usage** : l'évaluation de lundi devra se faire avec **copies d'entraînement fictives ou réellement anonymisées**, pas avec des documents scolaires personnels non autorisés. Vous pouvez consulter vos copies réelles hors application pour préparer le protocole, mais ne pas les importer sans les validations institutionnelles nécessaires.

## Tests et déploiement

Lancer `node --test tests/*.test.cjs` (Node 18+) et servir le dossier via HTTPS ou `python -m http.server 8000` sur localhost. L'accès à la caméra sur tablette exige un site HTTPS.

**Render : Nouveau Static Site**, dépôt `Junior-BOOTO/python.skills`, branche `main`, **Root Directory `booto-scangrade-ai-v2`**, Build Command `echo ready`, Publish Directory `.`, sans variable API. **Ne pas modifier** les services V0 et V1 existants. Aucun déploiement public V2 ne doit être considéré effectif avant confirmation Render.

© 2026 BOOTO AI & DATA INNOVATION LAB.
