import hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from file_guardian.core import scan,organize,restore,export_report,validate_categories,digest

class GuardianTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
  self.base=Path(self.tmp.name); self.source=self.base/'source'; self.source.mkdir()
  for name,data in {'a/lesson.txt':b'Bonjour !','b/copy.txt':b'Bonjour !','b/lesson.txt':b'Different','empty.txt':b''}.items(): self.put(name,data)
 def put(self,name,data):
  p=self.source/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data)
 def snapshot(self): return {str(p.relative_to(self.source)):p.read_bytes() for p in self.source.rglob('*') if p.is_file()}
 def test_exact_duplicates_and_different_same_names(self):
  p=scan(self.source)
  self.assertEqual(p['summary']['files'],4); self.assertEqual(p['duplicates'][0]['paths'],['a/lesson.txt','b/copy.txt'])
  self.assertEqual(p['summary']['redundant_bytes'],9); self.assertEqual(p['name_collisions'],[['a/lesson.txt','b/lesson.txt']])
 def test_empty_hash(self):
  f=next(f for f in scan(self.source)['files'] if f['path']=='empty.txt'); self.assertEqual(f['sha256'],hashlib.sha256(b'').hexdigest())
 def test_repeatability_no_writes(self):
  before=self.snapshot(); self.assertEqual(scan(self.source),scan(self.source)); self.assertEqual(before,self.snapshot()); self.assertEqual(list(self.base.iterdir()),[self.source])
 def test_copy_preserves_collisions_and_originals(self):
  before=self.snapshot(); dst=self.base/'organized'; j=organize(self.source,dst)
  self.assertEqual(j['status'],'completed'); self.assertEqual(before,self.snapshot())
  self.assertEqual((dst/'documents/a/lesson.txt').read_bytes(),b'Bonjour !'); self.assertEqual((dst/'documents/b/lesson.txt').read_bytes(),b'Different')
 def test_no_overwrite(self):
  dst=self.base/'organized'; organize(self.source,dst)
  with self.assertRaises(ValueError): organize(self.source,dst)
 def test_nested_destination(self):
  with self.assertRaises(ValueError): organize(self.source,self.source/'output')
 def test_restore_preview_then_execute(self):
  dst=self.base/'organized'; organize(self.source,dst); self.assertEqual(len(restore(dst)['paths']),4)
  self.assertTrue((dst/'documents/empty.txt').exists()); restore(dst,True); self.assertFalse((dst/'documents/empty.txt').exists()); self.assertEqual(restore(dst)['paths'],[]); self.assertEqual(len(self.snapshot()),4)
 def test_modified_copy_blocks_all_deletions(self):
  dst=self.base/'organized'; organize(self.source,dst); (dst/'documents/b/lesson.txt').write_text('modified')
  with self.assertRaises(ValueError): restore(dst,True)
  self.assertTrue((dst/'documents/a/lesson.txt').exists())
 def test_untracked_files_preserved(self):
  dst=self.base/'organized'; organize(self.source,dst); (dst/'personal.txt').write_text('untracked'); restore(dst,True); self.assertTrue((dst/'personal.txt').exists())
 def test_symlink_file_refused(self):
  try: (self.source/'outside.txt').symlink_to(self.base/'outside.txt')
  except OSError: self.skipTest('Symlinks unavailable')
  p=scan(self.source); self.assertTrue(p['errors']); self.assertEqual(len(p['files']),4)
 def test_symlink_directory_not_traversed(self):
  outside=self.base/'outside'; outside.mkdir(); (outside/'secret.txt').write_text('secret')
  try: (self.source/'link').symlink_to(outside,target_is_directory=True)
  except OSError: self.skipTest('Symlinks unavailable')
  p=scan(self.source); self.assertEqual(len(p['files']),4); self.assertEqual(p['skipped'],[{'path':'link','reason':'symlink'}])
 def test_permission_error_reported_and_blocks_copy(self):
  def restricted(path):
   if path.name=='empty.txt': raise PermissionError('Fixture unreadable file')
   return digest(path)
  with patch('file_guardian.core.digest',side_effect=restricted):
   self.assertEqual(len(scan(self.source)['errors']),1)
   with self.assertRaises(ValueError): organize(self.source,self.base/'organized')
  self.assertFalse((self.base/'organized').exists())
 def test_journal_traversal_refused(self):
  dst=self.base/'organized'; organize(self.source,dst); p=dst/'guardian-journal.json'; j=json.loads(p.read_text()); j['created'][0]['path']='../source/a/lesson.txt'; p.write_text(json.dumps(j))
  with self.assertRaises(ValueError): restore(dst,True)
  self.assertTrue((self.source/'a/lesson.txt').exists())
 def test_symlink_replacement_on_restore_refused(self):
  dst=self.base/'organized'; organize(self.source,dst); p=dst/'documents/a/lesson.txt'; p.unlink()
  try: p.symlink_to(self.source/'a/lesson.txt')
  except OSError: self.skipTest('Symlinks unavailable')
  with self.assertRaises(ValueError): restore(dst,True)
 def test_html_and_csv_escaping(self):
  self.put('<script>.txt',b'example'); self.put('=2+2.txt',b'example2'); export_report(scan(self.source),self.base/'report')
  t=(self.base/'report/report.html').read_text(); self.assertIn('&lt;script&gt;.txt',t); self.assertNotIn('<script>.txt',t)
  self.assertIn("'=2+2.txt",(self.base/'report/inventory.csv').read_text(encoding='utf-8-sig'))
 def test_config_validation(self):
  self.assertTrue(all(f['category']=='fle' for f in scan(self.source,{'fle':['.txt']})['files']))
  for rules in ({'../bad':['.txt']},{'a':['.txt'],'b':['.txt']}):
   with self.assertRaises(ValueError): validate_categories(rules)
 def test_cli_dry_run(self):
  r=subprocess.run([sys.executable,'-m','file_guardian','organize',str(self.source),str(self.base/'organized')],capture_output=True,text=True)
  self.assertEqual(r.returncode,0,r.stderr); self.assertEqual(json.loads(r.stdout)['mode'],'simulation'); self.assertFalse((self.base/'organized').exists())
 def test_cli_report_inside_source_refused(self):
  r=subprocess.run([sys.executable,'-m','file_guardian','scan',str(self.source),'--output',str(self.source/'reports')],capture_output=True,text=True)
  self.assertEqual(r.returncode,2); self.assertFalse((self.source/'reports').exists())

 def test_source_change_after_scan_is_detected(self):
  original_scan=scan
  def changed_scan(root,categories=None):
   plan=original_scan(root,categories)
   (root/'a/lesson.txt').write_bytes(b'Changed after inventory')
   return plan
  dst=self.base/'organized'
  with patch('file_guardian.core.scan',side_effect=changed_scan):
   with self.assertRaises(ValueError): organize(self.source,dst)
  self.assertFalse((dst/'documents/a/lesson.txt').exists())
  self.assertEqual(json.loads((dst/'guardian-journal.json').read_text())['status'],'failed')
 def test_copy_failure_records_pending_intent(self):
  real_open=Path.open
  def fail_copy(path,*args,**kwargs):
   if args and args[0]=='xb': raise OSError('Fixture disk failure')
   return real_open(path,*args,**kwargs)
  dst=self.base/'organized'
  with patch.object(Path,'open',fail_copy):
   with self.assertRaises(OSError): organize(self.source,dst)
  journal=json.loads((dst/'guardian-journal.json').read_text())
  self.assertEqual(journal['status'],'failed'); self.assertEqual(journal['created'][0]['status'],'pending')

if __name__=='__main__': unittest.main()
