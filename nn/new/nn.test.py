import unittest as ut
import numpy as np
from nodes import Variable, MatMul, Plus, Sigmoid, Sse, gradient



class NnTests(ut.TestCase):
   
    def testPrimitive(self):

        i = Variable('i')
        yObs = Variable('yObs')

        W1 = Variable('W1')
        b1 = Variable('b1')
        x1 = MatMul(W1, Plus(i, b1))
        y1 = Sigmoid(x1)

        W2 = Variable('W2')
        b2 = Variable('b2')
        x2 = MatMul(W2, Plus(y1, b2))
        y2 = Sigmoid(x2)

        e = Sse(yObs, y2)

        values = {
            'i':    np.random.random([3]),
            'b1':   np.random.random([3]),
            'W1':   np.random.random([2, 3]),
            'b2':   np.random.random([2]),
            'W2':   np.random.random([2, 2]),
            'yObs': np.random.random([2])
        }

        e0 = e.eval(values)

        alpha = 0.01
        for i in range(30):
            dedW2 = gradient(e, W2, values)
            dedb2 = gradient(e, x2, values)
            dedW1 = gradient(e, W1, values)
            dedb1 = gradient(e, x1, values)
            values['W2'] -= alpha * dedW2
            values['b2'] -= alpha * dedb2
            values['W1'] -= alpha * dedW1
            values['b1'] -= alpha * dedb1

            ei = e.eval(values)
            print(f"{i/30} - {ei}")

        self.assertLess(ei, e0)

        



if __name__ == '__main__':
    ut.main()