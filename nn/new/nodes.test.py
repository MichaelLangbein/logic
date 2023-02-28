import unittest as ut
from nodes import Constant, Variable, derivative, eval, Sin, Add, Mult, MatMul, Exp, Sum
import numpy as np


class NodeTests(ut.TestCase):
    
    def testEval(self):
        var = Variable('x')
        val = var.eval({'x': 3.0})
        self.assertEqual(val, 3.0)

    def testAdd(self):
        var = Variable('x')
        two = Constant(2)
        sum = Add(var, two)
        v0 = { 'x': 3 }
        sumVal = sum.eval(v0)
        self.assertEqual(sumVal, 5)

        d_sum_d_x = derivative(sum, var, v0)
        self.assertEqual(d_sum_d_x, 1)

    def testMatMul(self):
        x = Variable('x')
        W = Variable('W')
        y = MatMul(W, x)
        s = Sum(y)

        at = {
            'x': np.random.random(3),
            'W': np.random.random((2, 3))
        }

        sVal = s.eval(at)
        self.assertAlmostEqual(sVal, np.sum(at['W'] @ at['x']))

        d_s_d_y = derivative(s, y, at)
        d_s_d_x = derivative(s, x, at)
        self.assertAlmostEqual(d_s_d_x, d_s_d_y @ at['W'].T)

    


if __name__ == '__main__':
    ut.main()