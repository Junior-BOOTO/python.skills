"""Generate synthetic data and verify the full copy/restore workflow."""
import json,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'src'))
from file_guardian.core import scan,export_report,organize,restore
with tempfile.TemporaryDirectory() as tmp:
 source=Path(tmp)/'input'; source.mkdir()
 fixtures={'fle/routine.txt':'Je me lève. Je prends mon petit déjeuner.\n','archives/routine_copy.txt':'Je me lève. Je prends mon petit déjeuner.\n','fle/lesson.txt':'Les meubles de la maison.\n','drafts/lesson.txt':'Les paysages naturels.\n','python/analyze.py':'print("Synthetic portfolio fixture")\n','data/metrics.csv':'topic,count\nroutine,4\nmeubles,6\n','notes/project.md':'# Portfolio\nSynthetic demonstration only.\n','empty.txt':''}
 for name,text in fixtures.items():
  p=source/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')
 before={name:(source/name).read_bytes() for name in fixtures}
 plan=scan(source); assert scan(source)==plan; assert plan['summary']['files']==8; assert plan['summary']['duplicate_groups']==1
 export_report(plan,root/'reports')
 dst=Path(tmp)/'organized'; journal=organize(source,dst)
 (root/'reports/copy-journal.example.json').write_text(json.dumps(journal,ensure_ascii=False,indent=2),encoding='utf-8')
 preview=restore(dst); assert len(preview['paths'])==8; restore(dst,True); assert not restore(dst)['paths']
 assert before=={name:(source/name).read_bytes() for name in fixtures}
 evidence={'dataset':'8 synthetic files generated in temporary directory','summary':plan['summary'],'name_collisions':plan['name_collisions'],'scan_repeatable':True,'copies_verified':len(journal['created']),'restore_preview':len(preview['paths']),'originals_unchanged':True,'restore_completed':True}
 (root/'reports/demo-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(evidence,ensure_ascii=False,indent=2))
