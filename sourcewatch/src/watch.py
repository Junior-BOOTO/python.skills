"""SourceWatch: collecte RSS bornée, métadonnées et comparaison de snapshots."""
from pathlib import Path
from datetime import datetime,timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
from urllib.request import Request,build_opener,HTTPRedirectHandler
import argparse,csv,hashlib,html,ipaddress,json,re,socket
import xml.etree.ElementTree as ET

FEED='https://blog.python.org/feeds/posts/default?alt=rss'
KEYWORDS={'python':('python','pypi','cpython'),'ia':('artificial intelligence','machine learning','llm'),'education':('education','teaching','learning','school')}

def canonical(url):
    p=urlsplit(url.strip())
    if p.scheme not in ('http','https') or not p.hostname or p.username or p.password:
        raise ValueError('URL publique HTTP(S) requise')
    host=p.hostname.lower()
    if host=='localhost' or host.endswith(('.local','.localhost')):raise ValueError('Hôte local interdit')
    try:
        if not ipaddress.ip_address(host).is_global:raise ValueError('IP non publique interdite')
    except ValueError as exc:
        if 'interdite' in str(exc):raise
    query=[(k,v) for k,v in parse_qsl(p.query,keep_blank_values=True) if not k.lower().startswith('utm_') and k.lower() not in ('fbclid','gclid')]
    port=p.port
    netloc=('['+host+']' if ':' in host else host)+(':'+str(port) if port and not ((port==443 and p.scheme=='https') or (port==80 and p.scheme=='http')) else '')
    return urlunsplit((p.scheme.lower(),netloc,p.path or '/',urlencode(query),''))

def published(value):
    if not value:return None
    try:
        d=parsedate_to_datetime(value)
        if not d.tzinfo:raise ValueError('Fuseau absent')
        return d.astimezone(timezone.utc).isoformat()
    except (TypeError,ValueError):raise ValueError('Date de publication invalide')

def relevance(title):
    t=title.casefold();matches=[]
    for group,words in KEYWORDS.items():
        for word in words:
            if re.search(r'(?<!\w)'+re.escape(word)+r'(?!\w)',t):matches.append(group+': '+word)
    return matches

def parse_rss(data,source,collected,limit=20):
    if not 1<=limit<=100:raise ValueError('Limite entre 1 et 100')
    if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():raise ValueError('DTD et entités externes non acceptées')
    root=ET.fromstring(data)
    if root.tag!='rss':raise ValueError('RSS 2 requis dans cette version')
    items=root.findall('./channel/item')
    if root.find('channel') is None:raise ValueError('Channel RSS absent')
    rows,errors=[],[]
    for i,item in enumerate(items[:limit],1):
        try:
            title=html.unescape((item.findtext('title') or '').strip())
            url=canonical(item.findtext('link') or '')
            if not title:raise ValueError('Titre absent')
            guid=(item.findtext('guid') or '').strip() or url
            pub=published(item.findtext('pubDate'))
            key=hashlib.sha256((source+'\n'+guid).encode()).hexdigest()
            row={'key':key,'source':source,'guid':guid,'title':title,'url':url,'published_at_utc':pub,'collected_at_utc':collected,'relevance_reasons':relevance(title)}
            row['metadata_sha256']=hashlib.sha256(json.dumps({k:row[k] for k in ['title','url','published_at_utc']},sort_keys=True).encode()).hexdigest()
            rows.append(row)
        except (ValueError,TypeError) as exc:errors.append({'position':i,'error':str(exc)})
    return rows,errors,{'available_in_feed':len(items),'examined':min(len(items),limit),'limit':limit,'complete_feed_examined':len(items)<=limit}

def dedupe(rows):
    groups={}
    for row in rows:groups.setdefault(row['url'],[]).append(row)
    return [{'url':url,'observations':group,'titles':sorted({r['title'] for r in group}),'source_count':len({r['source'] for r in group})} for url,group in sorted(groups.items())]

def compare(old,new):
    def index(rows):
        d={}
        for r in rows:
            if r['key'] in d:raise ValueError('Identifiant répété : comparaison ambiguë')
            d[r['key']]=r
        return d
    a,b=index(old),index(new)
    changes=[]
    for k,r in b.items():
        status='new' if k not in a else ('changed' if r['metadata_sha256']!=a[k]['metadata_sha256'] else 'unchanged')
        fields=[f for f in ['title','url','published_at_utc'] if k in a and a[k][f]!=r[f]]
        changes.append({'key':k,'status':status,'title':r['title'],'fields':fields})
    for k,r in a.items():
        if k not in b:changes.append({'key':k,'status':'absent_from_snapshot','title':r['title'],'fields':[]})
    return changes

class RestrictedRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if urlsplit(newurl).scheme!='https' or urlsplit(newurl).hostname!='blog.python.org':raise ValueError('Redirection hors source refusée')
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def fetch():
    # Source fixe : pas d'URL arbitraire à télécharger, ni visite des liens d'articles.
    request=Request(FEED,headers={'User-Agent':'SourceWatch-Portfolio/1.0'})
    with build_opener(RestrictedRedirect()).open(request,timeout=20) as r:
        content_type=r.headers.get('Content-Type','')
        if not any(t in content_type.lower() for t in ['xml','rss','application/octet-stream']):raise ValueError('Réponse non XML/RSS')
        data=r.read(2_000_001)
        if len(data)>2_000_000:raise ValueError('Flux trop volumineux')
        return data,{'http_status':r.status,'content_type':content_type,'response_sha256':hashlib.sha256(data).hexdigest()}

def report(snapshot,changes=None):
    e=html.escape;rows=''
    mode='Collecte réelle' if snapshot['network']['mode']=='live' else 'Relecture hors ligne (fixtures fictives ou cache documenté)'
    for r in snapshot['records']:
        values=[r['title'],r['published_at_utc'] or 'Date absente',r['collected_at_utc'],', '.join(r['relevance_reasons']) or 'Aucun mot-clé ciblé']
        rows+='<tr>'+''.join('<td>'+e(v)+'</td>' for v in values)+'<td><a target="_blank" rel="noopener noreferrer" href="'+e(r['url'],quote=True)+'">Source ↗</a></td></tr>'
    diff=''
    if changes:
        diff='<h2>Comparaison de fixtures fictives</h2><p>Ces changements sont injectés pour tester le mécanisme ; ils ne sont pas des modifications observées du flux réel.</p><ul>'+''.join('<li>'+e(c['status']+' : '+c['title']+' ('+', '.join(c['fields'])+')')+'</li>' for c in changes)+'</ul>'
    return '''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SourceWatch — veille documentée</title><style>body{font:16px system-ui;color:#153246;background:#f4f7fa;margin:0}main{max-width:1200px;margin:auto;padding:35px 20px}h1{font-size:clamp(2rem,5vw,3.5rem)}input{padding:14px;border:1px solid #bccdd5;border-radius:8px;width:min(90%,550px)}table{border-collapse:collapse;background:white;width:100%}th,td{padding:13px;text-align:left;border-bottom:1px solid #dde5ea}a{color:#23686f}.scroll{overflow:auto}li{margin:12px 0}</style><main><p>JUNIOR BOOTO · PYTHON & DONNÉES</p><h1>Des actualités, avec leurs preuves.</h1><p>'''+e(mode)+''' : '''+str(len(snapshot['records']))+''' entrées. Métadonnées seulement : aucun corps d’article republié. Les mots-clés du titre expliquent le classement, sans évaluer la fiabilité.</p><label for="search">Rechercher dans les métadonnées</label><p><input id="search" type="search" placeholder="python, sécurité, titre…"></p><p id="count" aria-live="polite"></p><div class="scroll"><table><thead><tr><th>Titre</th><th>Publication UTC</th><th>Collecte UTC</th><th>Motifs</th><th>Lien</th></tr></thead><tbody>'''+rows+'''</tbody></table></div>'''+diff+'''<p>Absent d’un snapshot ne signifie pas supprimé : le flux peut être limité ou avoir changé de fenêtre. Cette page affiche un état enregistré ; aucune veille permanente n’est installée.</p><script>const input=document.getElementById('search'),rows=[...document.querySelectorAll('tbody tr')],count=document.getElementById('count');function filter(){let n=0;rows.forEach(r=>{r.hidden=!r.textContent.toLocaleLowerCase().includes(input.value.toLocaleLowerCase());if(!r.hidden)n++;});count.textContent=n+' résultat(s) visible(s)';}input.oninput=filter;filter();</script></main></html>'''

def run(out,limit=20,offline=None,previous=None):
    out=Path(out)
    if out.exists() and any(out.iterdir()):raise ValueError('Sortie non vide : préserver les anciennes collectes')
    out.mkdir(parents=True,exist_ok=True)
    timestamp=datetime.now(timezone.utc).isoformat()
    meta={'mode':'offline' if offline else 'live','source_url':FEED}
    try:
        if offline:
            data=Path(offline).read_bytes()
            if len(data)>2_000_000:raise ValueError('Flux trop volumineux')
            meta['response_sha256']=hashlib.sha256(data).hexdigest()
        else:data,m=fetch();meta.update(m)
        records,errors,coverage=parse_rss(data,FEED,timestamp,limit)
        snapshot={'source':FEED,'collected_at_utc':timestamp,'records':records,'errors':errors,'coverage':coverage,'network':meta}
        changes=compare(json.loads(Path(previous).read_text())['records'],records) if previous else None
        (out/'snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2))
        (out/'groups.json').write_text(json.dumps(dedupe(records),ensure_ascii=False,indent=2))
        if changes is not None:(out/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
        (out/'report.html').write_text(report(snapshot))
        (out/'manifest.json').write_text(json.dumps({'status':'completed','quality_review_required':bool(errors),'network':meta,'coverage':coverage,'record_count':len(records),'errors':errors,'artifacts':['snapshot.json','groups.json','report.html'],'scope':'Métadonnées, flux unique, pas contenu complet ni exécution permanente'},ensure_ascii=False,indent=2))
        return snapshot
    except Exception as exc:
        (out/'manifest.json').write_text(json.dumps({'status':'blocked','error':str(exc),'network':meta},ensure_ascii=False,indent=2));raise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--limit',type=int,default=20);p.add_argument('--offline');p.add_argument('--previous');a=p.parse_args();s=run(a.out,a.limit,a.offline,a.previous);print(json.dumps({'records':len(s['records']),'errors':s['errors'],'coverage':s['coverage']},indent=2))
