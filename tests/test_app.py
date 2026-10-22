import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
class AppTests(unittest.TestCase):
    def test_dashboard_starts(self):
        app=AppTest.from_file(Path(__file__).resolve().parents[1]/'app.py').run(timeout=30)
        self.assertEqual(len(app.exception),0,str(app.exception))

    def test_supplier_change_and_abstention(self):
        app=AppTest.from_file(Path(__file__).resolve().parents[1]/'app.py').run()
        app.selectbox[0].select('supplier_b').run()
        app.text_input[0].set_value('xyzxyz').run()
        self.assertIn('Insufficient evidence',app.text[0].value)
        self.assertEqual(len(app.exception),0)
