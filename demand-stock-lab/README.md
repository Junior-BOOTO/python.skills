# BOOTO Demand & Stock Lab
Junior BOOTO Waba · Projet de formation Python/Data réalisé avec assistance IA.

Prévoir quatre semaines de ventes et simuler une quantité de réapprovisionnement pour un responsable de magasin. Prototype reproductible, sans clé payante. L’application Streamlit est préparée mais pas encore déployée ni vérifiée visuellement.

## Démonstration
```bash
pip install -r requirements.txt
python engine.py
python -m unittest discover -s tests -v
streamlit run app.py
```
Depuis la racine du dépôt : `cd demand-stock-lab` avant ces commandes.
Pour vos données : `python engine.py --csv ventes.csv` ou import dans l’interface.

Entrée : CSV `date,product,sales`, dates ISO, ventes hebdomadaires non négatives en unités. Une ligne par produit/semaine, au moins 112 semaines consécutives par produit. Aucun remplissage silencieux des semaines absentes. Les ventes observées peuvent sous-estimer la demande en cas de rupture.

## Méthode et résultats exécutés
Source : générateur original `demo()` (graine 42), 156 semaines et 3 produits, données entièrement synthétiques, sans données clients. Les caractéristiques sont le temps, sinus et cosinus annuels. Comparaison : moyenne des 4 dernières semaines contre régression Ridge (alpha fixé à 1). Aucun résultat d’une entreprise réelle.

Sélection sur 3 blocs chronologiques de 4 semaines avant le test ; test sur les 12 dernières semaines, avec réentraînement à chaque origine et horizon de 4 semaines. La sélection reste figée pendant le test. Les prévisions finales réutilisent ensuite toutes les observations disponibles.

| Produit | MAE test moyenne 4 semaines | MAE test Ridge sélectionnée |
|---|---:|---:|
| A | 3,25 | 2,00 |
| B | 4,46 | 2,77 |
| C | 3,83 | 2,85 |

MAE = erreur absolue moyenne en unités/semaine, 12 prévisions test par produit. Scores détaillés : [metrics.json](reports/metrics.json). Le générateur contient volontairement tendance et saisonnalité : résultat favorable au modèle et non généralisable sans test sur données réelles.

Exemple : demande prévue 100 unités, stock 20, livraisons 10 et réserve 5 → commande indicative de 75 unités.

Formule : plafond(max(0, demande prévue sur 4 semaines + réserve − stock − livraisons)). La réserve est choisie par l’utilisateur ; elle ne correspond pas à un niveau de service statistique.

## Vérifications et limites
5 tests réussis : série constante, calcul du stock, anomalies de données, pipeline et séparation temporelle d’une prévision. Moteur exécuté avec Python et numpy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0. Interface non exécutée dans l’environnement de création : Streamlit absent. Version Streamlit à figer après validation de l’interface.

Ce MVP ne modélise pas les délais, commandes minimales, coûts, promotions, intervalles prédictifs, ventes perdues ni ruptures intra-période. Aucun gain financier réel revendiqué. Ne pas importer de données confidentielles dans un service public.

## Déploiement Render à préparer
Type : Web Service. Commande de construction : `pip install -r demand-stock-lab/requirements.txt`. Démarrage : `streamlit run demand-stock-lab/app.py --server.address 0.0.0.0 --server.port $PORT`. Aucun service Render créé à ce stade.

## Prochaine étape
Valider l’interface, puis tester sur un historique commercial autorisé et comparer plusieurs fenêtres temporelles avant tout usage opérationnel.

English: A reproducible synthetic weekly sales forecasting and inventory scenario lab. Chronological validation, held-out rolling test, baseline comparison and explicit operational limits. Streamlit UI prepared; deployment pending.
