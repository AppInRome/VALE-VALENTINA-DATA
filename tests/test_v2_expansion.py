import unittest
from semantic.expand_catalog import expand
from benchmarks.generate import cases
class Expansion(unittest.TestCase):
    def test_catalog(self):
        x=expand()
        self.assertEqual(sum(c.get('kind')=='indicator' for c in x['concepts']),141)
        ids={c['id'] for c in x['concepts']}
        self.assertTrue(all(e['from'] in ids and e['to'] in ids for e in x['edges']))
    def test_cases(self):
        self.assertEqual(len(cases()),564)
        self.assertEqual(len({c['question'] for c in cases()}),564)
