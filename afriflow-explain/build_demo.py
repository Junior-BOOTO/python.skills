from pathlib import Path
import json
P=Path(__file__).resolve().parent
metrics=json.loads((P/'models/metrics.json').read_text());cases=json.loads((P/'analysis/cases.json').read_text());test=[c for c in cases if c['split']=='test'];sample=[];ids=set()
def add(c):
 if c['id'] not in ids:sample.append(c);ids.add(c['id'])
for c in sorted(test,key=lambda c:-c['scores']['parcours'])[:20]:add(c)
for category in ['rapid_cycle','rapid_relay','legit_chain','legit_cycle','payroll','collection','random']:
 for c in [c for c in test if c['simulation_truth']['scenario']==category][:2]:add(c)
for c in [c for c in test if c['quality']['missing_timestamps']>0][:5]:add(c)
payload=json.dumps({'cases':sample,'metrics':metrics},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
html=(P/'app-template.html').read_text().replace('__PAYLOAD__',payload);assert '__PAYLOAD__' not in html
(P/'dashboard.html').write_text(html)
(P/'analysis/demo_sample.json').write_text(json.dumps({'sample_ids':[c['id'] for c in sample],'sample_size':len(sample),'selection':'20 scores parcours les plus élevés + exemples de chaque scénario et de qualité partielle ; échantillon explicatif non représentatif'},ensure_ascii=False,indent=2))
print(f'{len(sample)} dossiers dans la démonstration ; {len(html.encode())} octets')
