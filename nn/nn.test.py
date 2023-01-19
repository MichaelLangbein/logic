import unittest as ut
import numpy as np
from autodiff import SSE, Mult, Sigmoid, Variable

from nn import FullyConnectedLayer, NN, training, validation





class NNTests(ut.TestCase):
    
    def setUp(self):
        np.random.seed(123)
        return super().setUp()


    def _arraysClose(self, arr1: np.array, arr2: np.array, threshold = 0.001):
        if arr1.shape != arr2.shape:
            print("Dimensions don't match", arr1.shape, arr2.shape)
            return False
        diff = np.max(np.abs(arr1 - arr2))
        if diff >= threshold:
            print("values unequal: ", arr1, arr2)
            return False
        return True


    def _valuesClose(self, v1, v2, threshold = 0.001):
        diff = np.abs(v1 - v2)
        if diff >= threshold:
            print(v1, " != ", v2)
            return False
        return True


    def assertClose(self, v1, v2, threshold = 0.001):
        if hasattr(v1, "__len__"):
            return self.assertTrue(self._arraysClose(v1, v2, threshold))
        return self.assertTrue(self._valuesClose(v1, v2, threshold))


    def testPrimitive(self):

        # truth
        input = np.array([1.5])
        inputV = Variable(input)
        wV = Variable(np.array([0.5]))
        xV = Mult(wV, inputV)  # 0.75
        outputV = Sigmoid(xV)  # 0.6792
        output = outputV.eval()
        self.assertClose(output, np.array([0.6791787]))

        # first prediction
        layer = FullyConnectedLayer(1, 1)
        layer.setI(inputV)
        predictionV = layer.y()
        errorV = SSE(predictionV, output)
        error = errorV.eval()
        dEdX = errorV.diff(layer.x())
        self.assertNotEqual(dEdX, 0.0)
        layer.updateParas(dEdX)

        # second prediction
        prediction2V = layer.y()
        error2V = SSE(prediction2V, output)
        error2 = error2V.eval()
        self.assertLess(error2, error)

        

    def testSimplestNet(self):
        layers = [FullyConnectedLayer(1, 1)]
        net = NN(layers)
        
        nrSamples = 100
        nrValidation = 10
        inputsTraining = np.random.random((1, nrSamples))
        outputsTraining = inputsTraining * 0.3
        inputsValidation = np.random.random((1, nrValidation))
        outputsValidation = inputsValidation * 0.3

        sseInitial = validation(net, inputsValidation, outputsValidation)
        training(net, inputsTraining, outputsTraining, 5, 5)
        sseFinal = validation(net, inputsValidation, outputsValidation)
        
        self.assertLess(sseFinal, sseInitial)


    def testSimpleNet(self):

        def createRandomData(nrSamples, nrI=3):
            inputs = np.random.random((nrI, nrSamples))
            outputs = np.array([inputs[0,:] + inputs[1,:] * inputs[2,:] / 3])
            return inputs, outputs

        layers = [FullyConnectedLayer(3, 3), FullyConnectedLayer(3, 2), FullyConnectedLayer(2, 1)]
        net = NN(layers)

        nrSamples = 100
        nrSplVal = 5
        inputs, outputs = createRandomData(nrSamples)
        inputsVal, outputsVal = createRandomData(nrSplVal)

        sseInitial = validation(net, inputsVal, outputsVal)
        training(net, inputs, outputs, 5, 5)
        sseFinal = validation(net, inputsVal, outputsVal)
        
        self.assertLess(sseFinal, sseInitial)

    




if __name__ == '__main__':
    ut.main()