# BOOTO ScanGrade AI · Scanner tablette — Prototype V0

**Auteur : Junior BOOTO Waba · BOOTO AI & DATA INNOVATION LAB · 23 octobre 2026**

Prototype browser-first ciblant Lenovo Tab M11 (configurations 4 ou 8 Go), **numérisation uniquement**. Pas encore un correcteur ni un produit scolaire prêt à l'emploi.

## Fonctions effectivement codées

- Caméra arrière via l'API navigateur `getUserMedia`, avec autorisation explicite.
- **Première page photographiée manuellement**, puis détection expérimentale de mouvement → immobilité → changement d'image pour les pages suivantes. Les photos restent possibles manuellement en cas d'échec.
- Import optionnel JPEG/PNG/WebP, conversion en JPEG avec suppression des métadonnées EXIF dans l'image produite.
- Création d'identifiants de copies **anonymes** C001, C002… ; étiquetage par trimestre T1/T2/T3.
- Alternance recto/verso (recto page 1, verso page 2) si l'enseignant retourne **chaque feuille**, dans cet ordre ; mode recto seul sinon. Le système ne tourne pas les feuilles et n'identifie pas automatiquement leur propriétaire.
- Miniatures et suppression des photos mal cadrées.
- Export d'un lot ZIP en une action : images JPG + `inventaire.csv` + `manifest.json`, **aucune API ni bibliothèque distante**. Le code ZIP local est testé avec vérification CRC32.
- Aucune sauvegarde persistante : quitter/actualiser sans exporter détruit la session.

## Utilisation

1. Ouvrir la page depuis **HTTPS** sur Chrome Android ; autoriser la caméra.
2. Installer la tablette sur un support stable, caméra dirigée vers le papier et éclairage suffisant.
3. Choisir « Recto-verso » avant de commencer si nécessaire, choisir T1/T2/T3.
4. Appuyer sur « Photographier la première page ». Tourner ensuite **physiquement** chaque page pour que le déclenchement automatique expérimental détecte une nouvelle page stable.
5. Vérifier toutes les miniatures ; pour les pages presque identiques, utiliser le bouton manuel. Cliquez « Nouvelle copie » à chaque changement de copie.
6. Exporter ZIP et vérifier le fichier dans Téléchargements **avant** de vider le lot.

La détection ne garantit ni cadrage correct, ni capture de toutes les pages. Il faut vérifier les miniatures et le ZIP. La V0 limite les lots à 120 photos et redimensionne à 1600 pixels au plus grand côté pour réduire la mémoire occupée.

## Essai local sur ordinateur

```sh
cd booto-scangrade-ai
python -m http.server 8000
# ouvrir http://localhost:8000
node --test tests/*.test.cjs
```

La caméra d'une tablette exige **HTTPS** (ou `localhost` directement sur le même appareil). Ouvrir `file://` ne garantit pas la permission caméra.

## Déploiement de démonstration Render

Nouveau **Static Site** distinct : dépôt `Junior-BOOTO/python.skills`, branche `main`, `Root Directory = booto-scangrade-ai`, `Build Command = echo ready`, `Publish Directory = .`. Ne configurez pas de clé API. Ce dépôt ne collecte pas les copies : elles sont seulement conservées dans la mémoire du navigateur pendant l'usage.

## Limites et futur développement

- Le mouvement de la main / la luminosité / les écritures semblables peuvent provoquer des non-détections ou des prises intempestives ; aucun algorithme de détection de quadrilatère, d'alignement ou de netteté avancé n'est encore validé.
- Pas de rotation automatique du papier ni d'ADF. Pas d'identification automatique des copies.
- **Pas d'OCR manuscrit, pas d'IA de correction, pas de score ni de commentaire pédagogique automatique, pas de synchronisation Google Sheets ou Excel** dans cette version.
- Les applications futures nécessiteront un moteur de correction avec révision enseignante, journal d'audit, contrôle d'accès et infrastructure sécurisée. Ne jamais stocker de noms ou copies identifiables d'enfants dans ce prototype.
- Les tests automatisés portent sur les composants de logique et l'archive ZIP ; la caméra et la détection réelle sur Lenovo Tab M11 **restent à tester sur l'appareil**.

**Sécurité** : ne pas utiliser des données réelles d'élèves, notamment de mineurs, avant étude des règles applicables et autorisations de l'établissement.

© 2026 Junior BOOTO Waba. Tous droits réservés.
