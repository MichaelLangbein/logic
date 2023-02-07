import unittest as ut

# https://math.stackexchange.com/questions/409460/multiplying-3d-matrix


class Tensor():
    def __init__(self, data):
        if isinstance(data, Tensor):
            data = data.value()
        if not hasattr(data, "__len__"):
            self._data = data
        else:
            self._data = []
            for entry in data:
                self._data.append(Tensor(entry))

    def __add__(self, other):
        if self.isScalar() and other.isScalar():
            return Tensor(self.value() + other.value())

        if self.isScalar() and not other.isScalar():
            sum = Tensor.zeros(other.shape())
            for i, entry in enumerate(other):
                sum[i] = self + entry
            return sum

        else:
            out = Tensor.zeros(self.shape())
            for r, row in enumerate(self):
                out[r] = row + other
            return out

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        assert(isinstance(value, Tensor))
        self._data[index] = value

    def __mul__(self, other):
        shapeSelf = self.shape()
        shapeOther = other.shape()
        if len(shapeSelf) == 0:
            return Tensor.__scalarMult(self, other)
        if len(shapeSelf) == 1:
            return Tensor.__innerProd(self, other)

        out = Tensor.zeros([shapeSelf[0], shapeOther[0]])
        for r, row in enumerate(self):
            for c, col in enumerate(other):
                out[r][c] = row * col
        return out

    def __scalarMult(scalar, other):
        pass

    def __innerProd(a, b):
        pass

    def __matmul__(self, other):
        if self.isScalar() and other.isScalar():
            return Tensor(self.value() * other.value())

        if self.isScalar() and not other.isScalar():
            out = Tensor.zeros(other.shape())
            for i, entry in enumerate(other):
                out[i] = self * entry
            return out

        else:
            out = Tensor.zeros([len(self)])
            for i, entry in enumerate(self):
                out[i] = entry * other
            return out

    def shape(self):
        if not hasattr(self._data, "__len__"):
            return []
        shp = [len(self)]
        if len(self) > 0:
            shp += self[0].shape()
        return shp

    def value(self):
        if self.isScalar():
            return self._data
        else:
            data = []
            for entry in self._data:
                data.append(entry.value())
            return data

    def isScalar(self):
        return self.shape() == []

    def zeros(shape):
        if len(shape) == 0:
            return Tensor(0)
        else:
            data = [Tensor.zeros(shape[1:]) for i in range(shape[0])]
            return Tensor(data)

            



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
        self.assertRaises(AssertionError, lambda : a + b)

    def testVectorScalarAdd(self):
        a = Tensor(2)
        b = Tensor([1, 2])
        self.assertRaises(AssertionError, lambda : b + a)

    def testScalarMatrixAdd(self):
        a = Tensor(2)
        b = Tensor([[1, 2], [3, 4]])
        self.assertRaises(AssertionError, lambda : a + b)

    def testMatrixScalarAdd(self):
        a = Tensor(2)
        b = Tensor([[1, 2], [3, 4]])
        self.assertRaises(AssertionError, lambda : b + a)

    def testVectorVectorAdd(self):
        a = Tensor([1, 2, 3])
        b = Tensor([2, 3, 4])
        c = a + b
        self.assertEqual(c.value(), [3, 5, 7])

    def testMatrixVectorAdd(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor([1, 2])
        self.assertRaises(AssertionError, lambda : a + b)

    def testVectorMatrixAdd(self):
        a = Tensor([[1, 2], [3, 4]])
        b = Tensor([1, 2])
        self.assertRaises(AssertionError, lambda : b + a)

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

    def testHigherDimMult(self):
        a = Tensor([[[1, 2], [3, 4]], [[2, 3], [4, 5]]])
        self.assertEqual(a.shape(), [2, 2, 2])
        b = Tensor([[1, 2], [3, 4]])
        self.assertEqual(b.shape(), [2, 2])
        c = a * b
        self.assertEqual(c.shape(), [2, 2, 2])



if __name__ == '__main__':
    ut.main()
