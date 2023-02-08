import numpy as np
from autodiff import Node, Variable, Mult, Sigmoid, SSE
from helpers import matMul


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
        raise Exception("Method `setI` not implemented")
    def x(self):
        raise Exception("Method `x` not implemented")
    def y(self):
        raise Exception("Method `y` not implemented")
    def updateParas(self, dE_dx):
        raise Exception("Method `updateParas` not implemented")


class FullyConnectedLayer(Layer):
    def __init__(self, inputs: int, outputs: int):
        self.i = Variable(np.random.random(inputs))
        self.W = Variable(np.random.random((outputs, inputs)))

    def setI(self, i: Node):
        self.i = i

    def x(self):
        return Mult(self.W, self.i)

    def y(self):
        return Sigmoid(self.x())

    def updateParas(self, dE_dx):
        """
        dE/dWl = dE/dxl dxl/dWl 
        delta Wl = - alpha dE/dWl
        """
        def lineEye(v, D, R, C):
            out = []
            for d in range(D):
                dim = []
                for r in range(R):
                    row = []
                    for c in range(C):
                        if d == r:
                            row.append(v[c])
                        else:
                            row.append(0)
                    dim.append(row)
                out.append(dim)
            return np.array(out)
        i = self.i.eval()
        W = self.W.eval()
        dx_dW = lineEye(i, dE_dx.shape[-1], W.shape[0], W.shape[1])
        dE_dW = matMul(dE_dx, dx_dW)
        self.W.value -= 0.01 * dE_dW


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

        for l in range(1, len(layers)):
            layer = self.layers[l]
            previousLayer = self.layers[l - 1]
            layer.setI(previousLayer.y())

    def run(self, data: np.ndarray):
        inputV = Variable(data)
        self.layer0.setI(inputV)
        out = self.layerL.y().eval()
        return out

    def backward(self, input: np.ndarray, trueVal: np.ndarray):
        self.layer0.setI(Variable(input))
        E = SSE(self.layerL.y(), trueVal)

        dE_dx_l = E.diff(self.layerL.x())
        self.layerL.updateParas(dE_dx_l)

        for l in reversed(range(0, self.L)):
            layer = self.layers[l]
            nextLayer = self.layers[l+1]

            dE_dx_lp1 = dE_dx_l
            dx_lp1_dx_l = nextLayer.x().diff(layer.x())
            dE_dx_l = dE_dx_lp1 @ dx_lp1_dx_l

            layer.updateParas(dE_dx_l)

    def backwardBatch(self, inputs: list[np.ndarray], trueVals: list[np.ndarray]):
        summed_dE_dx_l = [0.0 for i in range(len(self.layers))]
        batchSize = len(inputs)
        
        for i in range(batchSize):
            input = inputs[i]
            trueVal = trueVals[i]

            self.layer0.setI(Variable(input))
            E = SSE(self.layerL.y(), trueVal)

            dE_dx_l = E.diff(self.layerL.x())
            summed_dE_dx_l[self.L] += dE_dx_l

            for l in reversed(range(0, self.L)):
                layer     = self.layers[l]
                nextLayer = self.layers[l+1]

                dE_dx_lp1   = dE_dx_l
                dx_lp1_dx_l = nextLayer.x().diff(layer.x())
                dE_dx_l     = dE_dx_lp1 @ dx_lp1_dx_l

                summed_dE_dx_l[l] += dE_dx_l
        
        for l in range(len(self.layers)):
            dE_dx_l = summed_dE_dx_l[l] / batchSize
            self.layers[l].updateParas(dE_dx_l)



def training(net, inputs: np.ndarray, outputs: np.ndarray, nrEpochs, batchSize):
    (inputDim, nrSamples) = inputs.shape
    (outputDim, nso) = outputs.shape
    if nrSamples != nso:
        raise Exception(f"Input and output have different sizes: {nrSamples} vs. {nso}")

    for e in range(nrEpochs):
        for b in range(int(nrSamples/batchSize)):
            batchIn = []
            batchOut = []
            for i in range(batchSize):
                n = b * batchSize + i
                batchIn.append(inputs[:, n])
                batchOut.append(outputs[:, n])
            net.backwardBatch(batchIn, batchOut)


def validation(net, inputs: np.ndarray, outputs: np.ndarray):
    (inputDim, nrSamples) = inputs.shape
    (outputDim, nso) = outputs.shape
    if nrSamples != nso:
        raise Exception(f"Input and output have different sizes: {nrSamples} vs. {nso}")

    sse = 0.0
    for n in range(nrSamples):
        input = inputs[:, n]
        output = outputs[:, n]
        prediction = net.run(input)
        se = (output - prediction) * (output - prediction)
        sse += se
    
    return sse