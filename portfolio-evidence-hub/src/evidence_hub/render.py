"""Standalone report with browser-local filters and escaped evidence."""
import html
import json
from pathlib import Path
from urllib.parse import urlsplit
LABELS={'verified':'Vérifié','missing':'Manquant','unknown':'À vérifier','attention':'Attention'}


def render(report):
    esc=html.escape
    projects=[]
    for p in report['projects']:
        findings=[]
        for f in p['findings']:
            evidence=[]
            for e in f['evidence']:
                url=e.get('url','')
                if urlsplit(url).scheme=='https': evidence.append(f'<a href="{esc(url,quote=True)}" target="_blank" rel="noopener noreferrer">Ouvrir la source</a>')
                evidence.append('<pre>'+esc(json.dumps(e,ensure_ascii=False,indent=2))+'</pre>')
            findings.append(f'<article class="finding" data-status="{f["status"]}"><div class="line"><h3>{esc(f["title"])}</h3><span class="badge {f["status"]}">{LABELS[f["status"]]}</span></div><p>{esc(f["detail"])}</p>'+ (f'<p class="action">Prochain pas : {esc(f["action"])}</p>' if f['action'] else '')+'<details><summary>Examiner les preuves</summary>'+(''.join(evidence) or '<p>Aucune preuve suffisante collectée.</p>')+'</details></article>')
        projects.append(f'<section class="project" data-project="{esc(p["id"],quote=True)}"><div class="heading"><h2>{esc(p["title"])}</h2><span>{p["file_count"]} fichiers au commit audité</span></div>'+''.join(findings)+'</section>')
    options=''.join(f'<option value="{esc(p["id"],quote=True)}">{esc(p["title"])}</option>' for p in report['projects'])
    s=report['summary']
    return '''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Portfolio Evidence Hub | Junior BOOTO Waba</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f5f1;color:#183747;font:16px/1.6 system-ui}main{max-width:1120px;margin:auto;padding:36px 24px}header{background:#123c46;color:#fff;padding:36px;border-radius:22px}.eyebrow{color:#98dfcc;letter-spacing:.12em;font-size:13px}h1{font-size:clamp(32px,5vw,54px);line-height:1.1;margin:14px 0}h2{font-size:25px}h3{font-size:17px;margin:0}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:22px 0}.stat{background:white;border:1px solid #dbe3df;padding:20px;border-radius:14px}.stat b{font-size:32px;display:block}.controls{background:#fff;padding:18px;border-radius:14px;display:flex;gap:18px;flex-wrap:wrap}label{font-weight:650}select,input{display:block;padding:10px;font:inherit;border:1px solid #94aaa9;border-radius:6px;max-width:100%;margin-top:5px}.project{margin:28px 0}.heading,.line{display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap}.finding{background:#fff;padding:20px 24px;border:1px solid #dbe3df;border-radius:12px;margin:12px 0}.badge{padding:3px 10px;border-radius:20px;font-size:13px;font-weight:700}.verified{background:#def3e8;color:#17583f}.missing{background:#ffe7e4;color:#923829}.unknown{background:#edf0f3;color:#425968}.attention{background:#fff0cb;color:#745319}.action{border-left:3px solid #b98b28;padding-left:12px}pre{font:12px/1.6 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f6f5;padding:12px}summary{cursor:pointer;color:#176558}a{color:#176558}footer{color:#506673;border-top:1px solid #d4dedd;margin-top:30px;padding-top:20px}.notice{background:#fff8e7;padding:16px;border-radius:12px;margin:18px 0}[hidden]{display:none!important}@media(max-width:620px){.stats{grid-template-columns:1fr 1fr}header{padding:24px}main{padding:20px 14px}.controls>*{width:100%}}
</style></head><body><main><header><span class="eyebrow">JUNIOR BOOTO WABA · PYTHON / AUTOMATISATION</span><h1>Portfolio Evidence Hub</h1><p>Chaque constat relié à une preuve. Chaque incertitude visible.</p></header>'''+f'<div class="stats"><div class="stat"><b>{s["projects"]}</b>projets audités</div><div class="stat"><b>{s["verified"]}</b>contrôles vérifiés</div><div class="stat"><b>{s["unknown"]}</b>contrôles à vérifier</div><div class="stat"><b>{s["attention"]+s["missing"]}</b>points signalés</div></div><p>Collecte : {esc(report["collected_at"])} · commit <code>{esc(report["commit"])}</code></p>'+'''<p class="notice">« Vérifié » décrit le contrôle affiché : un fichier de tests présent n'est pas une exécution réussie. Ce rapport ne mesure ni l'expertise de l'auteur ni la qualité scientifique des projets.</p><div class="controls"><label>Projet<select id="project"><option value="all">Tous les projets</option>'''+options+'''</select></label><label>État<select id="status"><option value="all">Tous les états</option><option value="verified">Vérifié</option><option value="unknown">À vérifier</option><option value="attention">Attention</option><option value="missing">Manquant</option></select></label><label>Rechercher<input id="search" type="search" placeholder="Documentation, CI, site…"></label></div><p id="count" role="status" aria-live="polite"></p>'''+''.join(projects)+'''<footer><p>Lecture seule. Filtres exécutés dans votre navigateur ; l'audit Python n'est pas relancé par cette page.</p><p>Instantané daté, pas de surveillance continue. Pas de publication automatique, de notifications envoyées ou de Drive connecté. Le statut HTTP ne remplace pas une vérification visuelle et d'accès public.</p><p lang="en">Evidence-based portfolio audit: commit-pinned files, explicitly attributed CI results and dated link observations. Missing evidence remains unknown. No proficiency score or automatic publishing.</p></footer></main><script>
function filter(){const selected=document.getElementById('project').value,status=document.getElementById('status').value,q=document.getElementById('search').value.toLocaleLowerCase();let shown=0;document.querySelectorAll('.project').forEach(p=>{let count=0;p.querySelectorAll('.finding').forEach(f=>{const visible=(selected==='all'||p.dataset.project===selected)&&(status==='all'||f.dataset.status===status)&&f.textContent.toLocaleLowerCase().includes(q);f.hidden=!visible;if(visible){count++;shown++;}});p.hidden=count===0;});document.getElementById('count').textContent=shown+' contrôles affichés';}
['project','status','search'].forEach(id=>document.getElementById(id).addEventListener('input',filter));filter();
</script></body></html>'''


def export(report, directory):
    out=Path(directory);out.mkdir(parents=True,exist_ok=True)
    (out/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'dashboard.html').write_text(render(report),encoding='utf-8')
    actions=['# Prochaines actions — Portfolio Evidence Hub','']
    for p in report['projects']:
        actions.extend(['## '+p['title'],''])
        actions.extend('- '+f['title']+' : '+f['action'] for f in p['findings'] if f['action'])
        actions.append('')
    (out/'next-actions.md').write_text('\n'.join(actions),encoding='utf-8')
