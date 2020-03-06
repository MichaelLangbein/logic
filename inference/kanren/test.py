import unittest
from inference.kanren.main import Var, run, eqR, andR, orR


class InferenceEngineTestCase(unittest.TestCase):

    @unittest.skip("known to work ...")
    def testAddition(self):
        self.assertTrue( 1 + 1 == 2 )


    def testSimpleEquals(self):
        x = Var('x')
        results = run([x], 
            eqR("someVal", "someVal")
        )
        self.assertTrue( results == [{}] )

        y = Var('y')
        results2 = run([y], 
            eqR("someVal", "otherVal")
        )
        self.assertTrue( results2 == [] )


    def testEquals(self):
        a = Var('a')
        results = run([a], 
            eqR(1, a)
        )
        self.assertTrue( results == [{a: 1}] )


    def testAnd(self):
        x = Var('x')
        y = Var('y')
        results = run([x, y],
            andR(
                eqR(x, y),
                eqR(y, 1)
            )
        )
        self.assertTrue( results == [{x: 1, y: 1}] )

        results2 = run([x],
            andR(
                eqR(x, y),
                eqR(y, 1)
            )
        )
        self.assertTrue( results2 == [{x: 1}] )


    def testContradiction(self):
        x = Var('x')
        results = run([x], 
            andR(
                eqR(x, 1),
                eqR(x, 2)
            )
        )
        self.assertTrue( results == [{}] )


    def testFusion(self):
        x = Var('x')
        y = Var('y')
        results = run([x], 
            eqR(x, y)
        )
        self.assertTrue( results == [{x: y}] )


    def testPeas(self):
        x = Var('x')
        results = run([x],
            eqR(["pea", "pod"], ["pea", x])
        )



if __name__ == '__main__':
    unittest.main()