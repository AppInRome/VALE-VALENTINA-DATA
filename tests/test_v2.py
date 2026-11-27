import unittest,tempfile,pathlib
from reasoning.engine import percentage,change,compare
from conversation.context import followup
from semantic.fts import build,search
from connectors.public import token,datacommons
from validation.build_v2 import build as pack
class TestV2(unittest.TestCase):
    def test_percent(self):
        self.assertEqual(percentage(1,4),25)
        for a,b in [(1,0),(5,4),(-1,5),(True,5)]:
            with self.assertRaises(ValueError):percentage(a,b)
    def test_change(self):
        self.assertEqual(change(100,120),20)
        with self.assertRaises(ValueError):change(0,1)
    def test_comparison(self):
        with self.assertRaises(ValueError):compare({'value':1},{'value':2})
    def test_context(self):
        self.assertEqual(followup({'indicator':'births','territory':'Roma'},{'territory':'Milano'})['indicator'],'births')
        self.assertNotIn('filters',followup({'indicator':'births','filters':{}},{'indicator':'population'}))
    def test_fts(self):
        db=build([('1','ospedale','nosocomio salute'),('2','scuola','istruzione')])
        self.assertEqual(search(db,'nosocomio')[0][0],'1')
        self.assertEqual(search(db,'"""'),[])
    def test_token(self):
        for s in ['../x','https://example.com','a?b']:
            with self.assertRaises(ValueError):token(s)
    def test_pack(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/'pack'
            m=pack(p)
            self.assertEqual(m['schema'],2)
            self.assertEqual(len(m['files']),8)
            with self.assertRaises(ValueError):pack(p)
