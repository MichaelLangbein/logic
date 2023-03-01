from abc import ABC
import numpy as np

from helpers import matMul


class Node(ABC):
    def eval(self, at):
        pass
    def derivative(self, wrt, at):
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
    
    def derivative(self, wrt, at):
        return np.array(0.0)

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
        
    def derivative(self, wrt, at):
        if self.name == wrt.name:
            return np.array(1.0)
        return np.array(0.0)
    
    def getVariables(self):
        return []
    
    def __str__(self):
        return f"{self.name}"


class Add(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, at):
        return self.a.eval(at) + self.b.eval(at)
    
    def derivative(self, wrt, at):
        return np.array(1.0)

    def getVariables(self):
        return [self.a, self.b]
        
    def __str__(self):
        return f"({self.a} + {self.b})"
    
   
class Mult(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, at):
        return self.a.eval(at) * self.b.eval(at)
    
    def derivative(self, wrt, at):
        if wrt == self.a:
            return self.b.eval(at)
        if wrt == self.b:
            return self.a.eval(at)
        
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
    
    def derivative(self, wrt, at):
        if wrt == self.a:
            aV = self.a.eval(at)
            return np.cos(aV)
        
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
    
    def derivative(self, wrt, at):
        if wrt == self.a:
            aV = self.a.eval(at)
            return aV * np.exp(aV)

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
    
    def derivative(self, wrt, at):
        """
          Important:
          ----------

          this assumes that  this expression ` U=A@B `
          is part of a larger expression ` f(U) `, which is scalar valued.
          If that's the case, then

          `` df/dA = df/dU * dU/dA = df/dU * B^T ``

          and

          `` df/dB = df/dU * dU/dB = df/dU * A^T ``
          
          https://mostafa-samir.github.io/auto-diff-pt2/
        """

        if wrt == self.a:
            bV = self.b.eval(at)
            return bV.T
        if wrt == self.b:
            aV = self.a.eval(at)
            return aV.T
    
    def getVariables(self):
        return [self.a, self.b]
        
    def __str__(self):
        return f"({self.a} @ {self.b})"


class Sum(Node):
    def __init__(self, v):
        self.v = v

    def eval(self, at):
        vVal = self.v.eval(at)
        return np.sum(vVal)

    def derivative(self, wrt, at):
        if wrt == self.v:
            vVal = self.v.eval(at)
            return np.ones(vVal.shape)

    def getVariables(self):
        return [self.v]
    
    def __str__(self):
        return f"sum({self.v})"



def __shape(undeep, total):
    targetShape = total.shape
    sourceShape = undeep.shape
    newShape = sourceShape + targetShape
    return newShape


def __derivative(node, wrt, at, shape):
    print(f"Derivative d {node} / d {wrt}")
    total = np.zeros(shape)
    for variable in node.getVariables():
        if type(variable) is Constant:
            continue
        if variable == wrt:
            total += node.derivative(variable, at).T
        else:
            undeep = node.derivative(variable, at) 
            deep = __derivative(variable, wrt, at, __shape(undeep, total))
            partial = matMul(undeep, deep)
            total += partial
    return total

def derivative(node, wrt, at):
    nodeV = node.eval(at)
    if nodeV.shape != ():
        raise Error(f"Can only do derivatives on scalar-valued expressions. This expression has shape {nodeV.shape}: {nodeV}")
    wrtV = wrt.eval(at)
    d_node_d_wrt = __derivative(node, wrt, at, wrtV.shape)
    return d_node_d_wrt