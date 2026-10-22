import unittest, tempfile
from pathlib import Path
from portfolio.requirements import *
class RequirementsTests(unittest.TestCase):
    def test_fixture_statuses(self):
        req=parse_document('data/requirements.txt'); b=parse_document('data/supplier_b.txt')
        self.assertEqual([r['status'] for r in compare(req,b)],['exception','exception','unit_mismatch','unknown','missing','met'])
    def test_citation_and_abstention(self):
        index=Retriever(parse_document('data/supplier_a.txt'))
        self.assertIn('[supplier_a.txt:2]',index.answer('lead_time'))
        self.assertIn('Insufficient evidence',index.answer('xyzxyz'))
    def test_boundary_and_nonfinite(self):
        req=parse_document('data/requirements.txt')[:1]; r=dict(req[0],value='14')
        self.assertEqual(compare(req,[r])[0]['status'],'met')
        self.assertEqual(compare(req,[dict(r,value='NaN')])[0]['status'],'unknown')
    def test_parser_rejects_malformed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.txt';p.write_text('R01 | incomplete')
            with self.assertRaises(ValueError):parse_document(p)
