from nodes import Node, Constant, Plus, Sse, Variable, MatMul, ScalarProd, Sigmoid, gradient
import numpy as np




"""
For a fully connected net:

yl = a(xl)
xl = Wl yl-1
E = \Sum(yObs - yL)^2

dE/dxL = - 2 \Sum (yObs - yL) da(xL)/dxL
dE/dxl = dE/dxl+1 dxl+1/dxl
                  dxl+1/dxl = Wl+1 da(xl)/dxl
dE/dWl = dE/dxl dxl/dWl 
                dxl/dWl = yl-1
delta Wl = - alpha dE/dWl

"""


class Layer:
    def eval(self, at):
        return self.getOutput().eval(at)
    def getOutput(self):
        pass
    def getParaValues(self):
        pass
    def update(self, error, at):
        pass


class FullyConnectedLayer(Layer):
    def __init__(self, name, nIn, nOut, input):
        self.name = name
        self.WVal = np.random.random([nOut, nIn])
        self.bVal = np.random.random([nOut])
        self.input = input
        self.W = Variable(f"{self.name}-W")
        self.b = Variable(f"{self.name}-b")
        self.output = Sigmoid(Plus(MatMul(self.W, self.input), self.b))

    def getParaValues(self):
        return {
            self.W.name: self.WVal,
            self.b.name: self.bVal
        }

    def getOutput(self):
        return self.output
    
    def update(self, error, at):
        dedW = gradient(error, self.W, at)
        self.WVal += 0.01 * dedW
        dedb = gradient(error, self.b, at)
        self.bVal += 0.01 * dedb


class SelfAttentionLayer(Layer):
    def __init__(self, name, nIn, useMask, input):
        """
        softmax((Q . K^T)/sqrt(kSize) + M) @ V
        """
        self.name = name
        kSize = 8
        vSize = 8
        
        self.QVal = np.random.random([nIn, kSize])
        self.KVal = np.random.random([nIn, kSize])
        self.VVal = np.random.random([nIn, vSize])
        
        self.input = input
        self.Q = Variable(f"{self.name}-Q")
        self.K = Variable(f"{self.name}-K")
        self.V = Variable(f"{self.name}-V")
        
        # How much each word relates to each other word
        focusOnEachOther = MatMul(self.Q, Transpose(self.K))
        normalizedFocus = ScalarProd(focusOnEachOther, 1.0 / np.sqrt(kSize))

        # For decoder only: hide words that come after the current word
        if useMask:
            maskVal = np.tril(np.ones(nIn, nIn))
            maskVal[maskVal == 0] = -np.infty
            maskVal[maskVal == 1] = 0
            mask = Constant(maskVal)
            attention = SoftMax(Plus(normalizedFocus, mask))
        else:
            attention = SoftMax(normalizedFocus)

        # 
        newV = MatMul(attention, self.V)
