import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from watch import canonical,published,relevance,parse_rss,dedupe,compare,run,report,fetch,FEED

def rss(title='Python',url='https://example.org/a',guid='A',date='Mon, 12 Oct 2026 10:00:00 +0000'):
    return f'<rss><channel><item><guid>{guid}</guid><title>{title}</title><link>{url}</link><pubDate>{date}</pubDate></item></channel></rss>'.encode()

class Tests(unittest.TestCase):
    def test_tracking_removed(self):self.assertEqual(canonical('https://EXAMPLE.org/a?utm_source=x&amp=1#t'),'https://example.org/a?amp=1')
    def test_query_semantics_preserved(self):self.assertEqual(canonical('https://example.org/a?id=42'),'https://example.org/a?id=42')
    def test_private_ip_rejected(self):
        with self.assertRaises(ValueError):canonical('http://127.0.0.1/a')
    def test_localhost_rejected(self):
        with self.assertRaises(ValueError):canonical('https://localhost/a')
    def test_script_link_rejected(self):
        with self.assertRaises(ValueError):canonical('javascript:alert(1)')
    def test_embedded_credentials_rejected(self):
        with self.assertRaises(ValueError):canonical('https://me:secret@example.org/a')
    def test_dates_utc(self):self.assertEqual(published('Mon, 12 Oct 2026 12:00:00 +0200'),'2026-10-12T10:00:00+00:00')
    def test_absent_date_unknown(self):self.assertIsNone(published(''))
    def test_invalid_date_rejected(self):
        with self.assertRaises(ValueError):published('tomorrow')
    def test_keyword_boundaries(self):self.assertEqual(relevance('Pythonic systems'),[])
    def test_explained_relevance(self):self.assertEqual(relevance('Python for teaching'),['python: python','education: teaching'])
    def test_limit_coverage(self):
        p=Path(__file__).resolve().parents[1]/'demo/fixtures/before.xml';rows,e,c=parse_rss(p.read_bytes(),FEED,'t',2);self.assertEqual(len(rows),2);self.assertFalse(c['complete_feed_examined'])
    def test_item_invalid_isolated(self):
        rows,e,c=parse_rss(rss(url='file:///etc/passwd'),FEED,'t');self.assertEqual(len(rows),0);self.assertEqual(len(e),1)
    def test_xml_entity_rejected(self):
        with self.assertRaises(ValueError):parse_rss(b'<!DOCTYPE rss><rss><channel/></rss>',FEED,'t')
    def test_same_title_different_urls_not_merged(self):
        a=parse_rss(rss(),FEED,'t')[0];b=parse_rss(rss(url='https://example.org/b',guid='B'),FEED,'t')[0];self.assertEqual(len(dedupe(a+b)),2)
    def test_url_duplicate_provenance_retained(self):
        a=parse_rss(rss(),FEED,'t')[0];b=parse_rss(rss(), 'other-source','t')[0];g=dedupe(a+b);self.assertEqual(len(g),1);self.assertEqual(g[0]['source_count'],2);self.assertEqual(len(g[0]['observations']),2)
    def test_collection_time_not_change(self):
        a=parse_rss(rss(),FEED,'t1')[0];b=parse_rss(rss(),FEED,'t2')[0];self.assertEqual(compare(a,b)[0]['status'],'unchanged')
    def test_duplicate_key_comparison_rejected(self):
        a=parse_rss(rss(),FEED,'t')[0]
        with self.assertRaises(ValueError):compare(a+a,a)
    def test_fixture_changes(self):
        p=Path(__file__).resolve().parents[1]/'demo/fixtures';a=parse_rss((p/'before.xml').read_bytes(),FEED,'t')[0];b=parse_rss((p/'after.xml').read_bytes(),FEED,'t')[0];self.assertEqual(sorted(c['status'] for c in compare(a,b)),['absent_from_snapshot','changed','new','unchanged'])
    def test_http429_records_block(self):
        with tempfile.TemporaryDirectory() as t:
            with patch('watch.fetch',side_effect=HTTPError(FEED,429,'rate limit',{},None)):
                with self.assertRaises(HTTPError):run(Path(t)/'out')
            self.assertEqual(json.loads((Path(t)/'out/manifest.json').read_text())['status'],'blocked')
    def test_timeout_records_block(self):
        with tempfile.TemporaryDirectory() as t:
            with patch('watch.fetch',side_effect=TimeoutError('timeout')):
                with self.assertRaises(TimeoutError):run(Path(t)/'out')
            self.assertEqual(json.loads((Path(t)/'out/manifest.json').read_text())['status'],'blocked')
    def test_preserve_snapshot(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'out';p.mkdir();(p/'sentinel').write_text('keep')
            with self.assertRaises(ValueError):run(p)
            self.assertEqual((p/'sentinel').read_text(),'keep')
    def test_octet_stream_rss_accepted(self):
        from unittest.mock import MagicMock
        r=MagicMock();r.headers={'Content-Type':'application/octet-stream'};r.read.return_value=rss();r.status=200
        opener=MagicMock();opener.open.return_value.__enter__.return_value=r
        with patch('watch.build_opener',return_value=opener):
            data,meta=fetch();self.assertEqual(len(parse_rss(data,FEED,'t')[0]),1);self.assertEqual(meta['http_status'],200)
    def test_html_mime_rejected(self):
        from unittest.mock import MagicMock
        r=MagicMock();r.headers={'Content-Type':'text/html'}
        opener=MagicMock();opener.open.return_value.__enter__.return_value=r
        with patch('watch.build_opener',return_value=opener):
            with self.assertRaises(ValueError):fetch()
    def test_render_escapes_title(self):
        records=parse_rss(rss(title='&lt;script&gt;bad()&lt;/script&gt;'),FEED,'t')[0]
        self.assertNotIn('<script>bad()</script>',report({'records':records,'network':{'mode':'offline'}}))

if __name__=='__main__':unittest.main()
