import numpy as np

from helpers import eye, matMul


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
        return self.a.eval(at) + self.b.eval(at)
    
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
        return self.a.eval(at) - self.b.eval(at)
    
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
        return self.a.eval(at) * self.b.eval(at)
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a:
            return grad_s_node @ self.b.eval(at)
        if v == self.b:
            return grad_s_node @ self.a.eval(at)
        
    def getVariables(self):
        return [self.a, self.b]
    
    def __str__(self):
        return f"({self.a} * {self.b})"


class Sin(Node):
    def __init__(self, a):
        self.a = a

    def eval(self, at):
        aV = self.a.eval(at)
        return np.sin(aV)
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a:
            aV = self.a.eval(at)
            return grad_s_node @ np.cos(aV)
        
    def getVariables(self):
        return [self.a]

    def __str__(self):
        return f"sin({self.a})"


class Exp(Node):
    def __init__(self, a):
        self.a = a

    def eval(self, at):
        aV = self.a.eval(at)
        return np.exp(aV)
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a:
            aV = self.a.eval(at)
            grad_node_v = np.eye(len(aV)) * (aV * np.exp(aV))
            return grad_s_node @ grad_node_v

    def getVariables(self):
        return [self.a]
    
    def __str__(self):
        return f"exp({self.a})"


class MatMul(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, at):
        aV = self.a.eval(at)
        bV = self.b.eval(at)
        return aV @ bV
    
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

        if v == self.a:
            bV = self.b.eval(at)
            return matMul(grad_s_node, bV.T)
        if v == self.b:
            aV = self.a.eval(at)
            return matMul(aV.T, grad_s_node)
    
    def getVariables(self):
        return [self.a, self.b]
        
    def __str__(self):
        return f"({self.a} @ {self.b})"


class InnerSum(Node):
    def __init__(self, v):
        self.v = v

    def eval(self, at):
        vVal = self.v.eval(at)
        return np.sum(vVal)

    def grad_s_v(self, v, at, grad_s_node):
        if v == self.v:
            vVal = self.v.eval(at)
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
        aVal = self.a.eval(at)
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
        aVal = self.a.eval(at)
        aPowS = np.power(aVal, self.scalar)
        return aPowS
    
    def grad_s_v(self, v, at, grad_s_node):
        if v == self.a:
            aVal = self.a.eval(at)
            singleValues = self.scalar * np.power(aVal, self.scalar - 1)
            grad_node_x = np.eye(len(singleValues)) * singleValues
            return grad_s_node @ grad_node_x

    def getVariables(self):
        return [self.a]
    
    def __str__(self):
        return f"{self.a}^{self.scalar}"



# @memoized()
def grad_s_x_through_op(op, x, at, grad_s_op):
    if op == x:
        return grad_s_op
    grad_s_x_total = 0
    for v in op.getVariables():
        grad_s_v = op.grad_s_v(v, at, grad_s_op)
        if (type(v) is not Constant) and (grad_s_v.shape != v.eval(at).shape):
            raise Exception(f"Something went wrong. grad_s_v must have shape {v.eval(at).shape} but has shape {grad_s_v.shape}.")
        grad_s_x_total += grad_s_x_through_op(v, x, at, grad_s_v)
    return grad_s_x_total



def gradient(op, x, at):
    opV = op.eval(at)
    if opV.shape != ():
        raise Exception(f"Can only do gradients on scalar-valued expressions. This expression has shape {opV.shape}: {opV}")
    grad_op_x_Val = grad_s_x_through_op(op, x, at, np.array(1.0))
    return grad_op_x_Val
