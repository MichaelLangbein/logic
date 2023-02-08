import numpy as np


def allEqual(data):
    for entry in data:
        if entry != data[0]:
            return False
    return True

def eye(Dims, Inds = []):
    if len(Dims) == 0:
        if allEqual(Inds):
            return 1
        else:
            return 0
    data = []
    for r in range(Dims[0]):
        row = eye(Dims[1:], Inds + [r])
        data.append(row)
    return data

class Tensor:
    def __init__(self, data):
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        self.data = data

    def dimensions(self):
        return self.data.shape

    def eye(*dims):
        data = eye(dims)
        return Tensor(data)

    def transpose(self):
        data = self.data.transpose()
        return Tensor(data)

    def isZero(self):
        return np.max(self.data) == 0.0 and np.min(self.data) == 0.0

    def __add__(self, other):
        sum = self.data + other.data
        return Tensor(sum)

    def __matmul__(self, other):
        data = self.data @ other.data
        return Tensor(data)

    def __mul__(self, other):
        data = self.data * other.data
        return Tensor(data)

    def __pow__(self, other):
        if not isinstance(other, Tensor):
            data = self.data ** other
        else:
            data = self.data ** other.data
        return Tensor(data)

    def __neg__(self):
        return Tensor(-self.data)

    def __sub__(self, other):
        return Tensor(self.data - other.data)

    def __truediv__(self, other):
        return Tensor(self.data / other.data)

    def __floordiv__(self, other):
        return Tensor(self.data // other.data)

    def zeros(*dims):
        return Tensor(np.zeros(dims))

    def asArray(self):
        return self.data.tolist()
