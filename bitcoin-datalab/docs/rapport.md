# Bitcoin DataLab — Junior BOOTO

Collecte réelle : https://www.cryptodatadownload.com/cdd/Bitstamp_BTCUSD_d.csv le 12 octobre 2026. Source : Bitstamp, distribution CryptoDataDownload. Données propres à cet échange, différentes de Yahoo. Téléchargement structuré CSV, sans scraping HTML.

4336 lignes dans la source brute. 1967 journées consécutives retenues du 1er janvier 2021 au 21 mai 2026. Le 22 mai 2026 est absent : exclusion de la période ultérieure pour ce premier protocole, sans interpolation. Conversion des timestamps Unix en UTC, volume en BTC selon l'en-tête de la source. Contrôles réussis : valeurs obligatoires, cours positifs, cohérence OHLC, volumes non négatifs, dates uniques et quotidiennes.

Cible : rendement du lendemain après clôture UTC, reconstruit en prix USD. Sept variables : rendements 1/3/7 jours, volatilité 7/30 jours, amplitude et variation du volume. Découpage 60/20/20 chronologique avec une observation de séparation. Prétraitement appris seulement sur l'entraînement. Ridge et forêt évalués sur validation. Ridge retenu avant consultation du test.

Test : 388 observations, du 2025-04-29 00:00:00+00:00 au 2026-05-21 00:00:00+00:00.

| Méthode | MAE USD | RMSE USD |
|---|---:|---:|
| Cours inchangé | 1425.70 | 1961.90 |
| Ridge | 1445.10 | 1975.12 |

Ridge ne surpasse pas la référence sur le test final. Aucun avantage prédictif démontré. Ce test ne doit plus servir de test indépendant pour sélectionner de nouvelles variantes. L'export Ridge et forêt ainsi que leur rechargement et l'égalité des prédictions ont été vérifiés. La forêt est un candidat, sans score de test. Modèles expérimentaux non déployés ; aucune prévision actuelle émise car historique retenu arrêté en mai.

Statistiques sur la période retenue : écart-type du rendement quotidien 3.05 %, baisse maximale du cours de clôture -76.66 %.

Données distribuées sous CC BY-NC-SA 4.0 selon CryptoDataDownload : attribution, usage non commercial et partage à l'identique applicables. Pas de publication externe réalisée.

## Reproduction

Installer requirements.txt puis lancer : python run.py input.csv --out output
Le fichier input.csv est la sélection normalisée utilisée ; source_original.csv préserve le fichier téléchargé. Consulter output/reports/results.json et output/manifest.json. Le manifeste conserve l'empreinte du fichier normalisé.
