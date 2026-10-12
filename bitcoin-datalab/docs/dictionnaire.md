# Dictionnaire
| Variable | Définition | Unité |
|---|---|---|
| Date | Début du jour selon timestamp Unix de la source | UTC |
| Open / High / Low / Close | Ouverture, maximum, minimum, clôture | USD par BTC |
| Volume | Volume BTC selon en-tête fournisseur | BTC |
| r1 / r3 / r7 | Rendement du cours sur 1 / 3 / 7 jours | fraction |
| vol7 / vol30 | Écart-type des rendements quotidiens | fraction |
| range | (High − Low) / Close | fraction |
| volume_change | Variation relative du volume | fraction |
| cible | Close(t+1) / Close(t) − 1 | fraction |

Pas de remplissage des absences ; lignes initiales sans fenêtres complètes et dernière cible indisponible exclues de l’entraînement. Date cible = date observation + un jour.
