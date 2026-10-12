import unittest,sys,json
from pathlib import Path
import pandas as pd,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import signals,connected_components,rank_metrics
class EvidenceChecks(unittest.TestCase):
 def frame(self,times):
  f=pd.DataFrame([{'transaction_id':f'T{i}','sender_id':a,'recipient_id':b,'amount':100.,'parsed_time':pd.Timestamp('2025-01-01',tz='UTC')+pd.Timedelta(minutes=t)} for i,(a,b,t) in enumerate(zip(['A','B','C'],['B','C','A'],times))]);return f
 def test_cycle_requires_temporal_order(self):
  sig,cycles,_=signals(self.frame([0,5,10]));self.assertEqual(sig['temporal_cycles'],1);self.assertEqual(list(cycles[0]),['T0','T1','T2'])
  sig,_,_=signals(self.frame([0,0,0]));self.assertEqual(sig['temporal_cycles'],0)
 def test_reverse_time_not_claimed_as_path(self):
  sig,cycles,_=signals(self.frame([0,20,10]));self.assertEqual(cycles,[])
 def test_equal_alert_budget(self):
  y=np.array([0,1,0,1,0,0,1,0,0,0]);a=rank_metrics(y,np.arange(10),.2);b=rank_metrics(y,np.arange(10)[::-1],.2);self.assertEqual(a['alert_budget'],b['alert_budget']);self.assertEqual(a['alert_budget'],2)
 def test_connected_components_ignore_lexical_ids(self):
  df=pd.DataFrame({'sender_id':['A','B','Z'],'recipient_id':['B','C','Y']});groups=connected_components(df);self.assertEqual({frozenset(g) for g in groups},{frozenset('ABC'),frozenset('ZY')})
 def test_all_evidence_is_grounded_in_rows(self):
  root=Path(__file__).resolve().parents[1];cases=json.loads((root/'analysis/cases.json').read_text())
  for c in cases:
   tx={t['transaction_id']:t for t in c['transactions']}
   self.assertEqual(c['quality']['missing_timestamps'],sum(not t['timestamp'] for t in tx.values()))
   for reason in c['reasons']:
    evidence=[tx[i] for i in reason['ids']]
    for a,b in zip(evidence,evidence[1:]):
     self.assertEqual(a['recipient_id'],b['sender_id']);self.assertLess(pd.Timestamp(a['timestamp']),pd.Timestamp(b['timestamp']))
     self.assertLessEqual((pd.Timestamp(b['timestamp'])-pd.Timestamp(a['timestamp'])).total_seconds(),600)
 def test_no_labels_ids_or_quality_in_model_features(self):
  root=Path(__file__).resolve().parents[1];m=json.loads((root/'models/metrics.json').read_text())
  for names in m['features'].values():self.assertFalse(set(names)&{'scenario','injected_anomaly','case_id','country','currency','missing_time_rate'})
if __name__=='__main__':unittest.main()
