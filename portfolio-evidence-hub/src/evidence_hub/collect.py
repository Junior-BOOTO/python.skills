"""Read-only API collector. Fixed GitHub host and configured HTTPS site host."""
import base64
import datetime
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from .audit import validate_config


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args):
        return None


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def get(url, token=None, limit=8_000_000):
    parts=urllib.parse.urlsplit(url)
    if parts.scheme!='https' or parts.username or parts.password: raise ValueError('HTTPS URL required')
    headers={'User-Agent':'Portfolio-Evidence-Hub/1.0','Accept':'application/vnd.github+json' if parts.hostname=='api.github.com' else 'text/html'}
    if token and parts.hostname=='api.github.com': headers['Authorization']='Bearer '+token
    request=urllib.request.Request(url,headers=headers)
    with urllib.request.build_opener(NoRedirect()).open(request,timeout=15) as response:
        data=response.read(limit+1)
        if len(data)>limit: raise ValueError('Response exceeds configured size limit')
        return data,response.status,response.url


def collect(config):
    validate_config(config)
    repo=config['repository']; token=os.environ.get('GITHUB_TOKEN'); api='https://api.github.com/repos/'+repo
    def fetch(url): return json.loads(get(url,token)[0])
    # The head commit is resolved once, then every file is read at this SHA.
    metadata=fetch(api)
    head=fetch(api+'/git/ref/heads/'+urllib.parse.quote(metadata['default_branch'],safe=''))['object']['sha']
    commit=fetch(api+'/git/commits/'+head)
    tree=fetch(commit['tree']['url']+'?recursive=1')
    prefixes=[p['path']+'/' for p in config['projects']]
    files=[{k:f[k] for k in ('path','sha','size') if k in f} for f in tree['tree'] if f['type']=='blob' and any(f['path'].startswith(p) for p in prefixes)]
    docs={};errors=[]
    wanted={p['path']+'/'+name for p in config['projects'] for name in ('README.md','requirements.txt','pyproject.toml')}
    wanted.update(p[k] for p in config['projects'] for k in ('validation_file','workflow') if k in p)
    for path in sorted(wanted):
        if path not in {f['path'] for f in files} and not path.startswith('.github/'):continue
        try:
            obj=fetch(api+'/contents/'+urllib.parse.quote(path,safe='/')+'?ref='+head)
            if obj.get('encoding')!='base64':raise ValueError('Expected a base64 UTF-8 file')
            docs[path]={'content':base64.b64decode(obj['content']).decode('utf-8'),'sha':obj['sha']}
        except (OSError,ValueError,KeyError) as exc:
            errors.append({'path':path,'error':type(exc).__name__,'http_status':getattr(exc,'code',None)})
    runs=[];complete=False
    try:
        for page in range(1,11):
            payload=fetch(api+'/actions/runs?head_sha='+head+'&per_page=100&page='+str(page))
            batch=payload['workflow_runs'];runs.extend({k:r[k] for k in ('id','path','head_sha','status','conclusion','html_url')} for r in batch)
            if len(runs)>=payload['total_count'] or not batch:complete=len(runs)>=payload['total_count'];break
    except (OSError,ValueError,KeyError) as exc:
        errors.append({'source':'actions','error':type(exc).__name__,'http_status':getattr(exc,'code',None)})
    for r in runs:r['url']=r.pop('html_url')
    snapshot={'schema_version':1,'repository':repo,'commit':head,'collected_at':now(),'tree_complete':not tree.get('truncated',True),'files':files,'documents':docs,'runs':runs,'runs_complete':complete,'collection_errors':errors}
    return snapshot,collect_sites(config)


def collect_sites(config):
    validate_config(config);observations=[]
    for project in config['projects']:
        item={'url':project['site_url'],'checked_at':now()}
        try:
            body,status,final=get(project['site_url'],limit=2_000_000)
            item.update(status=status,final_url=final,marker_found=project['site_marker'].casefold() in body.decode('utf-8',errors='replace').casefold(),body_sha256=hashlib.sha256(body).hexdigest(),truncated=False)
        except urllib.error.HTTPError as exc:
            item.update(status=exc.code,error=None if exc.code in (404,410) else 'HTTPError',marker_found=False,final_url=project['site_url'])
        except (OSError,ValueError) as exc:
            item['error']=type(exc).__name__
        observations.append(item)
    return observations
