import unittest as ut

# https://math.stackexchange.com/questions/409460/multiplying-3d-matrix


class Tensor():
    def __init__(self, data):
        pass

    def __add__(self, other: Tensor):
        assert(self.shape() == other.shape())
        
        if self.isScalar() and other.isScalar():
            return Tensor(self.value() + other.value())

        if self.isScalar() and not other.isScalar():
            sum = Tensor.zeros(other.shape())
            for i, entry in enumerate(other):
                sum[i] = self + entry
            return sum

        if not self.isScalar() and other.isScalar():
            sum = Tensor.zeros(self.shape())
            for i, entry in enumerate(self):
                sum[i] = entry + other

        else:
            sum = Tensor.zeros(self.shape)
            for r, row in enumerate(self):
                for c, col in enumerate(other):
                    sum[r][c] = row + col
            return sum

    def __len__(self):
        pass

    def __getitem__(self, index):
        pass

    def __mult__(self, other: Tensor):
        if self.isScalar() and other.isScalar():
            return Tensor(self.value() * other.value())

        if self.isScalar() and not other.isScalar():
            sum = Tensor.zeros(other.shape())
            for entry in other:
                sum += self * entry
            return sum

        if not self.isScalar() and other.isScalar():
            sum = Tensor.zeros(self.shape())
            for entry in self:
                sum += entry * other
            return sum

        else:
            ownShape = self.shape()
            otherShape = other.shape()
            assert(ownShape[-1] == otherShape[0])
            newShape = ownShape[:-1] + otherShape[1:]
            out = Tensor.zeros(newShape)
            for r, row in enumerate(self):
                for c, col in enumerate(other):
                    sum = row * col
                    out[r][c] = sum
            return out

    def shape(self):
        pass

    def value(self):
        if self.isScalar():
            return self.data
        else:
            data = []
            for entry in self.data:
                data.append(entry.value())
            return data

    def isScalar(self):
        return self.shape() == ()

    def zeros(shape):
        pass
            



class TensorTests(ut.TestCase):
    def setUp(self):
        return super().setUp()

    def testScalarScalarAdd(self):
        a = Tensor(1)
        b = Tensor(2)
        c = a + b
        self.assertEqual(c.value(), 3)

    def testScalarVectorAdd(self):
        a = Tensor(2)
        b = Tensor([1, 2])
        self.assertRaises(Exception, a + b)

    def testVectorScalarAdd(self):
        a = Tensor(2)
        b = Tensor([1, 2])
        self.assertRaises(Exception, b + a)

    def testScalarMatrixAdd(self):
        a = Tensor(2)
        b = Tensor([[1, 2], [3, 4]])
        self.assertRaises(Exception, a + b)

    def testMatrixScalarAdd(self):
        a = Tensor(2)
        b = Tensor([[1, 2], [3, 4]])
        self.assertRaises(Exception, b + a)

    def testVectorVectorAdd(self):
        a = Tensor([1, 2, 3])
        b = Tensor([2, 3, 4])
        c = a + b
        self.assertEqual(c.value(), [3, 5, 7])

    def testMatrixVectorAdd(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor([1, 2])
        self.assertRaises(Exception, a + b)

    def testVectorMatrixAdd(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor([1, 2])
        self.assertRaises(Exception, b + a)

    def testMatrixMatrixAdd(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor([[2, 3], [4, 5]])
        c = a + b
        self.assertEqual(c.value(), [[3, 5], [7, 9]])

    def testScalarScalarMult(self):
        a = Tensor(1)
        b = Tensor(2)
        c = a * b
        self.assertEqual(c.value(), 2)

    def testScalarVectorMult(self):
        a = Tensor(2)
        b = Tensor([1, 2])
        c = b * a
        self.assertEqual(c.value(), [2, 4])

    def testVectorScalarMult(self):
        a = Tensor(2)
        b = Tensor([1, 2])
        c = b * a
        self.assertEqual(c.value(), [2, 4])

    def testScalarMatrixMult(self):
        a = Tensor(2)
        b = Tensor([[1, 2], [3, 4]])
        c = a * b
        self.assertEqual(c.value(), [[2, 4], [6, 8]])

    def testMatrixScalarMult(self):
        a = Tensor(2)
        b = Tensor([[1, 2], [3, 4]])
        c = b * a
        self.assertEqual(c.value(), [[2, 4], [6, 8]])

    def testVectorVectorMult(self):
        a = Tensor([1, 2, 3])
        b = Tensor([2, 3, 4])
        c = a * b
        self.assertEqual(c.value(), 20)

    def testMatrixVectorMult(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor([1, 2])
        c = a * b
        self.assertEqual(c.value(), [3, 8])

    def testVectorMatrixMult(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor([1, 2])
        c = a * b
        self.assertEqual(c.value(), [3, 8])

    def testMatrixMatrixMult(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor([[2, 3], [4, 5]])
        c = a * b
        self.assertEqual(c.value(), [[10, 13], [22, 29]])



if __name__ == '__main__':
    ut.main()
