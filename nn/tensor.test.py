import unittest as ut
from tensor import Tensor, TensorNull, TensorOne


class AutodiffTests(ut.TestCase):

    def setUp(self):
        return super().setUp()

    def testTensorAddition(self):
        t1 = Tensor([1, 2, 3])
        t2 = Tensor([2, 3, 4])
        t3 = t1 + t2
        self.assertEqual(t3.asArray(), [3, 5, 7])

    def testTensorMultiplication(self):
        t1 = Tensor([[1, 2], [2, 1]])
        t2 = Tensor([1, 2])
        t3 = t1 @ t2
        self.assertEqual(t3.asArray(), [5, 4])

        t4 = Tensor([[1, 2], [2, 1]])
        t5 = t1 @ t4
        self.assertEqual(t5.asArray(), [[5, 4], [4, 5]])

    def testTensorEye(self):
        t1 = Tensor.eye(1)
        t2 = Tensor.eye(2, 2)
        t3 = Tensor.eye(3, 3)
        t4 = Tensor.eye(3, 3, 3)
        self.assertEqual(t1.asArray(), [1.0])
        self.assertEqual(t2.asArray(), [
            [1.0, 0.0], 
            [0.0, 1.0]
        ])
        self.assertEqual(t3.asArray(), [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ])

    # There must be a tensor 0 such that
    # t + 0 = t
    def testTensorNull(self):
        t0 = TensorNull()
        t = Tensor([[1, 2], [3, 4]])
        tp = t + t0
        pt = t0 + t
        t2 = Tensor([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        tp2 = t2 + t0
        pt2 = t0 + t2

        self.assertEqual(t.asArray(), tp.asArray())
        self.assertEqual(t.asArray(), pt.asArray())
        self.assertEqual(t2.asArray(), tp2.asArray())
        self.assertEqual(t2.asArray(), pt2.asArray())

    # There must be a tensor such that
    # t * 1 = t
    def testTensorOne(self):
        t1 = TensorOne()
        t = Tensor([[1, 2], [3, 4]])
        tm = t * t1
        mt = t1 * t
        t2 = Tensor([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        tm2 = t2 * t1
        mt2 = t1 * t2

        self.assertEqual(t.asArray(), tm.asArray())
        self.assertEqual(t.asArray(), mt.asArray())
        self.assertEqual(t2.asArray(), tm2.asArray())
        self.assertEqual(t2.asArray(), mt2.asArray())





if __name__ == '__main__':
    ut.main()


