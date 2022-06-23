import unittest as ut
import numpy as np

from nn import FullyConnectedLayer, NN




def simpleOutputFunc(input):
    return input[0] + input[1] * input[2] / 3

def createRandomData(nrSamples, nrI=3, outputFunc=simpleOutputFunc):
    inputs = np.random.random((nrSamples, nrI))
    outputs = outputFunc(inputs)
    return inputs, outputs



class NNTests(ut.TestCase):
    
    def setUp(self):
        return super().setUp()


    def testSimpleNet(self):
        layers = [FullyConnectedLayer(3, 3), FullyConnectedLayer(3, 2), FullyConnectedLayer(2, 1)]
        net = NN(layers)

        nrSamples = 100
        inputs, outputs = createRandomData(nrSamples)
        for e in range(3):
            print(f"epoch {e} ...")
            for n in range(nrSamples):
                print(f"epoch {e}:  {n/nrSamples}")
                net.backward(inputs[n], outputs[n])

        inputsVal, outputsVal = createRandomData(5)

        e = 0
        for i in range(5):
            oSim = net.run(inputsVal[i])
            oVal = outputsVal[i]
            e += (oSim - oVal)**2

        print(e)

        self.assertTrue(e < 5.0)

    




if __name__ == '__main__':
    ut.main()