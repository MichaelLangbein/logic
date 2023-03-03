import unittest as ut
import numpy as np
from nodes import Variable, MatMul, Plus, Transpose, Sigmoid, Softmax, Sse, gradient
from nn import FullyConnectedLayer, SelfAttentionLayer


class NnTests(ut.TestCase):
   
    def testPrimitive(self):

        i = Variable('i')
        yObs = Variable('yObs')

        W1 = Variable('W1')
        b1 = Variable('b1')
        x1 = Plus(MatMul(W1, i), b1)
        y1 = Sigmoid(x1)

        W2 = Variable('W2')
        b2 = Variable('b2')
        x2 = Plus(MatMul(W2, y1), b2)
        y2 = Sigmoid(x2)

        e = Sse(yObs, y2)

        values = {
            'i':    np.random.random([3]),
            'b1':   np.random.random([2]),
            'W1':   np.random.random([2, 3]),
            'b2':   np.random.random([2]),
            'W2':   np.random.random([2, 2]),
            'yObs': np.random.random([2])
        }

        e0 = e.eval(values)

        alpha = 0.01
        N = 10
        for i in range(N):
            dedW2 = gradient(e, W2, values)
            dedb2 = gradient(e, x2, values)
            dedW1 = gradient(e, W1, values)
            dedb1 = gradient(e, x1, values)
            values['W2'] += alpha * dedW2
            values['b2'] += alpha * dedb2
            values['W1'] += alpha * dedW1
            values['b1'] += alpha * dedb1

            ei = e.eval(values)
            print(f"{round(100 * i/N)}% - {ei}")

        self.assertLess(ei, e0)

    def testFullyConnected(self):
        observation = Variable("observation")
        input = Variable("input")
        layer1 = FullyConnectedLayer("layer1", 4, 3, input)
        layer2 = FullyConnectedLayer("layer2", 3, 2, layer1.getOutput())
        layer3 = FullyConnectedLayer("layer3", 2, 2, layer2.getOutput())
        err = Sse(observation, layer3.getOutput())

        inputTrue = np.random.random(4)
        obsvnTrue = np.random.random(2)

        at = {
            'input': inputTrue,
            'observation': obsvnTrue
        }
        at.update(layer1.getParaValues())
        at.update(layer2.getParaValues())
        at.update(layer3.getParaValues())

        eInitial = err.eval(at)

        N = 10
        for i in range(N):
            layer1.update(err, at)
            layer2.update(err, at)
            layer3.update(err, at)
            at.update(layer1.getParaValues())
            at.update(layer2.getParaValues())
            at.update(layer3.getParaValues())
            print(f"{round(100 * i/N)}% - {err.eval(at)}")

        eFinal = err.eval(at)
        self.assertLess(eFinal, eInitial)

    def testSelfAttention(self):
        """
        Task: sentiment-analysis
            Take in restaurant-reviews
            Analyze sentiment
        """

        sentence = Variable("sentence")
        sentiment = Variable("sentiment")

        embedder = FullyConnectedLayer("Word embedder", 20, 4, sentence)
        attention = SelfAttentionLayer("Self attention", embedder.getOutput())
        interpreter = FullyConnectedLayer("Interpreter", 4, 1, attention.getOutput())
        err = Sse(sentiment, interpreter.getOutput())

        sentenceValue = np.random.random(20)
        sentimentValue = np.random.random(1)

        at = {
            'sentence': sentenceValue,
            'sentiment': sentimentValue
        }
        at.update(embedder.getParaValues())
        at.update(interpreter.getParaValues())

        eInitial = err.eval(at)

        N = 30
        for i in range(N):
            embedder.update(err, at)
            interpreter.update(err, at)
            at.update(embedder.getParaValues())
            at.update(interpreter.getParaValues())
            print(f"{round(100 * i/N)}% - {err.eval(at)}")
        
        eFinal = err.eval(at)
        self.assertLess(eFinal, eInitial)





if __name__ == '__main__':
    ut.main()