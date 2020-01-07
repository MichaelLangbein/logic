import numpy as np


def zeroArray(arr):
    for el in arr:
        if el != 0:
            return False
    return True


def normalize(arr):
    if zeroArray(arr):
        return arr
    return arr / magnitude(arr)

def angle(arr1, arr2):
    if zeroArray(arr1) or zeroArray(arr2):
        return 0.0
    d = innerProd(arr1, arr2)
    n = magnitude(arr1) * magnitude(arr2)
    if d >= n:
        return 0.0
    return np.arccos((d/n))

def innerProd(arr1, arr2):
    return np.inner(arr1, arr2)

def magnitude(arr):
    return np.sqrt(arr[0]**2 + arr[1]**2)