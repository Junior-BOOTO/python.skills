# Méthode, provenance et droits

Source officielle : https://www.python.org/blogs/ (lien RSS Python Insider).
Endpoint utilisé : https://blog.python.org/feeds/posts/default?alt=rss .
Licence indiquée pour Python Insider : CC BY-NC-SA 3.0, https://creativecommons.org/licenses/by-nc-sa/3.0/ . Attribution : Python Core Team. Les métadonnées et leur cache dérivé restent sous ces conditions ; code et fixtures fictives sous MIT.

L’extraction ne retient que titres, liens, GUID et dates de publication. Des champs supplémentaires décrivent la collecte et le classement. Aucun corps d’article republié. L’état réel conserve l’empreinte SHA-256 de la réponse réseau et son type MIME ; la réponse originale n’est pas incluse dans le dépôt public pour éviter de republier des textes.

Une première tentative s’est arrêtée sur le type MIME générique. `demo/initial_blocked/manifest.json` conserve cet incident. Le lecteur accepte désormais application/octet-stream puis valide réellement la structure RSS ; une page HTML n’est pas traitée comme un flux.

Les motifs de pertinence sont des mots-clés explicites dans le titre. La couverture Python est démontrée ; une couverture IA/éducation ne l’est pas avec ce seul flux. La comparaison après ajout d’une autre source nécessitera un nouveau protocole.

Changements fictifs : A change de titre ; B reste identique ; C n’est plus dans la fenêtre ; D apparaît. Ces quatre événements ne constituent pas des changements constatés dans la collecte réelle.
