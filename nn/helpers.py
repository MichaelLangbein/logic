import numpy as np

def allEqual(data):
    for entry in data:
        if entry != data[0]:
            return False
    return True

def eye(Dims, Inds = []):
    if not hasattr(Dims, '__len__'):
        return eye([Dims], Inds)
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

def zeros(*dims):
    return np.zeros(dims)

def isZero(something):
    if np.min(something) == 0.0 and np.max(something) == 0.0:
        return True
    return False


def matMul(a, b):
    if a.shape == (1,):
        return a[0] * b
    if b.shape == (1,):
        return a * b[0]
    return a @ b