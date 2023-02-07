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
            self.data = np.array(data)
        else:
            self.data = data

    def dimensions(self):
        return self.data.shape

    def eye(*dims):
        data = eye(dims)
        return Tensor(data)

    def __add__(self, other):
        sum = self.data + other.data
        return Tensor(sum)

    def zeros(*dims):
        return Tensor(np.zeros(dims))

    def asArray():
        return self.data
