import copy,json,tempfile,unittest
from pathlib import Path
from decimal import Decimal
from transfer_cost.core import quote,compare,validate_rates
from transfer_cost.collect import parse_response
from transfer_cost.render import render,export
class CostTests(unittest.TestCase):
 def setUp(self):
  self.config=json.loads(Path('data/scenarios.json').read_text());self.rates=json.loads(Path('data/rates-synthetic.json').read_text());self.tariff={'sender_fixed':'0','sender_percent':'0','fx_margin_percent':'0','receiver_fixed':'0'}
 def test_zero_fees(self):
  r=quote('100.00','4000',self.tariff);self.assertEqual(Decimal(r['received']),400000);self.assertEqual(Decimal(r['reference_gap_target']),0)
 def test_total_budget_with_fixed_fee(self):
  self.tariff['sender_fixed']='5';r=quote('100.00','18',self.tariff);self.assertEqual(Decimal(r['principal']),95);self.assertEqual(Decimal(r['spent']),100)
 def test_percent_on_principal(self):
  self.tariff['sender_percent']='2';r=quote('100.00','18',self.tariff);self.assertEqual(Decimal(r['principal']),Decimal('98.03'));self.assertEqual(Decimal(r['sender_variable']),Decimal('1.96'));self.assertEqual(Decimal(r['unspent']),Decimal('0.01'))
 def test_margin_receiver_units(self):
  self.tariff.update(fx_margin_percent='10',receiver_fixed='10');r=quote('100.00','18',self.tariff);self.assertEqual(Decimal(r['effective_rate']),Decimal('16.2'));self.assertEqual(Decimal(r['received']),1610)
 def test_exact_decomposition(self):
  self.tariff.update(sender_fixed='2',sender_percent='1',fx_margin_percent='1.5',receiver_fixed='17');r=quote('100.00','18.12345',self.tariff)
  total=sum(Decimal(r[k]) for k in ('source_fee_effect_target','unspent_effect_target','fx_margin_effect_target','receiver_fixed','rounding_effect_target'));self.assertEqual(total,Decimal(r['reference_gap_target']))
 def test_rounding_half_up(self):self.assertEqual(Decimal(quote('1.00','1.005',self.tariff)['received']),Decimal('1.01'))
 def test_never_exceed_budget(self):
  for amount in ('0.01','1.00','100.00','9999.99'):
   for pct in ('0','0.1','2','99'):
    self.tariff['sender_percent']=pct
    try:r=quote(amount,'4000',self.tariff)
    except ValueError:continue
    self.assertLessEqual(Decimal(r['spent']),Decimal(amount))
 def test_invalid_numbers(self):
  for amount in ('NaN','Infinity','-1',100.0):
   with self.assertRaises(ValueError):quote(amount,'18',self.tariff)
 def test_invalid_rate_margin(self):
  with self.assertRaises(ValueError):quote('100.00','0',self.tariff)
  self.tariff['fx_margin_percent']='100'
  with self.assertRaises(ValueError):quote('100.00','18',self.tariff)
 def test_infeasible_fees(self):
  self.tariff['sender_fixed']='100'
  with self.assertRaises(ValueError):quote('100.00','18',self.tariff)
  self.tariff.update(sender_fixed='0',receiver_fixed='1801')
  with self.assertRaises(ValueError):quote('100.00','18',self.tariff)
 def test_precision(self):
  with self.assertRaises(ValueError):quote('1.001','18',self.tariff)
 def test_ties(self):
  c=copy.deepcopy(self.config);p=c['corridors'][0];p['tariffs'][1].update({k:p['tariffs'][0][k] for k in self.tariff});r=compare(c,self.rates,'2025-01-01');ranks={x['profile']:x['rank'] for x in r['corridors'][0]['comparisons'][1]['ranked']};self.assertEqual(ranks['A'],ranks['B'])
 def test_rank_changes(self):
  c=compare(self.config,self.rates,'2025-01-01')['corridors'][0]['comparisons'];self.assertEqual(c[0]['best_profiles'],['C']);self.assertEqual(c[2]['best_profiles'],['A'])
 def test_missing_pair(self):
  self.rates['rates']=self.rates['rates'][1:];r=compare(self.config,self.rates,'2025-01-01');self.assertEqual(r['corridors'][0]['status'],'reference_missing');self.assertEqual(r['corridors'][0]['comparisons'],[])
 def test_future_stale_dates(self):
  with self.assertRaises(ValueError):compare(self.config,self.rates,'2024-12-31')
  self.assertTrue(compare(self.config,self.rates,'2025-01-10')['corridors'][0]['reference_stale'])
 def test_duplicate_pairs(self):
  self.rates['rates'].append(copy.deepcopy(self.rates['rates'][0]))
  with self.assertRaises(ValueError):validate_rates(self.rates)
 def test_reference_provenance_missing_quote(self):
  r=parse_response([{'base':'USD','quote':'ZAR','rate':'18.123','date':'2026-10-09'}],'USD',['ZAR','COP'],'url','date');self.assertEqual(r['missing_quotes'],['COP']);self.assertEqual(r['rates'][0]['data_kind'],'public_reference')
 def test_wrong_pair_duplicate_response(self):
  rows=[{'base':'EUR','quote':'ZAR','rate':'18','date':'2026-10-09'}]
  with self.assertRaises(ValueError):parse_response(rows,'USD',['ZAR'],'url','date')
  rows[0]['base']='USD'
  with self.assertRaises(ValueError):parse_response(rows*2,'USD',['ZAR'],'url','date')
 def test_infeasible_not_ranked(self):
  self.config['corridors'][0]['tariffs'][0]['sender_fixed']='9999';c=compare(self.config,self.rates,'2025-01-01')['corridors'][0]['comparisons'][0];self.assertEqual(len(c['infeasible']),1);self.assertNotIn('A',[x['profile'] for x in c['ranked']])
 def test_html_escape_exports(self):
  self.config['corridors'][0]['tariffs'][0]['label']='<script>alert(1)</script>';r=compare(self.config,self.rates,'2025-01-01');h=render(r);self.assertIn('&lt;script&gt;',h);self.assertNotIn('<script>alert(1)',h)
  with tempfile.TemporaryDirectory() as tmp:export(r,tmp);self.assertEqual(json.loads((Path(tmp)/'comparison.json').read_text())['summary']['calculated_quotes'],27)
if __name__=='__main__':unittest.main()
