import unittest as ut
import numpy as np
from tensor import Tensor, eye
from autodiff import Add, Exp, InnerSum, Mult, PwProd, PwDiv, Variable, ScalarMult, Sigmoid, Softmax, SSE, ScalarPower


class AutodiffTests(ut.TestCase):
    """
        https://explained.ai/np.array-calculus/
    """

    def setUp(self):
        return super().setUp()

    def _arraysClose(self, arr1: np.array, arr2: np.array, threshold = 0.001):
        if arr1.shape != arr2.shape:
            print("Dimensions don't match", arr1.shape, arr2.shape)
            return False
        diff = np.max(np.abs(arr1 - arr2))
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

    
    def testAssertClose(self):
        return self.assertClose(np.array([
            [1, 2],
            [2, 1]
        ]), np.array([
            [1, 2],
            [2, 1]
        ]))

    def testDiffBySelf(self):
        """
            du/du = eye
        """
        u = Variable(Tensor([1, 2, 3]))
        dudu = u.diff(u)
        self.assertEqual(dudu.asArray(), eye(3, 3))

    def testSum(self):
        """
            s = u + v
            ds/du = eye
            ds/dv = eye
        """
        u = Variable(Tensor([1, 2, 3]))
        v = Variable(Tensor([2, 3, 4]))
        s = Add(u, v)
        sVal = s.eval()
        dSdu = s.diff(u)
        dSdv = s.diff(v)
        self.assertClose(sVal.asArray(), [3, 5, 7])
        self.assertClose(dSdu.asArray(), eye(3, 3))
        self.assertClose(dSdv.asArray(), eye(3, 3))

    def testInnerSum(self):
        """
            i = InnerSum(u)
            di/du = 1^T
        """
        u = Variable(Tensor([1, 2, 3]))
        i = InnerSum(u)
        iVal = i.eval()
        dIdu = i.diff(u)
        self.assertClose(iVal, 6)
        self.assertClose(dIdu, Tensor([1, 1, 1]))

        v = Variable(Tensor([2, 3, 4]))
        s = Add(u, v)
        si = InnerSum(s)
        dsidv = si.diff(v)
        self.assertClose(dsidv, Tensor([1, 1, 1]))

    def testNestedExpression(self):
        """
            sv = u + v
            si = Sum(sv)
            dsi/du = dsi/dsv * dsv/du
                   = 1_1xn * 1_nxn
                   = 1_1xn 
        """
        u = Variable(Tensor([1, 2, 3]))
        v = Variable(Tensor([2, 3, 4]))
        sv = Add(u, v)
        si = InnerSum(sv)
        dsidu = si.diff(u)
        self.assertClose(dsidu, Tensor([1, 1, 1]))
    
    def testMatrixVectorMult(self):
        v = Variable(Tensor([1., 2.]))
        M = Variable(Tensor([1., 2.], [2., 1.]))
        p = Mult(M, v)
        pVal = p.eval()
        pDifV = p.diff(v)
        pDifM = p.diff(M)

        pExpected = Tensor([5, 4])
        self.assertClose(pVal, pExpected)
        self.assertClose(pDifV, M.value)
        self.assertClose(pDifM, v.value)

    def testExp(self):
        """
            de^u/du = eye(e^ui)
            de^u/dx = de^u/du du/dx
                    = eye(e^ui) du/dx
        """
        u = Variable(Tensor([1, 2, 3]))
        e = Exp(u)
        dedu = e.diff(u)
        self.assertClose(dedu, Tensor(
            [np.exp(1), 0, 0],
            [0, np.exp(2), 0],
            [0, 0, np.exp(3)],
        ))

        v = Variable(Tensor([2, 3, 4]))
        e2 = Exp(Add(u, v))
        de2dv = e2.diff(v)
        self.assertClose(de2dv, Tensor(
            [np.exp(1 + 2), 0, 0],
            [0, np.exp(2 + 3), 0],
            [0, 0, np.exp(3 + 4)],
        ))
    
    def testProd(self):
        """
            d/dx uv = (du/dx)^T v  + (dv/dx)^T u
            d/du uv = (du/du)^T v
                    = eye() v
                    = eye(v)
        """
        u = Variable(Tensor([1, 2, 3]))
        v = Variable(Tensor([2, 3, 4]))
        p = PwProd(u, v)
        dpdu = p.diff(u)
        self.assertClose(dpdu, Tensor(
            [2, 0, 0],
            [0, 3, 0],
            [0, 0, 4]
        ))


        """
            d/du (u+v)*v = (d/du u+v)^T v  +  (u+v) (d/du  v)^T
                         = (d/du u+v)^T v
                         = (d/du u)^T v
                         = eye() v
                         = eye(v)
        """
        s = Add(u, v)
        p2 = PwProd(s, v)
        dp2du = p2.diff(u)
        self.assertClose(dp2du, Tensor(
            [2, 0, 0],
            [0, 3, 0],
            [0, 0, 4]
        ))

    def testPwDiv(self):
        u = Variable(Tensor([1, 2, 3]))
        v = Variable(Tensor([2, 3, 4]))
        d = PwDiv(u, v)
        dddu = d.diff(u)
        self.assertClose(dddu, Tensor(
            [1/2, 0, 0],
            [0, 1/3, 0],
            [0, 0, 1/4]
        ))
        dddv = d.diff(v)
        self.assertClose(dddv, Tensor(
            [-1/(2**2), 0, 0],
            [0, -2/(3**2), 0],
            [0, 0, -3/(4**2)]
        ))


    def testScalarPow(self):
        x = Tensor([1, 2])
        x2 = x**2

        xV = Variable(x)
        x2V = ScalarPower(xV, 2)

        x2val = x2V.eval()
        x2dx = x2V.diff(xV)

        self.assertClose(x2val, x2)
        self.assertClose(x2dx, np.diag(2*x))


    def testSigmoid(self):
        def sig(x):
            return 1 / (1 + np.exp(-x))
        
        def dsig(x):
            return np.diag(sig(x) * (1 - sig(x)))

        data = Tensor([0, 1000])

        x = Variable(data)
        s = Sigmoid(x)
        sVal = s.eval()
        sDif = s.diff(x)

        self.assertClose(sVal, sig(data))
        self.assertClose(sDif, dsig(data))

    def testSoftmax(self):
        def sm(x):
            return np.exp(x) / np.sum(np.exp(x))

        data = Tensor([0.6, 1.0])

        x = Variable(data)
        s = Softmax(x)
        sVal = s.eval()
        sDif = s.diff(x)
        self.assertClose(np.sum(sVal), 1.0)
        self.assertClose(sVal, sm(data))

    def testSSE(self):
        def sse(ySim, yObs):
            return np.sum((ySim - yObs)**2)

        x = Tensor([1, 2, 3])
        ySim = 2 * x
        yObs = x**2
        sseObs = sse(ySim, yObs)

        xV = Variable(x)
        ySimV = ScalarMult(2, xV)
        sseV = SSE(ySimV, yObs)

        sseVal = sseV.eval()
        sseDx = sseV.diff(xV)
        sseDy = sseV.diff(ySimV)

        self.assertClose(sseVal, sseObs)

        betterYSimV = ScalarPower(xV, 2)
        betterSseV = SSE(betterYSimV, yObs)
        betterSseVal = betterSseV.eval()
        betterSseDx = betterSseV.diff(xV)
        betterSseDy = betterSseV.diff(ySimV)

        self.assertClose(betterSseVal, 0)
        self.assertClose(betterSseDx, Tensor([0, 0, 0]))


    def testNotTooDeep(self):
        """
            y = a*b
            z = c + y
            dz/dy = ddy(c + y)
                  = 0 + dy/dy
                    .... good:
                        = 1.0
                    .... bad:
                        = ddy (a*b) 
                        = da/dy b + a db/dy
                        = 0*b + a*0
                        = 0
        """
        a = Variable(Tensor([1]))
        b = Variable(Tensor([2]))
        c = Variable(Tensor([3]))
        y = Mult(a, b)
        z = Add(c, y)
        dzdy = z.diff(y)
        self.assertClose(np.squeeze(dzdy), np.array(1.0))


    def testEffectiveExpressionEquality(self):
        a = Variable(Tensor([1]))
        b = Variable(Tensor([2]))
        c1 = Mult(a, b)
        c2 = Mult(a, b)
        # c1 and c1 live at different memory-adresses,
        # so conventionally c1 != c2.
        # Only evaluates to equal if
        # autodiff has a concept of expression-equality.
        self.assertEqual(c1, c2)


    def testNotTooDeepWithNewVariable(self):
        """
            y = a*b
            z = c + y
            dz/dy = ddy(c + y)
                  = 0 + dy/dy
                    .... good:
                        = 1.0
                    .... bad:
                        = ddy (a*b) 
                        = da/dy b + a db/dy
                        = 0*b + a*0
                        = 0
        """
        a = Variable(Tensor([1]))
        b = Variable(Tensor([2]))
        c = Variable(Tensor([3]))
        y = Mult(a, b)
        z = Add(c, y)
        y2 = Mult(a, b)
        dzdy = z.diff(y2)
        self.assertClose(np.squeeze(dzdy), np.array(1.0))
    




if __name__ == '__main__':
    ut.main()


