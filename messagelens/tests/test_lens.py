import json,sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from lens import normalize,grouped,split,metric,portable

class Tests(unittest.TestCase):
    def test_url_mask(self):self.assertEqual(normalize('visit https://example.org/claim'),'visit url')
    def test_email_mask(self):self.assertEqual(normalize('mail me x@example.org'),'mail me email')
    def test_digits_mask(self):self.assertEqual(normalize('call 12345'),'call number')
    def test_case(self):self.assertEqual(normalize('FREE Prize'),'free prize')
    def test_empty(self):self.assertEqual(normalize('!!!'),'')
    def test_punctuation(self):self.assertEqual(normalize('Hello, friend!'),'hello friend')
    def test_exact_duplicates_grouped(self):g=grouped(['hello friend','hello friend','different message']);self.assertEqual(g[0],g[1]);self.assertNotEqual(g[0],g[2])
    def test_phone_variants_grouped(self):g=grouped(['claim 123456 now','claim 999999 now']);self.assertEqual(g[0],g[1])
    def test_url_variants_grouped(self):g=grouped(['visit https://example.org/a now','visit https://example.org/b now']);self.assertEqual(g[0],g[1])
    def test_split_disjoint(self):
        y=np.array([0,1]*50);g=np.repeat(np.arange(50),2);a,b,c=split(y,g);self.assertFalse(set(g[a])&set(g[b]));self.assertFalse(set(g[b])&set(g[c]));self.assertFalse(set(g[a])&set(g[c]))
    def test_baseline_recall_zero(self):self.assertEqual(metric([0,1],[0,0],.5)['recall'],0)
    def test_confusion_order(self):self.assertEqual(metric([0,0,1,1],[0,.8,.9,0],.5)['matrix'],[[1,1],[1,1]])
    def test_no_known_terms(self):
        m={'terms':['hello'],'idf':[1],'coef':[2],'intercept':-1,'threshold':.5};r=portable('xyzzy',m);self.assertEqual(r['known_terms'],0);self.assertEqual(r['label'],'ham')
    def test_contribution_exact_logit(self):
        m={'terms':['hello'],'idf':[1],'coef':[2],'intercept':-1,'threshold':.5};r=portable('hello',m);self.assertAlmostEqual(r['logit'],1);self.assertEqual(r['label'],'spam')
    def test_l2_repeated_word(self):
        m={'terms':['hello'],'idf':[1],'coef':[2],'intercept':-1,'threshold':.5};self.assertEqual(portable('hello',m)['score'],portable('hello hello',m)['score'])
    def test_exported_model_examples(self):
        p=Path(__file__).resolve().parents[1]/'reports';m=json.loads((p/'model.json').read_text())
        for e in json.loads((p/'examples.json').read_text()):self.assertAlmostEqual(portable(e['text'],m)['score'],e['score'],12)
    def test_exported_partitions_disjoint(self):
        p=Path(__file__).resolve().parents[1]/'reports';s=json.loads((p/'split_indices.json').read_text());self.assertFalse(set(s['train'])&set(s['test']));self.assertFalse(set(s['validation'])&set(s['test']))

if __name__=='__main__':unittest.main()
