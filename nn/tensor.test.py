import unittest as ut
from tensor import Tensor


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






if __name__ == '__main__':
    ut.main()


