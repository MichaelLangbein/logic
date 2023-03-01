import unittest as ut
from nodes import Constant, Variable, derivative, Sin, Add, Mult, MatMul, Exp, Sum
import numpy as np


class NodeTests(ut.TestCase):
    
    def testEval(self):
        var = Variable('x')
        val = var.eval({'x': np.array(3.0)})
        self.assertEqual(val, np.array(3.0))

    def testAdd(self):
        x = Variable('x')
        two = Constant(2)
        sum = Add(x, two)
        v0 = { 'x': np.array(3) }
        sumVal = sum.eval(v0)
        self.assertEqual(sumVal, np.array(5))

        d_sum_d_x = derivative(sum, x, v0)
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
        np.testing.assert_array_almost_equal(d_s_d_x, d_s_d_y @ at['W'])

    


if __name__ == '__main__':
    ut.main()