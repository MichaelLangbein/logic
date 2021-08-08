import unittest
from inference.kanren.main import Var, run, eqR, andR, orR


class InferenceEngineTestCase(unittest.TestCase):

    @unittest.skip("known to work ...")
    def testAddition(self):
        self.assertEqual( 1 + 1, 2 )


    def testSimpleEquals(self):
        x = Var('x')
        results = run([x], 
            eqR("someVal", "someVal")
        )
        self.assertEqual( results, [{}] )

        y = Var('y')
        results2 = run([y], 
            eqR("someVal", "otherVal")
        )
        self.assertEqual( results2, [] )


    def testEquals(self):
        a = Var('a')
        results = run([a], 
            eqR(1, a)
        )
        self.assertEqual( results, [{a: 1}] )


    def testAnd(self):
        x = Var('x')
        y = Var('y')
        results = run([x, y],
            andR(
                eqR(x, y),
                eqR(y, 1)
            )
        )
        self.assertEqual( results, [{x: 1, y: 1}] )

        results2 = run([x],
            andR(
                eqR(x, y),
                eqR(y, 1)
            )
        )
        self.assertEqual( results2, [{x: 1}] )


    def testContradiction(self):
        x = Var('x')
        results = run([x], 
            andR(
                eqR(x, 1),
                eqR(x, 2)
            )
        )
        self.assertEqual( results, [] )


    def testFusion(self):
        x = Var('x')
        y = Var('y')
        results = run([x], 
            eqR(x, y)
        )
        self.assertEqual( results, [{x: y}] )


    def testLists(self):
        x = Var('x')
        results = run([x],
            eqR(["pea", "pod"],  x)
        )
        self.assertEqual( results, [{x: ["pea", "pod"]}] )

    
    def testLists2(self):
        x = Var('x')
        results = run([x],
            eqR(["pea", "pod"],  ["pea", x])
        )
        self.assertEqual( results, [{x: "pod"}] )


        



if __name__ == '__main__':
    unittest.main()