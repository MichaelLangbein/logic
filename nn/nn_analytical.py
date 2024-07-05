#%%
import numpy as np
import random



def pick_random_numbers(n, m):
    if n > m:
        raise ValueError("n cannot be greater than m as it's not possible to pick n unique numbers less than m.")
    return random.sample(range(m), n)


def pick(data, indices):
    out = []
    for i in indices:
        out.append(data[i])
    return out

def errors(predictions, realValues):
    es = []
    for i in range(len(predictions)):
        es.append(np.abs(predictions[i] - realValues[i])[0])
    return es


# %%


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def diffSigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


class FullyConnectedOutputLayer:
    def __init__(self, inSize, outSize):
        self.weights = np.random.randn(outSize, inSize) * np.sqrt(2. / (outSize + inSize))

    def forward(self, inputs):
        out = []
        for input in inputs:
            x = self.weights @ input
            y = sigmoid(x)
            out.append(y)
        return out
    
    def backward(self, trueValues, predictions, inputs):

        dEdx = []
        dEdW = np.zeros(self.weights.shape)

        batchSize = len(trueValues)
        for s in range(batchSize):

            input_s = inputs[s]
            prediction_s = predictions[s]
            trueValue_s = trueValues[s]

            x_s = self.weights @ input_s
            dSig_s = diffSigmoid(x_s)
            dEdx_s = 2 * (trueValue_s - prediction_s) * dSig_s
            
            dEdx.append(dEdx_s)
            dEdW += np.outer(dEdx_s, input_s)
        
        return dEdx, dEdW

        

class FullyConnectedLayer:
    def __init__(self, inSize, outSize):
        self.weights = np.random.randn(outSize, inSize) * np.sqrt(2. / (outSize + inSize))

    def forward(self, inputs):
        out = []
        for input in inputs:
            x = self.weights @ input
            y = sigmoid(x)
            out.append(y)
        return out
    
    def backward(self, dEdx_lp1, W_lp1, inputs):

        dEdx = []
        dEdW = np.zeros(self.weights.shape)

        batchSize = len(dEdx_lp1)
        for s in range(batchSize):

            dEdx_lp1_s = dEdx_lp1[s]
            input_s = inputs[s]

            x_s = self.weights @ input_s
            dSig_s = diffSigmoid(x_s)
            dEdx_l_s = (dEdx_lp1_s @ W_lp1) * dSig_s

            dEdx.append(dEdx_l_s)
            dEdW += np.outer(dEdx_l_s, input_s)

        return dEdx, dEdW



class Network:
    def __init__(self, shapes):
        self.layers = []

        nrLayers = len(shapes) - 1
        for i in range(1, nrLayers + 1):
            inSize = shapes[i-1]
            outSize = shapes[i]
            if i <= nrLayers - 1:
                layer = FullyConnectedLayer(inSize, outSize)
            else:
                layer = FullyConnectedOutputLayer(inSize, outSize)
            self.layers.append(layer)


    def predict(self, inputs):
        allOutputs = [inputs]
        for layer in self.layers:
            outputs = layer.forward(inputs)
            allOutputs.append(outputs)
            inputs = outputs
        return allOutputs


    def trainBatch(self, inputs, trueValues, alpha):
        # 1. forward
        allOutputs = self.predict(inputs)

        # 2. backward 
        allDEdWs = [None for i in range(len(self.layers))]

        layer_p1 = self.layers[-1]
        dEdx_lp1, dEdW = layer_p1.backward(trueValues, allOutputs[-1], allOutputs[-2])
        allDEdWs[-1] = dEdW

        for l in reversed(range(0, len(self.layers)-1)):
            layer = self.layers[l]
            dEdx, dEdW = layer.backward(dEdx_lp1, layer_p1.weights, allOutputs[l])
            allDEdWs[l] = dEdW
            dEdx_lp1 = dEdx
            layer_p1 = layer

        # 3. update
        for l, layer in enumerate(self.layers):
            layer.weights += alpha * allDEdWs[l]


        



#%%

# # LAND
# data = [
#     {"input": np.array([0, 0]), "output": np.array([0.0])},
#     {"input": np.array([0, 1]), "output": np.array([0.0])},
#     {"input": np.array([1, 0]), "output": np.array([0.0])},
#     {"input": np.array([1, 1]), "output": np.array([1.0])},
# ]
# XOR
data = [
    {"input": np.array([0, 0]), "output": np.array([0.0])},
    {"input": np.array([0, 1]), "output": np.array([1.0])},
    {"input": np.array([1, 0]), "output": np.array([1.0])},
    {"input": np.array([1, 1]), "output": np.array([0.0])},
]


net = Network([2, 2, 1])


nrIterations = 20_000
batchSize = 4



# prediction 1
batchIndices = pick_random_numbers(batchSize, len(data))
validationInputs     = [d["input"]  for d in data]
validationTrueValues = [d["output"] for d in data]
def predictionError(predictions, trueValues):
    e = 0
    for i in range(len(predictions)):
        e += (predictions[i] - trueValues[i]) * (predictions[i] - trueValues[i])
    return e

predictions1 = net.predict(validationInputs)[-1]
print("prediction before training: ", predictionError(predictions1, validationTrueValues))



# training
for i in range(nrIterations):
    batchIndices = pick_random_numbers(batchSize, len(data))
    inputs     = [d["input"]  for d in pick(data, batchIndices)]
    trueValues = [d["output"] for d in pick(data, batchIndices)]
    net.trainBatch(inputs, trueValues, 0.1 * (1. - i/nrIterations))
    if i % 1_000 == 0:
        prediction = net.predict(validationInputs)[-1]
        print(predictionError(prediction, validationTrueValues))



# prediction 2
predictions2 = net.predict(validationInputs)[-1]
print("prediction after training: ", predictionError(predictions2, validationTrueValues))

# %%
import matplotlib.pyplot as plt


fig, axes = plt.subplots(2, 1, height_ratios=[2, 1])
axes[0].imshow(net.layers[0].weights)
axes[1].imshow(net.layers[1].weights)
# %%
