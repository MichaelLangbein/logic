import unittest as ut
import numpy as np
from autodiff import Add, Exp, InnerSum, PwProd, PwDiv, Variable, ScalarMult, Sigmoid, Softmax, SSE, ScalarPower
from helpers import eye, isZero


class AutodiffTests(ut.TestCase):
    """
        https://explained.ai/np.array-calculus/
    """

    def setUp(self):
        return super().setUp()

    def _arraysClose(self, arr1, arr2, threshold = 0.001):
        for i in range(len(arr2)):
            row1 = arr1[i]
            row2 = arr2[i]
            if hasattr(row1, "__len__"):
                close = self._arraysClose(row1, row2, threshold)
                if not close:
                    return False
            else:
                diff = abs(row2 - row1)
                if diff > threshold:
                    print("values unequal: ", arr1, arr2)
                    return False
        return True

    def _valuesClose(self, v1, v2, threshold = 0.001):
        diff = np.abs(v1 - v2)
        if diff >= threshold:
            print(v1, " != ", v2)
            return False
        return True

    def _tensorsClose(self, v1, v2, threshold = 0.001):
        a1 = v1.tolist()
        a2 = v2.tolist()
        return self._arraysClose(a1, a2, threshold)

    def assertClose(self, v1, v2, threshold = 0.001):
        if hasattr(v1, "__len__"):
            return self.assertTrue(self._arraysClose(v1, v2, threshold))
        return self.assertTrue(self._valuesClose(v1, v2, threshold))

    
    def testAssertClose(self):
        return self.assertClose([
            [1, 2],
            [2, 1]
        ], [
            [1, 2],
            [2, 1]
        ])

    def testDiffBySelf(self):
        """
            du/du = eye
        """
        u = Variable(np.array([1, 2, 3]))
        dudu = u.grad(u)
        self.assertEqual(dudu.tolist(), eye((3, 3)))

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
        dSdu = s.grad(u)
        dSdv = s.grad(v)
        self.assertClose(sVal.tolist(), [3, 5, 7])
        self.assertClose(dSdu.tolist(), eye((3, 3)))
        self.assertClose(dSdv.tolist(), eye((3, 3)))

    def testInnerSum(self):
        """
            i = InnerSum(u)
            di/du = 1^T
        """
        u = Variable(np.array([1, 2, 3]))
        i = InnerSum(u)
        iVal = i.eval()
        dIdu = i.grad(u)
        self.assertAlmostEqual(iVal, np.array(6))
        self.assertClose(dIdu, np.array([1, 1, 1]))

        v = Variable(np.array([2, 3, 4]))
        s = Add(u, v)
        si = InnerSum(s)
        dsidv = si.grad(v)
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
        dsidu = si.grad(u)
        self.assertClose(dsidu, np.array([1, 1, 1]))
    
    def testMatrixVectorMult(self):
        """
        p = Mv
        dp/dv = M
        dp/dM: (2x2x2)
        """
        v = Variable(np.array([1., 2.]))
        M = Variable(np.array([[1., 2.], [3., 4.]]))
        p = Mult(M, v)
        pVal = p.eval()
        grad_p_V = p.grad(v)
        grad_p_M = p.grad(M)

        pExpected = np.array([5, 11])
        self.assertClose(pVal, pExpected)
        self.assertClose(grad_p_M.shape, [2, 2, 2])

    def testExp(self):
        """
            de^u/du = eye(e^ui)
            de^u/dx = de^u/du du/dx
                    = eye(e^ui) du/dx
        """
        u = Variable(np.array([1, 2, 3]))
        e = Exp(u)
        dedu = e.grad(u)
        self.assertClose(dedu.tolist(),[
            [np.exp(1), 0, 0],
            [0, np.exp(2), 0],
            [0, 0, np.exp(3)],
        ])

        v = Variable(np.array([2, 3, 4]))
        e2 = Exp(Add(u, v))
        de2dv = e2.grad(v)
        self.assertClose(de2dv.tolist(), [
            [np.exp(1 + 2), 0, 0],
            [0, np.exp(2 + 3), 0],
            [0, 0, np.exp(3 + 4)],
        ])
    
    def testProd(self):
        """
            d/dx uv = (du/dx)^T v  + (dv/dx)^T u
            d/du uv = (du/du)^T v
                    = eye() v
                    = eye(v)
        """
        u = Variable(np.array([1, 2, 3]))
        v = Variable(np.array([2, 3, 4]))
        p = PwProd(u, v)
        dpdu = p.grad(u)
        self.assertClose(dpdu.tolist(), [
            [2, 0, 0],
            [0, 3, 0],
            [0, 0, 4]
        ])


        """
            d/du (u+v)*v = (d/du u+v)^T v  +  (u+v) (d/du  v)^T
                         = (d/du u+v)^T v
                         = (d/du u)^T v
                         = eye() v
                         = eye(v)
        """
        s = Add(u, v)
        p2 = PwProd(s, v)
        dp2du = p2.grad(u)
        self.assertClose(dp2du.tolist(), [
            [2, 0, 0],
            [0, 3, 0],
            [0, 0, 4]
        ])

    def testPwDiv(self):
        u = Variable(np.array([1, 2, 3]))
        v = Variable(np.array([2, 3, 4]))
        d = PwDiv(u, v)
        dddu = d.grad(u)
        self.assertClose(dddu.tolist(), [
            [1/2, 0, 0],
            [0, 1/3, 0],
            [0, 0, 1/4]
        ])
        dddv = d.grad(v)
        self.assertClose(dddv.tolist(), [
            [-1/(2**2), 0, 0],
            [0, -2/(3**2), 0],
            [0, 0, -3/(4**2)]
        ])


    def testScalarPow(self):
        x = np.array([1, 2])
        x2 = x**2

        xV = Variable(x)
        x2V = ScalarPower(xV, 2)

        x2val = x2V.eval()
        x2dx = x2V.grad(xV)

        self.assertClose(x2val, x2)
        self.assertClose(x2dx, np.diag(2*x))


    def testSigmoid(self):
        def sig(x):
            return 1 / (1 + np.exp(-x))
        
        def dsig(x):
            return np.diag(sig(x) * (1 - sig(x)))

        data = np.array([0, 1000])

        x = Variable(data)
        s = Sigmoid(x)
        sVal = s.eval()
        sDif = s.grad(x)

        self.assertClose(sVal, sig(data))
        self.assertClose(sDif, dsig(data))

    def testSoftmax(self):
        def sm(x):
            return np.exp(x) / np.sum(np.exp(x))

        data = np.array([0.6, 1.0])

        x = Variable(data)
        s = Softmax(x)
        sVal = s.eval()
        sDif = s.grad(x)
        self.assertClose(sVal, sm(data))
        self.assertClose(sDif.shape, data.shape)

    def testSSE(self):
        def sse(ySim, yObs):
            return np.sum((ySim - yObs)**2)

        x = np.array([1, 2, 3])
        ySim = np.array(2) * x
        yObs = x**2
        sseObs = sse(ySim, yObs)

        xV = Variable(x)
        ySimV = ScalarMult(2, xV)
        sseV = SSE(ySimV, yObs)

        sseVal = sseV.eval()
        sseDx = sseV.grad(xV)
        sseDy = sseV.grad(ySimV)

        self.assertAlmostEqual(sseVal, sseObs)

        betterYSimV = ScalarPower(xV, 2)
        betterSseV = SSE(betterYSimV, yObs)
        betterSseVal = betterSseV.eval()
        betterSseDx = betterSseV.grad(xV)
        betterSseDy = betterSseV.grad(ySimV)

        self.assertAlmostEqual(betterSseVal, 0)
        self.assertClose(betterSseDx, np.array([0, 0, 0]))


    def testNotTooDeep(self):
        """
            y = a.*b
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
        a = Variable(np.array([1]))
        b = Variable(np.array([2]))
        c = Variable(np.array([3]))
        y = PwProd(a, b)
        z = Add(c, y)
        dzdy = z.grad(y)
        self.assertClose(dzdy, np.array([[1.0]]))


    def testEffectiveExpressionEquality(self):
        a = Variable(np.array([1]))
        b = Variable(np.array([2]))
        c1 = PwProd(a, b)
        c2 = PwProd(a, b)
        # c1 and c1 live at different memory-addresses,
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
        a = Variable(np.array([1]))
        b = Variable(np.array([2]))
        c = Variable(np.array([3]))
        y = PwProd(a, b)
        z = Add(c, y)
        y2 = PwProd(a, b)
        dzdy = z.grad(y2)
        self.assertClose(dzdy, np.array([[1.0]]))
    
    def testComplicatedGradients(self):
        a = Variable(np.random.rand(2, 3))
        b = Variable(np.random.rand(3))
        dadb = a.grad(b)
        self.assertTrue(isZero(dadb))
        self.assertEqual(dadb.shape, (2, 3, 3))
        c = Mult(a, b)
        self.assertEquals(c.eval().shape, (2,))
        dcdb = c.grad(b)
        self.assertEquals(dcdb.shape, (2, 3))
        dcda = c.grad(a)
        self.assertEquals(dcda.shape, (2, 2, 3))




if __name__ == '__main__':
    ut.main()


