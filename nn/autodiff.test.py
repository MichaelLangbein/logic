import unittest as ut
import numpy as np
from autodiff import Add, Exp, InnerSum, Mult, PwProd, PwDiv, Variable, Sigmoid, Softmax


class AutodiffTests(ut.TestCase):
    """
        https://explained.ai/np.array-calculus/
    """

    def setUp(self):
        return super().setUp()

    def _arraysClose(self, arr1, arr2, threshold = 0.001):
        if arr1.shape != arr2.shape:
            print('Dimensions dont match', arr1.shape, arr2.shape)
            return False
        diff = np.abs(np.sum(arr1 - arr2))
        if diff >= threshold:
            print("values unequal: ", arr1, arr2)
            return False
        return True

    def _valuesClose(self, v1, v2, threshold = 0.001):
        diff = np.abs(v1 - v2)
        if diff >= threshold:
            print(v1, " != ", v2)
            return False
        return True

    def assertClose(self, v1, v2, threshold = 0.001):
        if hasattr(v1, "__len__"):
            return self.assertTrue(self._arraysClose(v1, v2, threshold))
        return self.assertTrue(self._valuesClose(v1, v2, threshold))

    def testDiffBySelf(self):
        """
            du/du = eye
        """
        u = Variable(np.array([1, 2, 3]))
        dudu = u.diff(u)
        self.assertClose(dudu, np.eye(3))

    def testSum(self):
        """
            s = u + v
            ds/du = eye
            ds/dv = eye
        """
        u = Variable(np.array([1, 2, 3]))
        v = Variable(np.array([2, 3, 4]))
        s = Add(u, v)
        sVal = s.eval()
        dSdu = s.diff(u)
        dSdv = s.diff(v)
        self.assertClose(sVal, np.array([3, 5, 7]))
        self.assertClose(dSdu, np.eye(3, 3))
        self.assertClose(dSdv, np.eye(3, 3))

    def testInnerSum(self):
        """
            i = InnerSum(u)
            di/du = 1^T
        """
        u = Variable(np.array([1, 2, 3]))
        i = InnerSum(u)
        iVal = i.eval()
        dIdu = i.diff(u)
        self.assertClose(iVal, 6)
        self.assertClose(dIdu, np.array([1, 1, 1]))

        v = Variable(np.array([2, 3, 4]))
        s = Add(u, v)
        si = InnerSum(s)
        dsidv = si.diff(v)
        self.assertClose(dsidv, np.array([1, 1, 1]))

    def testNestedExpression(self):
        """
            sv = u + v
            si = Sum(sv)
            dsi/du = dsi/dsv * dsv/du
                   = 1_1xn * 1_nxn
                   = 1_1xn 
        """
        u = Variable(np.array([1, 2, 3]))
        v = Variable(np.array([2, 3, 4]))
        sv = Add(u, v)
        si = InnerSum(sv)
        dsidu = si.diff(u)
        self.assertClose(dsidu, np.array([1, 1, 1]))

    def testExp(self):
        """
            de^u/du = eye(e^ui)
            de^u/dx = de^u/du du/dx
                    = eye(e^ui) du/dx
        """
        u = Variable(np.array([1, 2, 3]))
        e = Exp(u)
        dedu = e.diff(u)
        self.assertClose(dedu, np.array([
            [np.exp(1), 0, 0],
            [0, np.exp(2), 0],
            [0, 0, np.exp(3)],
        ]))

        v = Variable(np.array([2, 3, 4]))
        e2 = Exp(Add(u, v))
        de2dv = e2.diff(v)
        self.assertClose(de2dv, np.array([
            [np.exp(1 + 2), 0, 0],
            [0, np.exp(2 + 3), 0],
            [0, 0, np.exp(3 + 4)],
        ]))
    
    def testProd(self):
        """
            d/dx uv = (du/dx)^T v  + (dv/dx)^T u
            d/du uv = (du/du)^T v
                    = eye() v
                    = eye(v)
        """
        u = Variable(np.array([1, 2, 3]))
        v = Variable(np.array([2, 3, 4]))
        p = PwProd([u, v])
        dpdu = p.diff(u)
        self.assertClose(dpdu, np.array([
            [2, 0, 0],
            [0, 3, 0],
            [0, 0, 4]
        ]))

        """
            d/du (u+v)*v = (d/du u+v)^T v  +  (u+v) (d/du  v)^T
                         = (d/du u+v)^T v
                         = (d/du u)^T v
                         = eye() v
                         = eye(v)
        """
        s = Add(u, v)
        p2 = PwProd([s, v])
        dp2du = p2.diff(u)
        self.assertClose(dp2du, np.array([
            [2, 0, 0],
            [0, 3, 0],
            [0, 0, 4]
        ]))

    def testDiv(self):
        u = Variable(np.array([1, 2, 3]))
        v = Variable(np.array([2, 3, 4]))
        d = PwDiv(u, v)
        dddu = d.diff(u)
        self.assertClose(dddu, np.array([
            [1/2, 0, 0],
            [0, 1/3, 0],
            [0, 0, 1/4]
        ]))
        dddv = d.diff(v)
        self.assertClose(dddv, np.array([
            [-1/(2**2), 0, 0],
            [0, -2/(3**2), 0],
            [0, 0, -3/(4**2)]
        ]))

    def testSigmoid(self):
        x = Variable(np.array([0, 1000]))
        s = Sigmoid(x)
        sVal = s.eval()
        sDif = s.diff(x)
        self.assertClose(sVal, np.array([0.5, 1.0]))
        self.assertClose(sDif, np.array([
            [0.25, 0],
            [0, 0]
        ]))

    def testSoftmax(self):
        x = Variable(np.array([0.6, 1.0]))
        s = Softmax(x)
        sVal = s.eval()
        sDif = s.diff(x)
        self.assertClose(np.sum(sVal), 1.0)

    def testMatrixVectorMult(self):
        v = Variable(np.array([1, 2]))
        M = Variable(np.array([[1, 2], [2, 1]]))
        p = Mult(M, v)
        pVal = p.eval()
        pDifV = p.diff(v)
        pDifM = p.diff(M)

        pExpected = np.array([5, 4])
        self.assertClose(pVal, pExpected)
        self.assertClose(pDifV, M.value)
        self.assertClose(pDifM, v.value)



if __name__ == '__main__':
    ut.main()


