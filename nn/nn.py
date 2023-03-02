from nodes import Node, Sse, Variable, MatMul, Sigmoid, gradient
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
    def getParas(self):
        pass
    def eval(self, paras):
        pass
    def setInput(self, input):
        pass
    def getOutput(self):
        pass
    def update(self, error):
        pass


class NN:
    def __init__(self, layers):

        # 1: collect all parameters
        paras = {
            'input': None
        }
        for layer in layers:
            layerParas = layer.getParas()
            paras += layerParas
        self.paras = paras

        # 2: connect layers to each other
        for i, layer in enumerate(layers):
            if i == 0:
                continue
            prevLayer = layers[i - 1]
            layer.setInput(prevLayer.getOutput())
        self.layers = layers

    def predict(self, input):
        self.paras["input"] = input
        lastLayer = self.layers[len(self.layers) - 1]
        prediction = lastLayer.eval(self.paras)
        return prediction
    
    def training(self, inputs, outputs):

        lastLayer = self.layers[len(self.layers) - 1]
        prediction = lastLayer.getOutput()
        outputVariable = Variable("output")
        error = Sse(outputVariable, prediction)
        
        for input, output in zip(inputs, outputs):
            for layer in self.layers:
                layer.update(error)
        
