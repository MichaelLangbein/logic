import unittest
from inference.kanren.main import Var, run, runN, eqR, andR, orR
from inference.kanren.algebra import addR, minR, multR, quotR

class AlgebraEngineTestCase(unittest.TestCase):

    def testRatio(self):
        goldenRatio = 1.618
        x = Var('x')
        y = Var('y')
        results = runN(5, [x, y], 
            quotR(x, y, goldenRatio)
        )
        self.assertTrue(results)



if __name__ == '__main__':
    unittest.main()