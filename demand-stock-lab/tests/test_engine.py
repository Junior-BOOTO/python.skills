import unittest
import numpy as np
from engine import demo,validate,run,forecast,order_quantity
class Tests(unittest.TestCase):
 def test_constant(self):
  np.testing.assert_equal(forecast([10]*112,'mean4'),[10]*4)
 def test_stock(self):
  self.assertEqual(order_quantity(100,20,10,5),75)
  self.assertEqual(order_quantity(10,100,0),0)
  with self.assertRaises(ValueError):order_quantity(1,-1,0)
 def test_bad_data(self):
  d=demo()
  with self.assertRaises(ValueError):validate(d.drop(index=5))
  with self.assertRaises(ValueError):validate(__import__('pandas').concat([d,d.iloc[:1]]))
 def test_pipeline(self):
  p,m=run(demo());self.assertEqual(len(p),12)
  self.assertTrue((p.forecast>=0).all());self.assertEqual(len(m),3)
 def test_future_not_used(self):
  # A forecast at an origin is unchanged by changes after that origin.
  y=demo().query("product=='A'").sales.to_numpy();a=forecast(y[:132],'ridge')
  y[132:]=99999;np.testing.assert_allclose(a,forecast(y[:132],'ridge'))
if __name__=='__main__':unittest.main()
