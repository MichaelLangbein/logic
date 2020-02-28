import unittest
from inference.kanren.main import Var, run, eqR, andR, orR


class InferenceEngineTestCase(unittest.TestCase):

    def testEquals(self):
        a = Var('a')
        results = run(
            eqR(1, a)
        )
        self.assertTrue( results == [{a: 1}] )

    
    def testAnd(self):
        x = Var('x')
        y = Var('y')
        results = run(
            andR(
                eqR(x, y),
                eqR(y, 1)
            )
        )
        self.assertTrue( results == [{x: 1, y: 1}] )


if __name__ == '__main__':
    unittest.main()