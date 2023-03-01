import unittest as ut
import numpy as np
from nn import Sigmoid, Sse
from nodes import InnerSum, MatMul, Variable, gradient



class NnTests(ut.TestCase):
    

    def testBasics(self):
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
        x = MatMul(W, i)
        y = Sigmoid(x)
        sse = Sse(yTrue, y)

        at = { 'i': iTrue, 'W': WSim }
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