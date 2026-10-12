from pathlib import Path
import sqlite3,json,csv,math
ROOT=Path(__file__).resolve().parent
def main():
    db=sqlite3.connect(ROOT/'collected'/'AdventureWorks_commercial.sqlite')
    (ROOT/'analysis').mkdir(exist_ok=True)
    queries=json.loads((ROOT/'requetes.json').read_text());guide=['# Guide des exercices — AdventureWorks\n','SQLite, adaptation commerciale des données officielles Microsoft. Tous les montants sont en UM.\n']
    summaries=[]
    for q in queries:
        guide += [f"## {q['id']}. {q['title']}\n",q['note']+'\n','```sql\n'+q['sql']+'\n```\n']
        if q['status']=='not_computable':
            summaries.append({**q,'rows':None,'columns':[],'preview':[]});guide.append('Statut : non calculable ; données de retours manquantes.\n');continue
        cursor=db.execute(q['sql']);rows=cursor.fetchall();names=[c[0] for c in cursor.description]
        with (ROOT/'analysis'/f"exercice_{q['id']:02}.csv").open('w',newline='',encoding='utf-8') as f:
            w=csv.writer(f);w.writerow(names);w.writerows(rows)
        summaries.append({**q,'rows':len(rows),'columns':names,'preview':rows[:5]})
        guide += [f"Résultat exécuté : {len(rows)} lignes. Aperçu (au plus cinq lignes) :\n",'| '+' | '.join(names)+' |','| '+' | '.join('---' for x in names)+' |']
        guide += ['| '+' | '.join('NULL' if v is None else str(v).replace('|','\\|') for v in row)+' |' for row in rows[:5]]
        guide.append('')
    total=db.execute('SELECT SUM(Revenu) FROM v_ventes').fetchone()[0]
    for dimension in ['Territoire','Categorie','SegmentClient']:
        result=db.execute('SELECT SUM(x) FROM (SELECT SUM(Revenu) x FROM v_ventes GROUP BY '+dimension+')').fetchone()[0]
        assert math.isclose(result,total,abs_tol=.001)
    monthly=db.execute(queries[15]['sql']).fetchall()
    assert abs(monthly[-1][2]-total)<.01
    assert monthly[0][4]==1 and monthly[1][4]==2 and all(r[4]==3 for r in monthly[2:])
    products=db.execute(queries[11]['sql']).fetchall()
    assert len(products)%12==0
    from collections import Counter
    assert set(Counter(r[0] for r in products).values())=={12}
    # Sommes après arrondi à 2 décimales comparées avec la tolérance de somme des arrondis.
    start=products[0][2]
    exact=db.execute('SELECT SUM(Revenu) FROM v_ventes WHERE date(OrderDate)>=?',(start,)).fetchone()[0]
    assert abs(sum(r[3] for r in products)-exact)<=len(products)*.005+.01
    (ROOT/'reports'/'guide_exercices.md').write_text('\n'.join(guide))
    (ROOT/'reports'/'apercus.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2))
    summary={'executed_analyses':sum(q['status']=='computed' for q in queries),'original_exercises_computed':14,'not_computable':[14],'bonus_computed':3,'monthly_rows':len(monthly),'checks':['Réconciliation par dimension','Cumul final = revenu total','Moyenne mobile sur calendrier dense','12 lignes par produit dans exercice 12'],'sqlite_version':sqlite3.sqlite_version}
    (ROOT/'reports'/'execution.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));db.close();print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
