"""Deterministic audit of a commit-pinned snapshot. Never execute project code."""
import hashlib
import base64
import json
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit


def validate_config(config):
    repo = config['repository']
    if len(repo.split('/')) != 2 or any(not p or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._' for c in p) for p in repo.split('/')):
        raise ValueError('Invalid repository identifier')
    seen = set()
    for p in config['projects']:
        rel = PurePosixPath(p['path'])
        if rel.is_absolute() or '..' in rel.parts or not rel.parts or str(rel) == '.' or '\\' in p['path']:
            raise ValueError('Unsafe project path')
        if p['id'] in seen:
            raise ValueError('Duplicate project id')
        seen.add(p['id'])
        url = urlsplit(p['site_url'])
        if url.scheme != 'https' or url.hostname != config['site_host'] or url.username or url.password or url.port not in (None,443):
            raise ValueError('Site URL must use the configured HTTPS host')
    return config


def blob_sha(content):
    data = content if isinstance(content, bytes) else content.encode('utf-8')
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def audit(config, snapshot, sites, local_observations=None):
    validate_config(config)
    if config['repository'] != snapshot['repository']:
        raise ValueError('Snapshot repository does not match configuration')
    if snapshot.get('schema_version') != 1:
        raise ValueError('Unsupported snapshot schema')
    files = {f['path']: f for f in snapshot['files']}
    docs = snapshot.get('documents', {})
    commit = snapshot['commit']
    report = {'schema_version':1, 'repository':snapshot['repository'], 'commit':commit,
              'collected_at':snapshot['collected_at'], 'dataset':'public portfolio observations, not synthetic scores',
              'projects':[], 'limitations':['Snapshot, not continuous monitoring', 'Presence of tests does not prove execution', 'HTTP reachability does not prove browser functionality or public visibility', 'No automatic publication or project code execution']}
    statuses = {'verified':0,'missing':0,'unknown':0,'attention':0}
    for project in config['projects']:
        prefix = project['path'] + '/'
        paths = sorted(p for p in files if p.startswith(prefix))
        base = f'https://github.com/{config["repository"]}/blob/{commit}/'
        findings = []
        def add(key, title, status, detail, evidence=None, action=''):
            findings.append({'key':key,'title':title,'status':status,'detail':detail,'evidence':evidence or [],'action':action})
            statuses[status] += 1
        def existence(key,title,candidates,action):
            present = [p for p in candidates if p in files]
            status = 'verified' if present else ('missing' if snapshot.get('tree_complete') else 'unknown')
            add(key,title,status,'Fichiers présents dans le commit audité.' if present else 'Absent du relevé complet.' if status=='missing' else 'Inventaire incomplet : absence non établie.',[{'url':base+p,'path':p,'blob_sha':files[p]['sha']} for p in present[:5]],'' if present else action)
        existence('readme','Documentation', [prefix+'README.md'], 'Ajouter un README avec installation, exemple et limites.')
        existence('code','Code Python', [p for p in paths if p.endswith('.py') and '/tests/' not in p], 'Publier les sources Python.')
        existence('dependencies','Environnement déclaré',[prefix+'requirements.txt',prefix+'pyproject.toml'], 'Déclarer les dépendances ou l’usage de la bibliothèque standard.')
        existence('tests','Tests présents',[p for p in paths if '/tests/' in p and Path(p).name.startswith('test') and p.endswith('.py')], 'Ajouter des tests ciblant les comportements essentiels.')
        # Treat a metadata file as a declaration, not independent proof of success.
        validation = project.get('validation_file')
        doc = docs.get(validation, {}) if validation else {}
        if doc and blob_sha(doc['content']) == files.get(validation,{}).get('sha'):
            try:
                result = json.loads(doc['content'])
                detail = f"Déclaration locale : {result.get('tests_passed','?')} tests ; code de sortie {result.get('exit_code','?')}. À distinguer d’une exécution observée par le Hub."
                add('local_result','Résultat local archivé','verified',detail,[{'url':base+validation,'path':validation,'blob_sha':doc['sha']}])
            except (ValueError,TypeError):
                add('local_result','Résultat local archivé','attention','Fichier de résultat illisible.',action='Corriger le JSON de validation.')
        else:
            add('local_result','Résultat local archivé','unknown','Aucun résultat local structuré configuré et vérifié.',action='Fournir un résultat daté et reproductible ; une affirmation dans le README ne suffit pas.')
        workflow = project.get('workflow')
        related = [r for r in snapshot.get('runs',[]) if workflow and r['path']==workflow and r['head_sha']==commit]
        if related:
            latest = max(related,key=lambda r:r['id'])
            status = 'verified' if latest['status']=='completed' and latest['conclusion']=='success' else 'attention' if latest['status']=='completed' else 'unknown'
            add('ci','Exécution CI attribuée',status,f"Workflow configuré : {latest['status']} / {latest.get('conclusion')}. L’attribution dépend du registre explicite du projet.",[{'url':latest['url'],'run_id':latest['id'],'commit':latest['head_sha']}],'Examiner le workflow et ses logs.' if status!='verified' else '')
        else:
            add('ci','Exécution CI attribuée','unknown','Aucun résultat du commit audité attribuable à ce projet. Les tests d’un autre projet ne sont pas transférés.',action='Configurer un workflow propre au projet et enregistrer son exécution.')
        site = next((s for s in sites if s['url']==project['site_url']),None)
        if not site or site.get('error'):
            add('site','Page du site','unknown','Vérification réseau indisponible ou non effectuée.',[{'url':project['site_url'],'error':site.get('error') if site else 'not_checked'}], 'Revérifier la page avec un accès réseau autorisé.')
        elif site.get('status') in (404,410):
            add('site','Page du site','missing',f"HTTP {site['status']} observé.",[site], 'Corriger la route ou publier la page.')
        elif site.get('truncated') or not site.get('marker_found') or site.get('status') != 200 or urlsplit(site.get('final_url','')).hostname != config['site_host']:
            add('site','Page du site','attention','Réponse reçue, mais la page attendue n’est pas confirmée.',[site], 'Inspecter la redirection, le statut et le titre de la page.')
        else:
            add('site','Page du site','verified','HTTP 200 et marqueur attendu présents ; interactions et visibilité publique non évaluées.',[site])
        local = (local_observations or {}).get(project['id'])
        if local:
            missing = sum(f['state']=='missing' for f in local['files'])
            mismatched = sum(f['state']=='different' for f in local['files'])
            add('local_sync','Concordance locale / GitHub','verified' if not missing and not mismatched else 'attention',f"{len(local['files'])} fichiers locaux comparés aux blobs GitHub ; {missing} absents, {mismatched} différents. Périmètre explicite, pas de miroir complet.",local['files'],'Examiner les différences avant publication.' if missing or mismatched else '')
        else:
            add('local_sync','Concordance locale / GitHub','unknown','Aucun dossier local fourni pour ce projet.',action='Fournir un checkout local pour comparer ses fichiers.')
        report['projects'].append({'id':project['id'],'title':project['title'],'file_count':len(paths),'findings':findings,'publication_ready':'review_required' if any(f['status']!='verified' for f in findings) else 'checks_verified'})
    report['summary'] = {'projects':len(report['projects']),'checks':sum(statuses.values()),**statuses}
    return report


def compare_local(root, prefix, files, documents=None):
    root=Path(root)
    if root.is_symlink() or not root.is_dir(): raise ValueError('Local root must be a real directory')
    result=[]
    for row in files:
        if not row['path'].startswith(prefix+'/'): continue
        rel=PurePosixPath(row['path'][len(prefix)+1:])
        if rel.is_absolute() or '..' in rel.parts: raise ValueError('Unsafe snapshot path')
        path=root.joinpath(*rel.parts)
        if any(p.is_symlink() for p in (root,*path.parents,path)): raise ValueError('Symlink refused')
        if not path.is_file(): result.append({'path':row['path'],'state':'missing','remote_blob':row['sha']});continue
        data=path.read_bytes()
        item={'path':row['path'],'state':'match' if blob_sha(data)==row['sha'] else 'different','sha256':hashlib.sha256(data).hexdigest(),'remote_blob':row['sha']}
        document=(documents or {}).get(row['path'])
        if item['state']=='different' and document and document.get('encoding')=='base64':
            remote=base64.b64decode(''.join(document['content'].split()),validate=True)
            if blob_sha(remote)==row['sha'] and data.replace(b'\r\n',b'\n')==remote.replace(b'\r\n',b'\n'):
                item['explanation']='Difference limited to CRLF/LF line endings; bytes remain different.'
        result.append(item)
    return {'files':result}
