from pathlib import Path
import sqlite3,json,csv,hashlib,zipfile,html
from decimal import Decimal
root=Path(__file__).parent
out=root/"resultats";out.mkdir(exist_ok=True)
db=root/"data/Chinook.sqlite"
if not db.exists():
 c=sqlite3.connect(db);c.executescript((root/"data/Chinook_Sqlite.sql").read_text());c.close()
con=sqlite3.connect("file:"+str(db)+"?mode=ro",uri=True);con.execute("PRAGMA query_only=ON")
assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
queries=json.loads((root/"queries.json").read_text())
summary=[];sections=[]
for i,(title,sql,note) in enumerate(queries,1):
 cur=con.execute(sql);cols=[x[0] for x in cur.description];rows=cur.fetchall()
 with (out/f"exercice_{i:02d}.csv").open("w",newline="",encoding="utf-8-sig") as f:
  w=csv.writer(f);w.writerow(cols);w.writerows(rows)
 summary.append({"exercice":i,"titre":title,"lignes":len(rows)})
 preview="| "+" | ".join(cols)+" |\n| "+" | ".join("---" for _ in cols)+" |\n"
 preview+="\n".join("| "+" | ".join(str(x).replace("|","/") for x in row)+" |" for row in rows[:5])
 if not rows:preview="Aucune ligne : aucune donnée disponible pour ce filtre."
 sections.append(f"## {i}. {title}\n\n{note}\n\n```sql\n{sql}\n```\n\nRésultat : {len(rows)} lignes. Aperçu :\n\n{preview}\n")
adapted=[]
for i,old,new in [(8,"2009","2021"),(18,"2009","2021"),(19,"2010","2022"),(23,"2013","2025")]:
 title,sql,note=queries[i-1]
 sql=sql.replace(old,new)
 if i==8:sql=sql.replace("2011","2023")
 cur=con.execute(sql);rows=cur.fetchall();cols=[x[0] for x in cur.description]
 with (out/f"exercice_{i:02d}_annees_disponibles.csv").open("w",newline="",encoding="utf-8-sig") as f:
  w=csv.writer(f);w.writerow(cols);w.writerows(rows)
 adapted.append((i,sql,[dict(zip(cols,r)) for r in rows]))
(root/"chinook-queries-annees-disponibles.sql").write_text("\n\n".join(f"-- Variante de l'exercice {i}\n{sql}" for i,sql,_ in adapted))
total=float(con.execute("SELECT SUM(Total) FROM Invoice").fetchone()[0])
lines_total=float(con.execute("SELECT SUM(UnitPrice*Quantity) FROM InvoiceLine").fetchone()[0])
assert abs(total-lines_total)<1e-8
# Les rapports géographiques et agents doivent réconcilier le total des factures.
for i in [17,22]:
 assert abs(sum(float(r[-1]) for r in con.execute(queries[i-1][1]))-total)<1e-8
assert len(con.execute(queries[15][1]).fetchall())==con.execute("SELECT COUNT(*) FROM Invoice").fetchone()[0]
tables={name:con.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0] for name, in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")}
schema={name:[dict(zip(["cid","name","type","notnull","default","pk"],r)) for r in con.execute('PRAGMA table_info("'+name+'")')] for name in tables}
(root/"schema.json").write_text(json.dumps(schema,ensure_ascii=False,indent=2))
years=con.execute("SELECT MIN(InvoiceDate),MAX(InvoiceDate) FROM Invoice").fetchone()
top_country=dict(zip(["pays","ventes"],con.execute(queries[21][1]).fetchone()))
best=dict(zip(["id","agent","ventes"],con.execute(queries[19][1]).fetchone()))
kpi={"periode":years,"factures":tables["Invoice"],"clients":tables["Customer"],"morceaux":tables["Track"],"ventes":round(total,2),"panier_moyen":round(total/tables["Invoice"],2),"meilleur_pays":top_country,"meilleur_agent":best}
(root/"resultats/synthese.json").write_text(json.dumps({"kpi":kpi,"tables":tables,"exercices":summary,"variantes":adapted,"controles":{"integrite":"ok","cles_etrangeres":"ok","total_factures_egal_lignes":True,"total_agents_egal_global":True,"total_pays_egal_global":True}},ensure_ascii=False,indent=2))
report=f"""# Chinook — 26 exercices SQL exécutés
Auteur du projet : Junior BOOTO Waba.
## Portée et provenance
Exercices inspirés de « Data Analysis Projects », Natacha Njongwa Yepnga / LeCoinStat, projet 5. Requêtes écrites et exécutées dans SQLite.
Source : https://github.com/lerocha/chinook-database/blob/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql
Blob GitHub : 299610dc69f04a2b16b3a2e45bd2af82ed2872a2.
Chinook est une base de démonstration : ventes générées et clients/employés fictifs. Aucun résultat commercial réel.
## Résultats vérifiés
- {tables['Invoice']} factures ; {tables['Customer']} clients ; {tables['Track']} morceaux.
- Ventes : {total:.2f} unités monétaires ; panier moyen : {kpi['panier_moyen']:.2f}.
- Pays en tête : {top_country['pays']} ({top_country['ventes']:.2f}).
- Agent en tête : {best['agent']} ({best['ventes']:.2f}).
- Période : {years[0][:10]} au {years[1][:10]}.
## Adaptation des exercices
Les exercices 8, 18, 19 et 23 demandent 2009, 2010, 2011 ou 2013. Ces années sont absentes de cette version. Le fichier principal conserve les filtres demandés ; les résultats vides ou nuls ne prouvent pas une absence historique de ventes. Un second fichier contient les variantes 2021/2023, 2021, 2022 et 2025. Les années ne sont pas changées silencieusement.
Les classements en unités et en chiffre d'affaires sont distingués. Les ex æquo sont conservés pour les gagnants ; les tops de cinq ou trois lignes utilisent l'identifiant comme départage explicite.
## Contrôles
Intégrité SQLite et clés étrangères vérifiées. Total des factures égal à celui des lignes ; sommes par agent et pays réconciliées au total. 26 requêtes exécutées, 26 CSV générés, plus quatre variantes annuelles.
## Limites
Les données ne permettent pas d'estimer bénéfice ou marge : aucun coût de revient n'est fourni. Une différence entre agents peut refléter leur portefeuille ; elle ne démontre pas leur performance causale.
Machine learning non utilisé : ce projet porte sur SQL et des rapports descriptifs.
"""
(root/"rapport.md").write_text(report)
(root/"guide_exercices.md").write_text("# Guide SQL — Chinook\n\nChaque exercice contient la requête, son explication et un aperçu des résultats. Les CSV complets sont dans resultats/.\n\n"+"\n".join(sections))
readme="""# Analyse SQL des ventes — Chinook
**Junior BOOTO Waba · Projet d'apprentissage documenté**

26 exercices SQL résolus et exécutés, résultats CSV, guide explicatif et contrôles de cohérence.

## Ouvrir et reproduire
- Avec DB Browser for SQLite : ouvrir data/Chinook.sqlite, puis utiliser l'onglet Exécuter le SQL avec chinook-queries.sql.
- Avec Python 3 (bibliothèque standard uniquement) : exécuter python executer_projet.py depuis ce dossier.
- Consulter rapport.md pour les résultats et guide_exercices.md pour les explications.
- La commande régénère les fichiers resultats/ et la documentation dans ce dossier.

## Compétences
SELECT, WHERE, JOIN, LEFT JOIN, GROUP BY, COUNT, SUM, DISTINCT, CTE, sous-requêtes, filtres temporels, gestion des ex æquo et contrôle de la granularité.

## Sources et limites
Base officielle de Luis Rocha : https://github.com/lerocha/chinook-database
Licence incluse dans LICENSE-Chinook.md.
Exercices : Data Analysis Projects, Natacha Njongwa Yepnga / LeCoinStat, projet 5 (source des exercices SQL citée dans le PDF : LucasMcL/15-sql_queries_02-chinook).
Cette version couvre 2021–2025 : variantes fournies pour les années absentes demandées dans le document.
Données de démonstration, pas de ventes réelles. Pas de calcul de marge faute de coûts.
"""
(root/"README.md").write_text(readme)
manifest={"objectif":"Résoudre les 26 exercices SQL Chinook du projet 5","sources":[{"url":"https://github.com/lerocha/chinook-database/blob/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql","blob_sha":"299610dc69f04a2b16b3a2e45bd2af82ed2872a2","sha256":hashlib.sha256((root/"data/Chinook_Sqlite.sql").read_bytes()).hexdigest()}],"stages":{"DataCollect":"completed","DataAnalyse":"completed","DataML":"skipped"},"raison_ml":"Rapports SQL descriptifs ; aucune cible prédictive requise.","exercices_executés":26,"variantes":4,"files":{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}}
(root/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
con.close()
with zipfile.ZipFile(root.parent/"Projet_Chinook_SQL_Complet.zip","w",zipfile.ZIP_DEFLATED) as z:
 for p in root.rglob("*"):
  if p.is_file():z.write(p,p.relative_to(root.parent))
print(json.dumps({"kpi":kpi,"tables":tables,"exercices":len(summary),"variantes":len(adapted),"archive":str(root.parent/"Projet_Chinook_SQL_Complet.zip")},ensure_ascii=False))

