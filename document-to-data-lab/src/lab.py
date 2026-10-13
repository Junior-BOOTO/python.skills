"""Document-to-Data Lab: extraction locale et contrôles traçables."""
from pathlib import Path
from datetime import date
from decimal import Decimal, InvalidOperation
import argparse, csv, hashlib, html, io, json, re
import pdfplumber

FIELDS = ['id', 'date', 'description', 'amount', 'currency']
ALIASES = {'identifiant':'id', 'montant':'amount', 'devise':'currency', 'libelle':'description'}

def header(value):
    return ALIASES.get(str(value or '').strip().lower(), str(value or '').strip().lower())

def amount(value):
    """Montant monétaire à deux décimales, sans ambiguïté des séparateurs."""
    s = str(value).strip()
    if not re.fullmatch(r'-?\d+(?:[.,]\d{1,2})?', s):
        raise ValueError('Montant absent ou ambigu : utiliser 1250.50 ou 1250,50')
    try:
        n = Decimal(s.replace(',', '.'))
    except InvalidOperation as exc:
        raise ValueError('Montant invalide') from exc
    if n < 0:
        raise ValueError('Montant négatif hors contrat dépenses')
    return n.quantize(Decimal('0.01'))

def extract(path):
    """Retourne lignes brutes, repères PDF/CSV et éventuels totaux déclarés."""
    records, totals = [], []
    if path.suffix.lower() == '.csv':
        text = path.read_text(encoding='utf-8-sig')
        first = text.splitlines()[0] if text.splitlines() else ''
        delim = ';' if first.count(';') > first.count(',') else ','
        reader = csv.reader(io.StringIO(text), delimiter=delim)
        matrix = list(reader)
        tables = [(None, 1, matrix)]
    elif path.suffix.lower() == '.pdf':
        tables = []
        with pdfplumber.open(path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                for table_num, matrix in enumerate(page.extract_tables(), 1):
                    tables.append((page_num, table_num, matrix))
                for currency, value in re.findall(r'TOTAL\s+(USD|COP):\s*([0-9]+(?:[.,][0-9]{1,2})?)', page.extract_text() or ''):
                    totals.append({'page': page_num, 'currency': currency, 'amount': str(amount(value))})
        if not tables:
            raise ValueError('Aucun tableau détecté. OCR non implémenté ; vérifier le document.')
    else:
        raise ValueError('Format non pris en charge : PDF texte ou CSV UTF-8 requis')
    if not tables or not tables[0][2]:
        raise ValueError('Document vide')
    for page, table, matrix in tables:
        columns = [header(v) for v in matrix[0]]
        if len(columns) != len(set(columns)) or not set(FIELDS) <= set(columns):
            raise ValueError('Schéma incompatible : id, date, description, amount, currency requis')
        for line_num, values in enumerate(matrix[1:], 2):
            if not any(str(v or '').strip() for v in values):
                continue
            raw = dict(zip(columns, values))
            records.append({'raw': raw, 'source_page': page, 'source_table': table,
                            'source_row': line_num, 'row_width_valid': len(values) == len(columns)})
    return records, totals

def validate(record, allowed=('USD','COP')):
    raw = record['raw']
    errors = []
    if not record['row_width_valid']:
        errors.append('row_width')
    normalized = {k: str(raw.get(k) or '').strip() for k in FIELDS}
    for k in FIELDS:
        if not normalized[k]: errors.append('missing_'+k)
    try:
        parsed = date.fromisoformat(normalized['date'])
        if parsed.isoformat() != normalized['date']: raise ValueError()
    except ValueError:
        errors.append('invalid_date')
    try:
        normalized['amount'] = str(amount(normalized['amount']))
    except ValueError:
        errors.append('invalid_amount')
    normalized['currency'] = normalized['currency'].upper()
    if normalized['currency'] not in allowed: errors.append('unsupported_currency')
    return normalized, sorted(set(errors))

def csv_safe(value):
    s = str(value if value is not None else '')
    return "'"+s if s.lstrip().startswith(('=', '+', '-', '@', '\t', '\r')) else s

def write_csv(path, rows, columns):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        w.writeheader()
        for row in rows: w.writerow({k: csv_safe(row.get(k)) for k in columns})

def render(report, rows):
    esc = html.escape
    cards = ''.join(f'<div class="metric"><strong>{v}</strong>{esc(k)}</div>' for k,v in [('Lignes extraites',report['extracted']),('Lignes acceptées',report['accepted']),('Lignes à revoir',report['review']),('Documents bloqués',report['blocked_documents'])])
    body = ''
    for row in rows:
        values=[row.get('id',''),row.get('date',''),row.get('amount',''),row.get('currency',''),row['status'],', '.join(row['issues']),row['source_file'],str(row['source_page'] or 'CSV'),str(row['source_row'])]
        body += '<tr>'+''.join('<td>'+esc(str(v))+'</td>' for v in values)+'</tr>'
    findings=''.join('<li>'+esc(json.dumps(x,ensure_ascii=False))+'</li>' for x in report['file_issues']) or '<li>Aucun incident de document</li>'
    return '''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Document-to-Data Lab — rapport</title><style>body{font:16px system-ui;background:#f5f7fa;color:#153246;margin:0}main{max-width:1180px;margin:auto;padding:35px 20px}h1{font-size:clamp(2rem,5vw,3.5rem)}.metrics{display:flex;flex-wrap:wrap;gap:15px}.metric{background:white;padding:20px;border-radius:12px;flex:1;min-width:170px}.metric strong{display:block;font-size:2rem;color:#246c70}table{border-collapse:collapse;width:100%;background:white}td,th{padding:12px;text-align:left;border-bottom:1px solid #ddd}.scroll{overflow:auto}code{background:#e5edf2;padding:3px}li{margin:12px 0;overflow-wrap:anywhere}button{padding:12px;border:0;border-radius:8px;background:#246c70;color:white;cursor:pointer}</style><main><p>JUNIOR BOOTO · PYTHON & DONNÉES</p><h1>Chaque ligne garde son origine.</h1><p>Démonstration sur documents fictifs. Rapport calculé par Python ; cette page affiche les résultats enregistrés, sans extraction dans le navigateur.</p><div class="metrics">'''+cards+'''</div><h2>Inspecter les décisions</h2><button id="filter" type="button">Afficher seulement les lignes à revoir</button><div class="scroll"><table><thead><tr><th>ID</th><th>Date</th><th>Montant</th><th>Devise</th><th>Statut</th><th>Motif</th><th>Fichier</th><th>Page</th><th>Ligne</th></tr></thead><tbody>'''+body+'''</tbody></table></div><h2>Totaux des lignes acceptées, séparés par devise</h2><pre>'''+esc(json.dumps(report['totals'],ensure_ascii=False,indent=2))+'''</pre><h2>Incidents et rapprochement des totaux déclarés</h2><ul>'''+findings+'''</ul><p>Un doublon incertain reste à revoir. Un total extrait du document est comparé au total brut des montants lisibles de la même page, avant exclusions. Il ne prouve pas à lui seul la justesse des données.</p><script>let review=false;document.getElementById('filter').onclick=function(){review=!review;document.querySelectorAll('tbody tr').forEach(r=>r.hidden=review&&r.cells[4].textContent==='accepted');this.textContent=review?'Afficher toutes les lignes':'Afficher seulement les lignes à revoir';};</script></main></html>'''

def run(inputs, output):
    inputs, output = Path(inputs).resolve(), Path(output).resolve()
    if inputs == output or inputs in output.parents:
        raise ValueError('La sortie doit être hors du dossier source')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Sortie non vide : choisir un nouveau dossier pour préserver les résultats')
    paths = sorted(p for p in inputs.iterdir() if p.is_file() and not p.is_symlink())
    if not paths: raise ValueError('Aucun fichier source')
    output.mkdir(parents=True,exist_ok=True)
    all_rows, files, file_issues = [], [], []
    for path in paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        meta={'file':path.name,'sha256':digest,'status':'completed'}
        try:
            records, totals = extract(path)
            for r in records:
                normalized, errors = validate(r)
                normalized.update({k:v for k,v in r.items() if k not in ('raw','row_width_valid')})
                normalized.update({'source_file':path.name,'source_sha256':digest,'raw':r['raw'], 'issues':errors,'status':'review' if errors else 'accepted'})
                all_rows.append(normalized)
            for control in totals:
                values=[]
                for r in records:
                    if r['source_page']==control['page'] and str(r['raw'].get('currency','')).strip().upper()==control['currency']:
                        try: values.append(amount(r['raw'].get('amount','')))
                        except ValueError: pass
                observed = sum(values,Decimal('0.00'))
                if observed != Decimal(control['amount']): file_issues.append({'source_file':path.name,'code':'declared_total_mismatch','page':control['page'],'currency':control['currency'],'declared':control['amount'],'readable_total':str(observed)})
        except Exception as exc:
            meta['status']='blocked';meta['error']=str(exc)
            file_issues.append({'source_file':path.name,'code':'document_blocked','detail':str(exc)})
        files.append(meta)
    # Identifiant répété : toutes les occurrences sont soumises à révision.
    groups={}
    for r in all_rows:
        if r['id']: groups.setdefault(r['id'],[]).append(r)
    for group in groups.values():
        if len(group)>1:
            exact=len({tuple(r[k] for k in FIELDS) for r in group})==1
            for r in group: r['issues'].append('duplicate_exact' if exact else 'duplicate_conflict');r['status']='review'
    accepted=[r for r in all_rows if r['status']=='accepted']
    totals={}
    for r in accepted:totals[r['currency']]=totals.get(r['currency'],Decimal('0.00'))+Decimal(r['amount'])
    summary={'extracted':len(all_rows),'accepted':len(accepted),'review':len(all_rows)-len(accepted),'blocked_documents':sum(f['status']=='blocked' for f in files),'totals':{k:str(v) for k,v in sorted(totals.items())},'file_issues':file_issues,'files':files,'demo':'Données fictives pour la démonstration fournie ; vérifier la provenance de vos propres entrées.'}
    provenance=['source_file','source_sha256','source_page','source_table','source_row']
    write_csv(output/'accepted.csv',accepted,FIELDS+provenance)
    write_csv(output/'review.csv',[dict(r,issues=';'.join(r['issues'])) for r in all_rows if r['status']=='review'],FIELDS+provenance+['issues'])
    (output/'rows.json').write_text(json.dumps(all_rows,ensure_ascii=False,indent=2))
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    (output/'report.html').write_text(render(summary,all_rows))
    manifest={'objective':'Extraction PDF/CSV, validation et consolidation par devise','source_hashes':files,'files':['accepted.csv','review.csv','rows.json','summary.json','report.html'],'transformations':['alias en-têtes','dates ISO','montants Decimal','monnaies majuscules','quarantaine des anomalies'],'status':'completed','quality_review_required':bool(summary['review'] or summary['blocked_documents'] or file_issues),'ocr':'not_implemented'}
    (output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('inputs');p.add_argument('--out',required=True);args=p.parse_args()
    print(json.dumps(run(args.inputs,args.out),ensure_ascii=False,indent=2))
