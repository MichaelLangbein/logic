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
        return self.output
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

    def update(self, error, at):
        dedW = gradient(error, self.W, at)
        self.WVal += 0.01 * dedW
        dedb = gradient(error, self.b, at)
        self.bVal += 0.01 * dedb


class SelfAttentionLayer(Layer):
    def __init__(self, name, input):
        """
        https://www.youtube.com/watch?v=KmAISyVvE1Y
        sequence-to-sequence-layer
        no parameters

        Nice analogy:
        Word: person
        Word's embedding: person's interests
        Interests * Interests^T: compatability-matrix
        Compat-matrix * Interests: how well is this person integrated into each interest's community
                                 = word expressed by how well its embedding's elements fit with the other words
        """
        self.name = name

        WPrime = MatMul(input, Transpose(input))
        W = SoftMax(WPrime)
        output = MatMul(input, Transpose(W))

        self.input = input
        self.output = output

    def getParaValues(self):
        return {}
    
    def update(self, error, at):
        return