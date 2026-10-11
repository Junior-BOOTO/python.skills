# Global Superstore — Tableau de bord des performances commerciales
**Junior BOOTO Waba · Projet 7 · Python et visualisation web**

Tableau de bord interactif d’une entreprise fictive, sur ses données historiques 2011–2014. Le script Python prépare les indicateurs ; l’interface web filtre année, marché, région, catégorie et segment.

## Ouvrir le tableau de bord
```sh
python -m http.server 8000 --directory web
```
Ouvrir http://localhost:8000 dans un navigateur. Le dossier `web/` contient les résultats préparés : aucune dépendance Python supplémentaire n’est nécessaire pour le consulter.

## Reproduire la préparation
```sh
python -m pip install -r requirements.txt
python preparer.py
node verifier.mjs
```
Au premier lancement, Python télécharge le classeur officiel Tableau si `raw/Global Superstore.xls` est absent. Internet est alors nécessaire. Les fichiers bruts sont préservés et les sorties sont régénérées. Node sert uniquement aux contrôles du moteur de filtres.

## Fonctionnalités
- Ventes, bénéfice, marge, commandes distinctes, panier moyen et taux de commandes signalées retournées.
- Filtres combinés, réinitialisation, tendance mensuelle ventes/bénéfice, classement des régions et comparaison des catégories.
- Tableau mensuel accessible et export CSV du périmètre filtré.
- Gestion d’un résultat vide, montants négatifs et dénominateurs nuls.

## Méthode et contrôles
La granularité source est une ligne de commande. La clé de commande combine `Market` et `Order ID` : le seul identifiant de commande n’est pas unique entre marchés. Les retours sont joints en many-to-one après harmonisation de `United States` vers `US` (296 retours concernés). Aucun nom de client n’est exporté dans l’interface.

Les cellules agrégées contiennent les clés internes des commandes. Le moteur utilise des ensembles pour compter les commandes distinctes sous n’importe quelle combinaison de filtres, plutôt que de sommer les comptages par catégorie.

Huit scénarios, dont des filtres combinés et un résultat vide, comparent le moteur JavaScript aux calculs Python sur les lignes sources. Ventes et bénéfices sont réconciliés par marché, région et catégorie. Les détails figurent dans [le rapport](reports/rapport.md) et [le manifeste](manifest.json).

## Compatibilité BI
Le CSV `collected/ventes_preparees.csv`, produit en exécutant Python, est utilisable dans Power BI ou Tableau. [Le guide BI](reports/guide_bi.md) précise dimensions et formules. Ce dépôt livre une version web ; il ne contient pas de `.pbix`, `.twb` ou `.twbx`.

## Limites et attribution
Données historiques fictives, sans connexion temps réel. Devise non documentée dans le classeur : montants en unités monétaires du jeu (UM). Le bénéfice est celui fourni par la source, pas un résultat net recalculé.

Le taux de retour porte sur des commandes signalées retournées, pas sur les unités retournées. Les remboursements ne sont pas détaillés ; aucun ajustement du chiffre d’affaires n’est inventé.

Source : [Global Superstore, Tableau](https://www.tableau.com/sites/default/files/training/global_superstore.zip). Le classeur brut n’est pas redistribué : URL, empreinte et script de collecte sont fournis. Les fichiers publiés contiennent le code et les agrégats de l’analyse. Inspiration : *Data Analysis Projects*, Natacha Njongwa Yepnga / LeCoinStat, projet 7.
