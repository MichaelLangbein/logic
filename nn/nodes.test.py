import unittest as ut
from nodes import Constant, Variable, Plus, Sse, MatMul, Sigmoid, InnerSum, gradient
import numpy as np


class NodeTests(ut.TestCase):
    
    def testEval(self):
        var = Variable('x')
        val = var.eval({'x': np.array(3.0)})
        self.assertEqual(val, np.array(3.0))

    def testAdd(self):
        x = Variable('x')
        two = Constant(2)
        sum = Plus(x, two)
        at = { 'x': np.array(3) }
        sumVal = sum.eval(at)
        self.assertEqual(sumVal, np.array(5))

        grad_sum_x = gradient(sum, x, at)
        self.assertEqual(grad_sum_x, 1)

    def testMatMul(self):
        xVal = np.array([1, 2, 3])
        WVal = np.array([[1, 0, 2], [2, 1, 0]])
        yVal = WVal @ xVal
        sVal = np.sum(yVal)

        x = Variable('x')
        W = Variable('W')
        y = MatMul(W, x)
        s = InnerSum(y)

        at = {
            'x': xVal,
            'W': WVal
        }

        yEval = y.eval(at)
        np.testing.assert_array_almost_equal(yVal, yEval)
        sEval = s.eval(at)
        self.assertAlmostEqual(sVal, sEval)

        grad_s_y = gradient(s, y, at)
        self.assertEqual(grad_s_y.shape, yVal.shape)
        np.testing.assert_array_almost_equal(grad_s_y, np.array([1.0, 1.0]))

        grad_s_x = gradient(s, x, at)
        self.assertEqual(grad_s_x.shape, xVal.shape)
        np.testing.assert_array_almost_equal(grad_s_x, np.array([3.0, 1.0, 2.0]))

        grad_s_W = gradient(s, W, at)
        self.assertEqual(grad_s_W.shape, WVal.shape)
        np.testing.assert_array_almost_equal(grad_s_W, np.array([xVal, xVal]))


    def testSigmoidAndSse(self):
        iTrue = np.array([1, 2, 3])
        WTrue = np.array([[1, 0, 2], [2, 1, 0]])
        WSim  = np.array([[1, 1, 1], [1, 1, 1]])
        xTrue = np.dot(WTrue, iTrue)
        yTrue = 1.0 / (1.0 + np.exp(-xTrue))
        xSim  = np.dot(WSim, iTrue)
        ySim  = 1.0 / (1.0 + np.exp(-xSim))
        sseTrue = np.dot(ySim - yTrue, ySim - yTrue)

        i = Variable('i')
        W = Variable('W')
        yObs = Variable('yObs')
        x = MatMul(W, i)
        y = Sigmoid(x)
        sse = Sse(yObs, y)

        at = { 'i': iTrue, 'W': WSim, 'yObs': yTrue }
        outputEVal = y.eval(at)
        np.testing.assert_array_almost_equal(outputEVal, ySim)
        sseEval = sse.eval(at)
        np.testing.assert_array_almost_equal(sseEval, sseTrue)

        grad_e_i = gradient(sse, i, at)
        self.assertEqual(grad_e_i.shape, iTrue.shape)
        grad_e_W = gradient(sse, W, at)
        self.assertEqual(grad_e_W.shape, WTrue.shape)

    


if __name__ == '__main__':
    ut.main()