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

def matMul(A, B, nrDims=None):
    if type(A) is not np.ndarray:
        if A == 0:
            return 0
        if A == 1:
            return B
        A = np.array(A)
    if type(B) is not np.ndarray:
        if B == 1:
            return A
        if B == 0:
            return 0
        B = np.array(B)
    if not A.shape:
        return A * B
    if not B.shape:
        return A * B
    axesA = []
    axesB = []
    if not nrDims:
        dimsA = [(i, v) for  (i, v) in enumerate(A.shape)]
        dimsB = [(i, v) for  (i, v) in enumerate(B.shape)]
        for (i, da), (j, db) in zip(reversed(dimsA), dimsB):
            if da == db:
                axesA.append(i)
                axesB.append(j)
            else: 
                break
    else:
        lA = len(A.shape) - 1
        axesA = [lA - i for i in range(nrDims)]
        axesB = [i      for i in range(nrDims)]
    return np.tensordot(A, B, axes=(axesA, axesB))


def crossMult(A, B):
    if A.shape[-1] != 1:
        A = np.reshape(A, A.shape + (1,))
    if B.shape[0] != 1:
        B = np.reshape(B, (1,) + B.shape)
    return np.dot(A, B)

def permutations(ranges):
    if len(ranges) == 0:
        return []
    if len(ranges) == 1:
        return [[i] for i in range(ranges[0])]
    subResults = permutations(ranges[1:])
    result = []
    for i in range(ranges[0]):
        for p in subResults:
            result.append([i] + p)
    return result

def diffBySelf(shape):
    if shape == ():
        return np.array(1)
    newShape = shape + shape
    out = np.zeros(newShape)
    for indices in permutations(shape):
        out[*indices][*indices] = 1
    return out


def memoized(func):
    memory = {}
    def memF(*args):
        argString = f"{args}"
        if argString not in memory:
            memory[argString] = func(*args)
        return memory[argString]
    return memF