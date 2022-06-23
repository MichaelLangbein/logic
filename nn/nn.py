import numpy as np
from autodiff import Node, Variable, Mult, Sigmoid, SSE, matMul


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
    def setI(self, i: Node):
        pass
    def x(self):
        pass
    def y(self):
        pass
    def updateParas(self, dE_dx):
        pass


class FullyConnectedLayer(Layer):
    def __init__(self, inputs: int, outputs: int):
        self.W = Variable(np.random.random((inputs, outputs)))

    def setI(self, i: Node):
        self.i = i

    def x(self):
        return Mult(self.W, self.i)

    def y(self):
        return Sigmoid(self.x())

    def updateParas(self, dE_dx):
        """
        dE/dWl = dE/dxl dxl/dWl 
                dxl/dWl = yl-1
        delta Wl = - alpha dE/dWl
        """
        dx_dW = self.i.value
        self.W.value -= 0.01 * dE_dx * dx_dW


class ConvolutionalLayer(Layer):
    pass


class AttentionLayer(Layer):
    def __init__(self, nInput: int, nOutput: int):
        self.Q = Variable(np.random.random((nInput, nOutput)))
        self.K = Variable(np.random.random((nInput, nOutput)))
        self.V = Variable(np.random.random((nInput, nOutput)))






class NN:
    def __init__(self, layers: list[Layer]):
        L = len(layers) - 1
        self.L = L
        self.layers = layers
        self.layer0 = self.layers[0]        
        self.layerL = self.layers[L]

        for l in range(1, L):
            layer = self.layers[l]
            previousLayer = self.layers[l - 1]
            layer.setI(previousLayer.y())

    def run(self, data: np.array):
        inputV = Variable(data)
        self.layer0.setI(inputV)
        out = self.layerL.y().eval()
        return out

    def backward(self, input: np.array, trueVal: np.array):
        inputV = Variable(input)
        self.layer0.setI(inputV)
        E = SSE(self.layerL.y(), trueVal)

        dE_dx_l = E.diff(self.layerL.x)

        for l in range(self.L - 1, 0):
            layer = self.layers[l]
            nextLayer = self.layers[l+1]

            dE_dx_lp1 = dE_dx_l
            dx_lp1_dx_l = nextLayer.x().diff(layer.x())
            dE_dx_l = matMul(dE_dx_lp1, dx_lp1_dx_l)

            layer.updateParas(dE_dx_l)

