"""Démonstration sans dépendances tierces : python scripts/run_demo.py"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from booto_fle.engine import evaluate, group_summary, recommend

if __name__ == "__main__":
    dashboard = group_summary()
    first = dashboard["details"][1]
    print("BOOTO FLE Adaptive AI V1 — démonstration 100 % synthétique")
    print(f"Profils fictifs : {dashboard['n_profiles']}")
    print("Synthèse des compétences (comptage de statuts) :")
    print(json.dumps(dashboard["status_totals"], ensure_ascii=False, indent=2))
    print(f"Recommandations du profil fictif {first['student_id']} :")
    for rec in first["recommendations"]:
        print(f"- {rec['titre']} ({rec['motif']})")
