import unittest
from inference.kanren.pykanren import Var, run, eqR, andR, orR


class InferenceEngineTestCase(unittest.TestCase):

    def testEquals(self):
        results = run(
            eqR(1, Var('a'))
        )
        self.assertTrue( results == [{'a': 1}] )

    
    def testAnd(self):
        results = run(
            andR(
                eqR(Var('x'), Var('y')),
                eqR(Var('y'), 1)
            )
        )
        self.assertTrue( results == [{'x': 1, 'y': 1}] )
