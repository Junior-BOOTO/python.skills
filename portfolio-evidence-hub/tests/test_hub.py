import copy,json,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
from http.server import HTTPServer
from unittest.mock import patch
from evidence_hub.audit import audit,blob_sha,compare_local,validate_config
from evidence_hub.render import render
from evidence_hub.server import handler
from evidence_hub.collect import collect_sites

class EvidenceTests(unittest.TestCase):
 def setUp(self):
  self.config={'repository':'owner/repo','site_host':'portfolio.example','projects':[{'id':'demo','title':'Demo','path':'demo','site_url':'https://portfolio.example/demo.html','site_marker':'Demo','workflow':'.github/workflows/demo.yml','validation_file':'demo/validation.json'}]}
  validation=json.dumps({'tests_passed':3,'exit_code':0})
  self.snapshot={'schema_version':1,'repository':'owner/repo','commit':'a'*40,'collected_at':'2026-10-12T00:00:00+00:00','tree_complete':True,'files':[{'path':p,'sha':blob_sha(c),'size':len(c.encode())} for p,c in [('demo/README.md','# Demo'),('demo/main.py','print(1)'),('demo/tests/test_main.py','test'),('demo/pyproject.toml','deps'),('demo/validation.json',validation)]],'documents':{'demo/validation.json':{'content':validation,'sha':blob_sha(validation)}},'runs':[{'id':1,'path':'.github/workflows/demo.yml','head_sha':'a'*40,'status':'completed','conclusion':'success','url':'https://github.com/owner/repo/actions/runs/1'}]}
  self.sites=[{'url':'https://portfolio.example/demo.html','status':200,'final_url':'https://portfolio.example/demo.html','marker_found':True,'checked_at':'2026-10-12T00:00:00Z'}]
 def report(self):return audit(self.config,self.snapshot,self.sites)
 def status(self,key):return next(f['status'] for f in self.report()['projects'][0]['findings'] if f['key']==key)
 def test_missing_test_file_is_not_a_failed_test(self):
  self.snapshot['files']=[f for f in self.snapshot['files'] if '/tests/' not in f['path']]
  self.assertEqual(self.status('tests'),'missing');self.assertEqual(self.status('ci'),'verified')
 def test_incomplete_tree_keeps_absence_unknown(self):
  self.snapshot['tree_complete']=False;self.snapshot['files']=[]
  self.assertEqual(self.status('readme'),'unknown')
 def test_ci_of_another_project_not_transferred(self):
  self.snapshot['runs'][0]['path']='.github/workflows/other.yml';self.assertEqual(self.status('ci'),'unknown')
 def test_ci_of_another_commit_not_transferred(self):
  self.snapshot['runs'][0]['head_sha']='b'*40;self.assertEqual(self.status('ci'),'unknown')
 def test_latest_ci_failure_is_attention(self):
  run=copy.deepcopy(self.snapshot['runs'][0]);run.update(id=2,conclusion='failure');self.snapshot['runs'].append(run);self.assertEqual(self.status('ci'),'attention')
 def test_running_ci_is_unknown(self):
  self.snapshot['runs'][0].update(status='in_progress',conclusion=None);self.assertEqual(self.status('ci'),'unknown')
 def test_metadata_is_a_declaration_not_execution(self):
  finding=next(f for f in self.report()['projects'][0]['findings'] if f['key']=='local_result')
  self.assertIn('Déclaration locale',finding['detail']);self.assertIn('À distinguer',finding['detail'])
 def test_tampered_metadata_not_verified(self):
  self.snapshot['documents']['demo/validation.json']['content']='{"tests_passed":900}'
  self.assertEqual(self.status('local_result'),'unknown')
 def test_wrong_repo_rejected(self):
  self.snapshot['repository']='other/repo'
  with self.assertRaises(ValueError):self.report()
 def test_404_is_missing_but_network_error_unknown(self):
  self.sites[0].update(status=404,marker_found=False);self.assertEqual(self.status('site'),'missing')
  self.sites[0]['error']='HTTPError';self.assertEqual(self.status('site'),'unknown')
 def test_login_page_not_verified(self):
  self.sites[0]['marker_found']=False;self.assertEqual(self.status('site'),'attention')
 def test_redirect_outside_configured_host_not_verified(self):
  self.sites[0]['final_url']='https://login.example/login';self.assertEqual(self.status('site'),'attention')
 def test_html_escapes_project_and_source(self):
  self.config['projects'][0]['title']='<script>alert(1)</script>'
  page=render(self.report());self.assertIn('&lt;script&gt;',page);self.assertNotIn('<script>alert(1)',page)
 def test_local_hash_matches_and_detects_changes(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'main.py').write_text('print(1)')
   rows=[f for f in self.snapshot['files'] if f['path']=='demo/main.py']
   self.assertEqual(compare_local(root,'demo',rows)['files'][0]['state'],'match')
   (root/'main.py').write_text('print(2)');self.assertEqual(compare_local(root,'demo',rows)['files'][0]['state'],'different')
 def test_local_absent_and_symlink(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);rows=[f for f in self.snapshot['files'] if f['path']=='demo/main.py']
   self.assertEqual(compare_local(root,'demo',rows)['files'][0]['state'],'missing')
   try:(root/'main.py').symlink_to(root/'elsewhere')
   except OSError:self.skipTest('Symlink unavailable')
   with self.assertRaises(ValueError):compare_local(root,'demo',rows)
 def test_unsafe_paths_hosts_and_duplicate_ids_rejected(self):
  for change in [{'path':'../escape'},{'site_url':'http://portfolio.example/x'},{'site_url':'https://external.example/x'}]:
   config=copy.deepcopy(self.config);config['projects'][0].update(change)
   with self.assertRaises(ValueError):validate_config(config)
  self.config['projects'].append(copy.deepcopy(self.config['projects'][0]))
  with self.assertRaises(ValueError):validate_config(self.config)
 def test_site_collector_records_http_status(self):
  error=urllib.error.HTTPError(self.sites[0]['url'],403,'Forbidden',{},None)
  with patch('evidence_hub.collect.get',side_effect=error):rows=collect_sites(self.config)
  self.assertEqual(rows[0]['status'],403);self.assertEqual(rows[0]['error'],'HTTPError')
 def test_report_repeatable_and_summary_correct(self):
  self.assertEqual(self.report(),self.report());s=self.report()['summary'];self.assertEqual(s['checks'],8);self.assertEqual(s['verified'],7);self.assertEqual(s['unknown'],1)
 def test_local_api_routes_and_read_only(self):
  server=HTTPServer(('127.0.0.1',0),handler(self.report()));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  try:
   origin='http://127.0.0.1:'+str(server.server_port)
   with urllib.request.urlopen(origin+'/api/report') as r:self.assertEqual(json.loads(r.read())['summary']['projects'],1)
   with urllib.request.urlopen(origin+'/api/projects/demo') as r:self.assertEqual(json.loads(r.read())['id'],'demo')
   for url,method,code in [('/api/projects/absent','GET',404),('/api/report','POST',405)]:
    with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(urllib.request.Request(origin+url,method=method))
    self.assertEqual(error.exception.code,code)
  finally:server.shutdown();server.server_close();thread.join()

 def test_line_ending_difference_explained_without_marking_match(self):
  import base64
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'data.csv').write_bytes(b'a,b\r\n1,2\r\n')
   remote=b'a,b\n1,2\n';rows=[{'path':'demo/data.csv','sha':blob_sha(remote)}]
   docs={'demo/data.csv':{'encoding':'base64','content':base64.b64encode(remote).decode()}}
   item=compare_local(root,'demo',rows,docs)['files'][0]
   self.assertEqual(item['state'],'different');self.assertIn('CRLF/LF',item['explanation'])

if __name__=='__main__':unittest.main()
