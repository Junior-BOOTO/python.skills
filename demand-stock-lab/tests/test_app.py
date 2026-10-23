import io
import unittest
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from engine import demo
APP=str(Path(__file__).resolve().parents[1]/'app.py')
class InterfaceTests(unittest.TestCase):
 def test_selection_and_stock(self):
  a=AppTest.from_file(APP).run()
  self.assertEqual(len(a.exception),0)
  self.assertEqual(len(a.metric),2)
  a.selectbox[0].select('B').run()
  self.assertEqual(len(a.exception),0)
  a.number_input[0].set_value(100000).run()
  self.assertEqual(a.metric[1].value,'0')
 def test_upload(self):
  with patch('streamlit.file_uploader',return_value=io.BytesIO(demo().to_csv(index=False).encode())):
   a=AppTest.from_file(APP).run()
  self.assertEqual(len(a.exception),0)
  self.assertEqual(len(a.error),0)
  self.assertEqual(len(a.metric),2)
 def test_invalid_upload(self):
  with patch('streamlit.file_uploader',return_value=io.BytesIO(b'date,product,sales\n')):
   a=AppTest.from_file(APP).run()
  self.assertEqual(len(a.exception),0)
  self.assertEqual(len(a.error),1)
if __name__=='__main__':unittest.main()
