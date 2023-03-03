import numpy as np
from helpers import eye, matMul, memoized


class Node():
    def eval(self, at):
        pass
    def grad_s_v(self, v, at, grad_s_node):
        """
            returns grad_s_v 
            by calculating grad_s_node @ grad_node_v
            v must be a variable of the node;
            i.e. grad_node_v must be a shallow gradient.
            otherwise returns None
        """
        pass
    def getVariables(self):
        pass
    def __str__(self):
        pass
    def __repr__(self):
        return self.__str__()


class Constant(Node):
    def __init__(self, value):
        if not type(value) is np.ndarray:
            value = np.array(value)
        self.value = value

    def eval(self, at):
        return self.value
    
    def grad_s_v(self, v, at, grad_s_node):
        return np.zeros(grad_s_node.shape)

    def getVariables(self):
        return []

    def __str__(self):
        return f"{self.value}"


class Variable(Node):
    def __init__(self, name):
        self.name = name

    def eval(self, at):
        if self.name in at:
            return at[self.name]
        
    def grad_s_v(self, v, at, grad_s_node):
        if self == x:
            return grad_s_node
    
    def getVariables(self):
        return []
    
    def __str__(self):
        return f"{self.name}"


class Plus(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, at):
        return  eval(self.a, at) +  eval(self.b, at)
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a or v == self.b:
            return grad_s_node

    def getVariables(self):
        return [self.a, self.b]
        
    def __str__(self):
        return f"({self.a} + {self.b})"
    

class Minus(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, at):
        return eval(self.a, at) - eval(self.b, at)
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a:
            return grad_s_node
        if v == self.b:
            return -grad_s_node

    def getVariables(self):
        return [self.a, self.b]
        
    def __str__(self):
        return f"({self.a} - {self.b})"
    
   
class Mult(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, at):
        return eval(self.a, at) * eval(self.b, at)
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a:
            return matMul(grad_s_node, eval(self.b, at), 1)
        if v == self.b:
            return matMul(grad_s_node, eval(self.a, at), 1)
        
    def getVariables(self):
        return [self.a, self.b]
    
    def __str__(self):
        return f"({self.a} * {self.b})"


class Exp(Node):
    def __init__(self, a):
        self.a = a

    def eval(self, at):
        aV = eval(self.a, at)
        return np.exp(aV)
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a:
            aV = eval(self.a, at)
            grad_node_v = np.eye(len(aV) if aV.shape else 1) * (aV * np.exp(aV))
            return matMul(grad_s_node, grad_node_v, 1)

    def getVariables(self):
        return [self.a]
    
    def __str__(self):
        return f"exp({self.a})"


class MatMul(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, at):
        aV = eval(self.a, at)
        bV = eval(self.b, at)
        return matMul(aV, bV, 1)
    
    def grad_s_v(self, v, at, grad_s_node):
        """
          Important:
          ----------

          this assumes that  this expression ` Node=A@B `
          is part of a larger expression ` f(Node) `, which is scalar valued.
          If that's the case, then

          `` df/dA = df/dNode * dNode/dA = df/dNode * B^T ``

          and

          `` df/dB = df/dNode * dNode/dB = A^T * df/dNode``
          
          https://mostafa-samir.github.io/auto-diff-pt2/
        """

        vVal = eval(v, at)
        if v == self.a:
            bV =  eval(self.b, at)
            (a, b, nrDims) = self.__reshape(vVal, grad_s_node, bV.T)
            return matMul(a, b, nrDims)
        if v == self.b:
            aV =  eval(self.a, at)
            (a, b, nrDims) = self.__reshape(vVal, aV.T, grad_s_node)
            return matMul(a, b, nrDims)
        
    def __reshape(self, target, a, b):
        resultShape = a.shape[:-1] + b.shape[1:]
        if resultShape == target.shape:
            return (a, b, 1)
        if len(resultShape) < len(target.shape):
            a = np.reshape(a, a.shape + (1,))
            b = np.reshape(b, (1,) + b.shape)
            return self.__reshape(target, a, b)

    
    def getVariables(self):
        return [self.a, self.b]
        
    def __str__(self):
        return f"({self.a} @ {self.b})"


class InnerSum(Node):
    def __init__(self, v):
        self.v = v

    def eval(self, at):
        vVal =  eval(self.v, at)
        return np.sum(vVal)

    def grad_s_v(self, v, at, grad_s_node):
        if v == self.v:
            vVal =  eval(self.v, at)
            grad_node_v = np.ones(vVal.shape)
            return grad_s_node * grad_node_v

    def getVariables(self):
        return [self.v]
    
    def __str__(self):
        return f"sum({self.v})"


class ScalarProd(Node):
    def __init__(self, scalar, a):
        self.a = a
        self.scalar = scalar

    def eval(self, at):
        aVal =  eval(self.a, at)
        aTimesS = aVal * self.scalar
        return aTimesS
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a:
            return self.scalar * grad_s_node

    def getVariables(self):
        return [self.a]
    
    def __str__(self):
        return f"({self.scalar} * {self.a})"


class ScalarPower(Node):
    def __init__(self, a, scalar):
        self.a = a
        self.scalar = scalar

    def eval(self, at):
        aVal =  eval(self.a, at)
        aPowS = np.power(aVal, self.scalar)
        return aPowS
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a:
            aVal =  eval(self.a, at)
            singleValues = self.scalar * np.power(aVal, self.scalar - 1)
            grad_node_x = np.eye(len(singleValues)) * singleValues
            return grad_s_node @ grad_node_x

    def getVariables(self):
        return [self.a]
    
    def __str__(self):
        return f"{self.a}^{self.scalar}"


class Transpose(Node):
    def __init__(self, a):
        self.a = a

    def eval(self, at):
        aVal = eval(self.a, at)
        return aVal.T
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a:
            return grad_s_node
        
    def getVariables(self):
        return [self.a]
    
    def __str__(self):
        return f"{self.a}^T"


def Sigmoid(x):
    minX = ScalarProd(-1, x)
    ex = Exp(minX)
    one = Constant(1)
    body = Plus(one, ex)
    sigmoid = ScalarPower(body, -1)
    return sigmoid


def Divide(numerator, denominator):
    result = Mult(numerator, ScalarPower(denominator, -1.0))
    return result


def Softmax(x):
    ex = Exp(x)
    sm = InnerSum(ex)
    softmax = Divide(ex, sm)
    return softmax


def Sse(observation, simulation):
    errors = Minus(observation, simulation)
    squaredErrors = ScalarPower(errors, 2)
    sse = InnerSum(squaredErrors)
    return sse


@memoized
def eval(op, at):
    return op.eval(at)


@memoized
def grad_s_x_through_op(op, x, at, grad_s_op):
    if op == x:
        return grad_s_op
    grad_s_x_total = 0
    for v in op.getVariables():
        grad_s_v = op.grad_s_v(v, at, grad_s_op)
        if (type(v) is not Constant) and (grad_s_v.shape != eval(v, at).shape):
            grad_s_v = op.grad_s_v(v, at, grad_s_op)
            raise Exception(f"Something went wrong with {op.__class__.__name__}. grad_s_v must have shape {eval(v, at).shape} but has shape {grad_s_v.shape}.")
        grad_s_x_total += grad_s_x_through_op(v, x, at, grad_s_v)
    return grad_s_x_total



def gradient(op, x, at):
    opV = eval(op, at)
    if opV.shape != ():
        raise Exception(f"Can only do gradients on scalar-valued expressions. This expression has shape {opV.shape}: {opV}")
    grad_op_x_Val = grad_s_x_through_op(op, x, at, np.array(1.0))
    return grad_op_x_Val



