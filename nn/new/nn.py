from nodes import Constant, InnerSum, Plus, ScalarPower, Minus, ScalarProd, Exp


def Sigmoid(x):
    minX = ScalarProd(-1, x)
    ex = Exp(minX)
    one = Constant(1)
    body = Plus(one, ex)
    sigm = ScalarPower(body, -1)
    return sigm

def Sse(observation, simulation):
    obsVar = Constant(observation)
    errors = Minus(obsVar, simulation)
    squaredErrors = ScalarPower(errors, 2)
    sse = InnerSum(squaredErrors)
    return sse


