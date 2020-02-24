import unittest
from inference.kanren.pykanren import Var, Goal, Relation, run, eqR, andR, orR


class InferenceEngineTestCase(unittest.TestCase):

    def testEquals(self):
        results = run(
            eqR(1, Var('a'))
        )
        self.assertTrue( results == [{'a': 1}] )

    
    def testAnd(self):
        pass
