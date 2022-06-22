import numpy as np
from autodiff import MatrixVectorMult, Sigmoid, Variable





class NN:
    def __init__(self, layers: list[Layer]):
        self.layers = layers

    def run(self, data: np.array):
        for layer in self.layers:
            data = layer.run(data)
        return data

    def backward(self, trueVal: np.array, predictedVal: np.array):

        X = []
        for layer in self.layers:
            output = layer.run(input)
            X.append(output)
            input = output
        
        dE_dx_L = None

        dE_dx_l = dE_dx_L
        for l in range(len(self.layers) - 1, 0):
            
            layer = self.layers[l]
            xl = X[l]

            dE_dx_lp1 = dE_dx_l
            dx_lp1_dx_l = layer.dx_lp1_dx_l(xl)
            dE_dx_l = dE_dx_lp1 @ dx_lp1_dx_l




class Layer:
    def run(self, data: np.array) -> np.array:
        raise Exception('`run` not implemented')

    def dx_lp1_dx_l(self) -> np.array:
        raise Exception('`dx_lp1_dx_l` not implemented')

    def update(self):
        raise Exception('`update` not implemented')


class FullyConnectedLayer(Layer):
    def __init__(self, nInput: int, nOutput: int):
        self.W = Variable(np.random.random((nInput, nOutput)))
        self.i = Variable(np.zeros(nInput, 1))
        self.x = MatrixVectorMult(self.W, self.i)
        self.y = Sigmoid(self.x)

    def calc(self, input: np.array):
        self.i.val = input
        yVal = self.y.eval()
        return yVal

    def dx_lp1_dx_l(self, xl) -> np.array:
        return self.x.diff(xl)

    def update(self):
        pass


class ConvolutionalLayer(Layer):
    pass

class AttentionLayer(Layer):
    pass

