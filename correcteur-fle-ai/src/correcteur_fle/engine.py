"""Moteur local et explicable de suggestions pour de courtes productions FLE A1.

Ce moteur ne corrige PAS le français libre de façon générale. Il applique un petit
ensemble de règles ciblées sur des erreurs connues. Les décisions appartiennent à
l'enseignant, aucune note automatique ni profilage des apprenants.
"""
from __future__ import annotations
from dataclasses import dataclass
import re

MAX_CHARS = 900
THEMES = {
    "routine": "Ma journée typique · Grade 4 · A1",
    "ecologie": "Droits, devoirs & écoresponsabilité · Grade 5 · A1",
}

@dataclass(frozen=True)
class Rule:
    ident: str
    pattern: str
    correction: str
    category: str
    explanation: str
    themes: tuple[str, ...]
    criterion: str

RULES: tuple[Rule, ...] = (
    Rule("pronom_se_leve", r"\bje se l[eè]ve\b", "je me lève", "Verbes pronominaux", "Avec « je », le pronom réfléchi est « me ».", ("routine",), "Je peux utiliser les verbes pronominaux avec « je »."),
    Rule("pronom_se_couche", r"\bje se couche\b", "je me couche", "Verbes pronominaux", "Avec « je », on dit « je me couche ».", ("routine",), "Je peux utiliser les verbes pronominaux avec « je »."),
    Rule("pronom_infinitif_lever", r"\bje me lever\b", "je me lève", "Conjugaison", "À la première personne, le verbe est conjugué : « je me lève ».", ("routine",), "Je peux conjuguer quelques verbes au présent."),
    Rule("pronom_infinitif_coucher", r"\bje me coucher\b", "je me couche", "Conjugaison", "Au présent avec « je », on écrit « je me couche ».", ("routine",), "Je peux conjuguer quelques verbes au présent."),
    Rule("leve_accent", r"\bje me leve\b", "je me lève", "Accents", "Le verbe « lever » prend un accent grave : « je me lève ».", ("routine",), "Je peux écrire le vocabulaire de ma routine."),
    Rule("prepare_accent", r"\bje me prepare\b", "je me prépare", "Accents", "Au présent : « je me prépare », avec un accent aigu.", ("routine",), "Je peux écrire le vocabulaire de ma routine."),
    Rule("reveil_accent", r"\bje me reveille\b", "je me réveille", "Accents", "On écrit « réveille » avec un accent aigu.", ("routine",), "Je peux écrire le vocabulaire de ma routine."),
    Rule("vais_present", r"\bje va\b", "je vais", "Conjugaison", "« Aller » au présent avec « je » donne « je vais ».", ("routine",), "Je peux conjuguer quelques verbes au présent."),
    Rule("mange_present", r"\bje manges\b", "je mange", "Conjugaison", "Le présent de « manger » avec « je » est « je mange ».", ("routine",), "Je peux conjuguer quelques verbes au présent."),
    Rule("heure_sept", r"\ba sept heures\b", "à sept heures", "Accents", "Pour exprimer une heure, on utilise la préposition « à ».", ("routine",), "Je peux indiquer une heure avec « à » ou « vers »."),
    Rule("heure_huit", r"\ba huit heures\b", "à huit heures", "Accents", "Pour exprimer une heure, on utilise la préposition « à ».", ("routine",), "Je peux indiquer une heure avec « à » ou « vers »."),
    Rule("je_doit_protege", r"\bje doit protege\b", "je dois protéger", "Conjugaison et infinitif", "Avec « je », on dit « je dois » ; après « devoir », on emploie l’infinitif « protéger ».", ("ecologie",), "Je peux exprimer une obligation et une action écoresponsable."),
    Rule("je_doit", r"\bje doit\b", "je dois", "Conjugaison", "Le verbe « devoir » au présent avec « je » donne « je dois ».", ("ecologie",), "Je peux exprimer une obligation simple."),
    Rule("nous_doit", r"\bnous doit\b", "nous devons", "Conjugaison", "Avec « nous », on dit « nous devons ».", ("ecologie",), "Je peux exprimer une obligation simple."),
    Rule("il_faut_protege", r"\bil faut protege\b", "il faut protéger", "Infinitif", "Après « il faut », on emploie ici l'infinitif « protéger ».", ("ecologie",), "Je peux proposer une action écoresponsable."),
    Rule("je_protege", r"\bje protege\b", "je protège", "Accents", "Au présent : « je protège », avec un accent grave.", ("ecologie",), "Je peux proposer une action écoresponsable."),
    Rule("les_arbre", r"\bles arbre\b", "les arbres", "Accord nominal", "Après « les », le nom « arbres » prend un « s » au pluriel.", ("ecologie",), "Je peux identifier un pluriel courant."),
    Rule("des_arbre", r"\bdes arbre\b", "des arbres", "Accord nominal", "Après « des », on écrit « arbres » au pluriel.", ("ecologie",), "Je peux identifier un pluriel courant."),
    Rule("dechets_accent", r"\bles dechets\b", "les déchets", "Accents", "Le mot « déchets » comporte deux accents aigus.", ("ecologie",), "Je peux employer le vocabulaire de l'environnement."),
    Rule("nous_protegeons", r"\bnous protegeons\b", "nous protégeons", "Accents", "Avec « nous », on écrit « protégeons ».", ("ecologie",), "Je peux proposer une action écoresponsable."),
)

@dataclass(frozen=True)
class Suggestion:
    ident: str
    category: str
    original: str
    proposal: str
    explanation: str
    criterion: str
    start: int
    end: int

@dataclass(frozen=True)
class Analysis:
    original: str
    theme: str
    suggestions: tuple[Suggestion, ...]
    preview: str
    observation: str


def _capitalize_first(pattern: str, replacement: str) -> str:
    return replacement[:1].upper() + replacement[1:] if pattern[:1].isupper() else replacement


def analyze(text: str, theme: str = "routine") -> Analysis:
    if theme not in THEMES:
        raise ValueError("Thème inconnu.")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Saisissez une production écrite non vide.")
    if len(text) > MAX_CHARS:
        raise ValueError(f"Limite de {MAX_CHARS} caractères pour cette démonstration.")
    # Evaluate matches on the ORIGINAL (stable spans, no cascading corrections).
    matches = []
    for rule in RULES:
        if theme not in rule.themes:
            continue
        for match in re.finditer(rule.pattern, text, re.IGNORECASE):
            proposal = _capitalize_first(match.group(0), rule.correction)
            matches.append((match.start(), match.end(), rule, match.group(0), proposal))
    # Prevent overlapping edits: earliest start, prefer the longer expression.
    matches.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    accepted = []
    cursor = 0
    for start, end, rule, original, proposal in matches:
        if start < cursor:
            continue
        accepted.append(Suggestion(rule.ident, rule.category, original, proposal, rule.explanation, rule.criterion, start, end))
        cursor = end
    suggestions = tuple(accepted)
    preview = review_suggestions(text, suggestions)
    observation = ("Les règles n'ont pas relevé d'expression couverte par cette V1. Cela ne garantit pas que le texte soit correct."
                   if not suggestions else
                   f"{len(suggestions)} piste(s) de révision ciblée(s) : validation obligatoire par l'enseignant.")
    return Analysis(text, theme, suggestions, preview, observation)


def review_suggestions(original: str, suggestions: tuple[Suggestion, ...], selected: set[int] | None = None) -> str:
    """Apply selected suggestions (0-based indices) to original spans, in reverse order."""
    if selected is None:
        selected = set(range(len(suggestions)))
    if not isinstance(original, str):
        raise ValueError("Texte incorrect.")
    output = original
    for i in sorted(selected, reverse=True):
        if not 0 <= i < len(suggestions):
            raise ValueError("Index de suggestion invalide.")
        s = suggestions[i]
        if original[s.start:s.end] != s.original:
            raise ValueError("Décalage : la suggestion ne correspond pas au texte initial.")
        output = output[:s.start] + s.proposal + output[s.end:]
    return output
