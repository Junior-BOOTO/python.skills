"""Auditable local file inventory and copy-only organization. Python 3.10+."""
from __future__ import annotations
import csv
import hashlib
import html
import json
import os
from pathlib import Path
import stat

DEFAULT_CATEGORIES = {
    'documents': ['.pdf', '.docx', '.txt', '.md'],
    'presentations': ['.pptx', '.odp'],
    'data': ['.csv', '.xlsx', '.json'],
    'code': ['.py', '.ipynb', '.r'],
    'images': ['.png', '.jpg', '.jpeg', '.svg'],
    'media': ['.mp3', '.wav', '.mp4'],
}


def validate_categories(categories):
    extensions = set()
    for name, suffixes in categories.items():
        if not name or name in ('.', '..') or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789_-' for c in name):
            raise ValueError('Category must be a lowercase directory name')
        if not isinstance(suffixes, list):
            raise ValueError('Suffixes must be a list')
        for suffix in suffixes:
            if not isinstance(suffix, str) or not suffix.startswith('.') or suffix != suffix.lower() or suffix in extensions:
                raise ValueError('Invalid or repeated extension')
            extensions.add(suffix)
    return categories


def safe_path(root, relative):
    """Reject traversal and symlinks in every existing path component."""
    root = Path(root).absolute()
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts:
        raise ValueError('Unsafe relative path')
    target = root / rel
    for part in (root, *root.parents, *target.parents, target):
        if part.is_symlink():
            raise ValueError('Symbolic link refused')
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path outside root')
    return target


def digest(path):
    """Stream regular files and reject changes during reading."""
    path = Path(path)
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError('Not a regular file')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    with os.fdopen(os.open(path, flags), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
            raise ValueError('File changed before reading')
        value = hashlib.sha256()
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
        after = os.fstat(stream.fileno())
    if (opened.st_size, opened.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError('File changed during reading')
    return value.hexdigest(), after.st_size


def scan(root, categories=None):
    categories = validate_categories(categories or DEFAULT_CATEGORIES)
    root = Path(root).absolute()
    if any(p.is_symlink() for p in (root, *root.parents)) or not root.is_dir():
        raise ValueError('Source must be a real directory without symlink ancestors')
    files, errors, skipped = [], [], []
    def walk_error(exc):
        errors.append({'path': str(Path(exc.filename).relative_to(root)), 'error': str(exc)})
    for folder, dirs, names in os.walk(root, followlinks=False, onerror=walk_error):
        for name in sorted(dirs[:]):
            path = Path(folder) / name
            if path.is_symlink():
                skipped.append({'path': path.relative_to(root).as_posix(), 'reason': 'symlink'})
                dirs.remove(name)
        dirs.sort()
        for name in sorted(names):
            path = Path(folder) / name
            relative = path.relative_to(root).as_posix()
            try:
                path = safe_path(root, relative)
                if not stat.S_ISREG(path.lstat().st_mode):
                    skipped.append({'path': relative, 'reason': 'not_regular'})
                    continue
                sha, size = digest(path)
                category = next((key for key, suffixes in categories.items() if path.suffix.lower() in suffixes), 'other')
                # Preserve the full source-relative path: two same-name files never collide.
                files.append({'path': relative, 'size': size, 'sha256': sha,
                              'category': category, 'destination': f'{category}/{relative}'})
            except (OSError, ValueError) as exc:
                errors.append({'path': relative, 'error': str(exc)})
    files.sort(key=lambda row: row['path'])
    groups = {}
    names = {}
    for item in files:
        groups.setdefault(item['sha256'], []).append(item)
        names.setdefault(Path(item['path']).name.casefold(), []).append(item)
    duplicates = [{'sha256': key, 'paths': [i['path'] for i in rows],
                   'redundant_bytes': rows[0]['size'] * (len(rows) - 1)}
                  for key, rows in sorted(groups.items()) if len(rows) > 1]
    collisions = [[i['path'] for i in rows] for _, rows in sorted(names.items())
                  if len(rows) > 1 and len({i['sha256'] for i in rows}) > 1]
    return {'schema_version': 1, 'mode': 'simulation', 'files': files,
            'duplicates': duplicates, 'name_collisions': collisions,
            'errors': errors, 'skipped': skipped,
            'summary': {'files': len(files), 'bytes': sum(i['size'] for i in files),
                        'duplicate_groups': len(duplicates),
                        'redundant_bytes': sum(i['redundant_bytes'] for i in duplicates)}}


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    os.replace(temporary, path)


def export_report(plan, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / 'plan.json', plan)
    with (output / 'inventory.csv').open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=['path', 'size', 'sha256', 'category', 'destination'])
        writer.writeheader()
        for row in plan['files']:
            # Protect text cells from formula interpretation in spreadsheets.
            writer.writerow({k: ("'" + v if isinstance(v, str) and v.startswith(('=', '+', '-', '@', '\t', '\r')) else v) for k, v in row.items()})
    escape = html.escape
    rows = ''.join(f'<tr><td>{escape(i["path"])}</td><td>{i["size"]}</td><td>{escape(i["category"])}</td><td>{escape(i["destination"])}</td></tr>' for i in plan['files'])
    groups = ''.join('<li>' + ' · '.join(escape(p) for p in g['paths']) + '</li>' for g in plan['duplicates'])
    alerts = escape(json.dumps({'errors': plan['errors'], 'skipped': plan['skipped'], 'name_collisions': plan['name_collisions']}, ensure_ascii=False, indent=2))
    s = plan['summary']
    page = f'''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Portfolio File Guardian — rapport</title>
<style>body{{margin:0;background:#f3f6fc;color:#182944;font:16px system-ui}}main{{max-width:1120px;margin:auto;padding:38px 24px}}header{{background:#132b4a;color:white;padding:30px;border-radius:18px}}.tag{{color:#79e1d5}}.stats{{display:flex;gap:14px;flex-wrap:wrap;margin:24px 0}}.card{{background:white;padding:22px;border-radius:14px;flex:1;min-width:160px}}b{{font-size:30px;display:block}}table{{width:100%;border-collapse:collapse;background:white}}td,th{{padding:13px;text-align:left;border-bottom:1px solid #dde4ef;overflow-wrap:anywhere}}.table{{overflow-x:auto}}pre{{white-space:pre-wrap;background:white;padding:20px}}footer{{margin-top:25px;color:#52647c}}</style>
<main><header><span class="tag">PYTHON / AUTOMATISATION · SIMULATION</span><h1>Portfolio File Guardian</h1><p>Inventorier, comprendre les doublons et préparer une organisation sans toucher aux originaux.</p></header>
<section class="stats"><div class="card"><b>{s['files']}</b>fichiers analysés</div><div class="card"><b>{s['duplicate_groups']}</b>groupes de doublons</div><div class="card"><b>{s['redundant_bytes']}</b>octets redondants théoriques</div></section>
<p>SHA-256 identifie les contenus identiques. Aucun fichier supprimé. La redondance ne représente pas une mesure d'espace disque libérable.</p><h2>Doublons exacts</h2><ul>{groups or '<li>Aucun doublon détecté.</li>'}</ul><h2>Plan de copie</h2><div class="table"><table><thead><tr><th>Source</th><th>Octets</th><th>Catégorie</th><th>Destination proposée</th></tr></thead><tbody>{rows}</tbody></table></div><h2>Collisions, exclusions et erreurs</h2><pre>{alerts}</pre><footer>Junior BOOTO Waba · Prototype de portfolio · Rapport généré par Python, sans service externe.</footer></main></html>'''
    (output / 'report.html').write_text(page, encoding='utf-8')


def organize(source, destination, categories=None):
    """Copy files into a new directory; originals and duplicate copies are retained."""
    source, destination = Path(source).absolute(), Path(destination).absolute()
    if any(p.is_symlink() for p in (destination, *destination.parents)):
        raise ValueError('Symlink destination refused')
    if destination.exists():
        raise ValueError('Destination must not exist; refusing overwrite')
    if destination.resolve().is_relative_to(source.resolve()) or source.resolve().is_relative_to(destination.resolve()):
        raise ValueError('Source and destination must be disjoint')
    plan = scan(source, categories)
    if plan['errors']:
        raise ValueError('Scan contains errors; copy refused')
    destination.mkdir(parents=True, exist_ok=False)
    journal = {'schema_version': 1, 'mode': 'copy', 'status': 'running', 'created': []}
    write_json(destination / 'guardian-journal.json', journal)
    try:
        for item in plan['files']:
            src = safe_path(source, item['path'])
            target = safe_path(destination, item['destination'])
            target.parent.mkdir(parents=True, exist_ok=True)
            # Persist intent first; an interrupted partial copy stays visible in the journal.
            entry = {'path': item['destination'], 'sha256': item['sha256'], 'status': 'pending'}
            journal['created'].append(entry)
            write_json(destination / 'guardian-journal.json', journal)
            sha = hashlib.sha256()
            flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
            with os.fdopen(os.open(src, flags), 'rb') as incoming, target.open('xb') as outgoing:
                if not stat.S_ISREG(os.fstat(incoming.fileno()).st_mode):
                    raise ValueError('Non-regular source')
                for block in iter(lambda: incoming.read(1024 * 1024), b''):
                    outgoing.write(block)
                    sha.update(block)
            if sha.hexdigest() != item['sha256'] or digest(target)[0] != item['sha256']:
                target.unlink()
                raise ValueError('Source changed or copy failed verification')
            entry['status'] = 'verified'
            write_json(destination / 'guardian-journal.json', journal)
        journal['status'] = 'completed'
    except Exception:
        journal['status'] = 'failed'
        raise
    finally:
        write_json(destination / 'guardian-journal.json', journal)
    return journal


def restore(destination, execute=False):
    """Remove only journaled, unchanged copies. Preview is the default."""
    destination = Path(destination).absolute()
    journal_path = safe_path(destination, 'guardian-journal.json')
    journal = json.loads(journal_path.read_text(encoding='utf-8'))
    if journal.get('schema_version') != 1 or journal.get('mode') != 'copy':
        raise ValueError('Invalid journal')
    pending = []
    for item in journal['created']:
        target = safe_path(destination, item['path'])
        if not target.exists():
            continue
        if digest(target)[0] != item['sha256']:
            raise ValueError(f'Modified copy preserved: {item["path"]}')
        pending.append((target, item['sha256']))
    if execute:
        for target, sha in pending:
            if digest(target)[0] != sha:
                raise ValueError('Copy changed during restoration')
            target.unlink()
        journal['status'] = 'restored'
        write_json(journal_path, journal)
    return {'mode': 'restore' if execute else 'simulation', 'paths': [p.relative_to(destination).as_posix() for p, _ in pending]}
