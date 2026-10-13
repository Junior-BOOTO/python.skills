import csv,hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from lab import amount,validate,extract,run,csv_safe,render

def record(**values):
    base={'id':'001','date':'2026-01-01','description':'Livres','amount':'12.50','currency':'USD'};base.update(values)
    return {'raw':base,'row_width_valid':True,'source_page':None,'source_table':1,'source_row':2}

class ContractTests(unittest.TestCase):
    def test_decimal_comma(self): self.assertEqual(str(amount('12,50')),'12.50')
    def test_ambiguous_separator(self):
        with self.assertRaises(ValueError):amount('1,250.00')
    def test_negative_expense(self):
        with self.assertRaises(ValueError):amount('-1')
    def test_nonfinite(self):
        with self.assertRaises(ValueError):amount('NaN')
    def test_extra_precision(self):
        with self.assertRaises(ValueError):amount('1.234')
    def test_impossible_date(self): self.assertIn('invalid_date',validate(record(date='2026-02-30'))[1])
    def test_valid_leap_day(self): self.assertEqual(validate(record(date='2024-02-29'))[1],[])
    def test_currency_outside_contract(self): self.assertIn('unsupported_currency',validate(record(currency='EUR'))[1])
    def test_missing_identifier(self): self.assertIn('missing_id',validate(record(id=''))[1])
    def test_identifier_zeros_preserved(self): self.assertEqual(validate(record())[0]['id'],'001')
    def test_formula_export_escaped(self): self.assertEqual(csv_safe(' =SUM(A1:A2)'),"' =SUM(A1:A2)")
    def test_html_untrusted_content_escaped(self):
        report={'extracted':0,'accepted':0,'review':0,'blocked_documents':1,'file_issues':[{'detail':'<script>alert(1)</script>'}],'totals':{}}
        self.assertNotIn('<script>alert(1)</script>',render(report,[]))

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.inputs=self.root/'inputs';self.inputs.mkdir()
    def tearDown(self): self.temp.cleanup()
    def add(self,name,rows,head=['id','date','description','amount','currency']):
        with (self.inputs/name).open('w',newline='') as f:w=csv.writer(f);w.writerow(head);w.writerows(rows)
    def test_conflicting_duplicates_all_reviewed(self):
        self.add('a.csv',[['X','2026-01-01','A','10','USD'],['X','2026-01-01','A','12','USD']]);s=run(self.inputs,self.root/'out');self.assertEqual(s['accepted'],0);self.assertEqual(s['review'],2)
    def test_multicurrency_not_added_together(self):
        self.add('a.csv',[['X','2026-01-01','A','10','USD'],['Y','2026-01-01','B','200','COP']]);s=run(self.inputs,self.root/'out');self.assertEqual(s['totals'],{'COP':'200.00','USD':'10.00'})
    def test_sources_unchanged(self):
        self.add('a.csv',[['X','2026-01-01','A','10','USD']]);before=(self.inputs/'a.csv').read_bytes();run(self.inputs,self.root/'out');self.assertEqual(before,(self.inputs/'a.csv').read_bytes())
    def test_incompatible_document_isolated(self):
        self.add('a.csv',[['X','2026-01-01','A','10','USD']]);self.add('b.csv',[['2026-01-01','12']],['date','amount']);s=run(self.inputs,self.root/'out');self.assertEqual(s['accepted'],1);self.assertEqual(s['blocked_documents'],1)
    def test_provenance_and_reloading(self):
        self.add('a.csv',[['001','2026-01-01','A','10','USD']]);out=self.root/'out';run(self.inputs,out);r=json.loads((out/'rows.json').read_text())[0];self.assertEqual(r['source_row'],2);self.assertEqual(r['source_sha256'],hashlib.sha256((self.inputs/'a.csv').read_bytes()).hexdigest());self.assertEqual(r['id'],'001')
    def test_preserve_existing_output(self):
        self.add('a.csv',[['X','2026-01-01','A','10','USD']]);out=self.root/'out';run(self.inputs,out)
        with self.assertRaises(ValueError):run(self.inputs,out)
    def test_output_inside_source_rejected(self):
        with self.assertRaises(ValueError):run(self.inputs,self.inputs/'out')
    def test_bad_row_width(self):
        self.add('a.csv',[['X','2026-01-01','A','10','USD','extra']]);self.assertEqual(run(self.inputs,self.root/'out')['review'],1)

class FrozenDemoTests(unittest.TestCase):
    def test_pdf_cells_match_manual_reference(self):
        p=Path(__file__).resolve().parents[1]/'demo/inputs'
        expected=[['A001','2026-01-01','Livres','100.00','USD'],['A002','2026-01-02','Transport','30.00','USD'],['A001','2026-01-01','Livres','100.00','USD'],['A003','2026-01-03','Materiel','25.00','USD'],['A004','2026-02-30','Erreur de saisie','abc','USD']]
        observed=[]
        for name in ['01_report.pdf','02_report.pdf']:
            rows,_=extract(p/name)
            observed.extend([[r['raw'][k] for k in ['id','date','description','amount','currency']] for r in rows])
        self.assertEqual(observed,expected)
    def test_demo_expected_decisions(self):
        inputs=Path(__file__).resolve().parents[1]/'demo/inputs'
        with tempfile.TemporaryDirectory() as t:
            s=run(inputs,Path(t)/'out');self.assertEqual((s['extracted'],s['accepted'],s['review'],s['blocked_documents']),(9,5,4,1));self.assertEqual(s['totals'],{'COP':'30000.00','USD':'65.50'});self.assertTrue(any(x['code']=='declared_total_mismatch' for x in s['file_issues']))

if __name__=='__main__':unittest.main()
