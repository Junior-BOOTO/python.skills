import copy,json,os,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
from http.server import HTTPServer
from unittest.mock import patch
from fle_studio.core import build_kit,export_kit,approved_videos,validate_catalog,SUPPORTS
from fle_studio.render import render_kit,render_studio
from fle_studio.server import handler
from fle_studio.youtube import metadata

class StudioTests(unittest.TestCase):
 def setUp(self):self.catalog=json.loads(Path('data/catalog.json').read_text())
 def test_catalog_five_themes_fifty_entries(self):
  validate_catalog(self.catalog);self.assertEqual(len(self.catalog['themes']),5);self.assertEqual(sum(len(t['lexicon']) for t in self.catalog['themes']),50)
 def test_all_forty_five_variants(self):
  for t in self.catalog['themes']:
   for s in SUPPORTS:
    for lang in ('fr','es','en'):
     k=build_kit(self.catalog,t['id'],support=s,language=lang);self.assertEqual(k['objective'],t['objective']);self.assertEqual(k['support'],s);self.assertEqual(k['aid_language'],lang)
 def test_three_steps_sum_to_45(self):
  for t in self.catalog['themes']:
   k=build_kit(self.catalog,t['id']);self.assertEqual(sum(s['minutes'] for s in k['teacher']['stages']),45);self.assertEqual(len(k['teacher']['stages']),3)
 def test_main_activity_and_resources(self):
  k=build_kit(self.catalog,'meubles');self.assertIn('Les élèves vont',k['teacher']['stages'][1]['instructions']);self.assertIn('binômes',k['teacher']['stages'][1]['grouping']);self.assertIn('Portfolio',k['teacher']['resources'])
 def test_objective_common_across_supports(self):
  kits=[build_kit(self.catalog,'routine',support=s) for s in SUPPORTS];self.assertEqual(len({k['objective'] for k in kits}),1);self.assertEqual(len({k['differentiation'] for k in kits}),3)
 def test_unknown_theme_level_and_options_rejected(self):
  for kw in ({'theme_id':'missing'},{'theme_id':'meubles','level':'A2'},{'theme_id':'meubles','support':'magic'},{'theme_id':'meubles','language':'de'}):
   with self.assertRaises(ValueError):build_kit(self.catalog,**kw)
 def test_civic_criteria_align_right_and_duties(self):
  k=build_kit(self.catalog,'ecocitoyen');self.assertIn('un droit et deux devoirs',k['learner']['task']);self.assertIn('un droit + deux devoirs',k['teacher']['criteria'][1]['threshold'])
 def test_matching_answers_are_correct(self):
  for t in self.catalog['themes']:
   k=build_kit(self.catalog,t['id']);ex=k['learner']['exercise'];choices={c['letter']:c['text'] for c in ex['choices']}
   for i,w in enumerate(t['lexicon'][:3],1):self.assertEqual(choices[ex['answers'][str(i)]],w['es'])
 def test_french_only_activity_not_mislabeled_comprehension(self):
  k=build_kit(self.catalog,'routine',language='fr');self.assertIn('pas une preuve de compréhension',k['learner']['exercise']['note'])
 def test_pending_video_never_approved(self):
  k=build_kit(self.catalog,'routine');self.assertEqual(k['approved_videos'],[]);self.assertEqual(len(k['video_candidates']),1)
 def test_incomplete_review_not_approved(self):
  t=self.catalog['themes'][1];v=t['videos'][0];v['review_status']='approved';v['reviewer']='teacher';v['reviewed_at']='2026-10-12';v['checks']['age_appropriate']=True;self.assertEqual(approved_videos(t),[])
 def test_full_review_can_approve(self):
  t=self.catalog['themes'][1];v=t['videos'][0];v.update(review_status='approved',reviewer='teacher',reviewed_at='2026-10-12');v['checks']={k:True for k in v['checks']};self.assertEqual(len(approved_videos(t)),1)
 def test_duplicate_ids_and_bad_video_url_rejected(self):
  c=copy.deepcopy(self.catalog);c['themes'].append(copy.deepcopy(c['themes'][0]))
  with self.assertRaises(ValueError):validate_catalog(c)
  c=copy.deepcopy(self.catalog);c['themes'][1]['videos'][0]['url']='javascript:alert(1)'
  with self.assertRaises(ValueError):validate_catalog(c)
 def test_html_and_script_escaping(self):
  c=copy.deepcopy(self.catalog);c['themes'][0]['title']='</script><script>alert(1)</script>'
  page=render_studio(c);self.assertNotIn('</script><script>alert(1)',page);self.assertIn('\\u003c',page)
 def test_export_no_overwrite_and_text_audio_only(self):
  with tempfile.TemporaryDirectory() as tmp:
   k=build_kit(self.catalog,'meubles');p=export_kit(k,tmp);self.assertTrue((p/'audio-script.txt').exists());self.assertFalse(any(p.glob('*.mp3')));self.assertFalse(k['audio']['recording_available'])
   with self.assertRaises(ValueError):export_kit(k,tmp)
 def test_kit_detached_from_catalog(self):
  k=build_kit(self.catalog,'meubles');k['lexicon'][0]['fr']='changed';self.assertEqual(self.catalog['themes'][0]['lexicon'][0]['fr'],'un lit')
 def test_missing_youtube_key_and_invalid_id(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(ValueError):metadata(['yW5PvraL-wA'])
  with self.assertRaises(ValueError):metadata(['wrong'])
 def test_youtube_metadata_never_auto_approves(self):
  class Response:
   def __enter__(self):return self
   def __exit__(self,*a):pass
   def read(self,n):return json.dumps({'items':[{'id':'yW5PvraL-wA','snippet':{'title':'Demo'},'contentDetails':{'duration':'PT2M'},'status':{'embeddable':True}}]}).encode()
  with patch.dict(os.environ,{'YOUTUBE_API_KEY':'TEST_NOT_REAL'}),patch('fle_studio.youtube.urllib.request.urlopen',return_value=Response()):r=metadata(['yW5PvraL-wA'])
  self.assertFalse(r['pedagogical_approval']);self.assertEqual(r['items'][0]['review_status'],'pending');self.assertNotIn('TEST_NOT_REAL',json.dumps(r))
 def test_youtube_error_does_not_leak_key(self):
  err=urllib.error.HTTPError('https://example/?key=SECRET',403,'Forbidden',{},None)
  with patch.dict(os.environ,{'YOUTUBE_API_KEY':'SECRET'}),patch('fle_studio.youtube.urllib.request.urlopen',side_effect=err):
   with self.assertRaises(RuntimeError) as caught:metadata(['yW5PvraL-wA'])
  self.assertNotIn('SECRET',str(caught.exception))
 def test_local_api_validation_and_no_writes(self):
  server=HTTPServer(('127.0.0.1',0),handler(self.catalog));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  try:
   base='http://127.0.0.1:'+str(server.server_port)
   with urllib.request.urlopen(base+'/api/kits/meubles?language=en&support=guided') as r:k=json.loads(r.read());self.assertEqual(k['aid_language'],'en');self.assertEqual(k['support'],'guided')
   for url,method,code in [('/api/kits/meubles?level=A2','GET',400),('/missing','GET',404),('/api/catalog','POST',405)]:
    with self.assertRaises(urllib.error.HTTPError) as err:urllib.request.urlopen(urllib.request.Request(base+url,method=method))
    self.assertEqual(err.exception.code,code)
  finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()
