from abc import ABC
import numpy as np


class Node(ABC):
    def eval(self, at):
        pass
    def derivative(self, wrt, at):
        pass
    def getVariables(self):
        pass


class Constant(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, at):
        return self.value
    
    def derivative(self, wrt, at):
        return 0

    def getVariables(self):
        return []


class Variable(Node):
    def __init__(self, name):
        self.name = name

    def eval(self, at):
        if self.name in at:
            return at[self.name]
        
    def derivative(self, wrt, at):
        if self.name == wrt.name:
            return 1
        return 0
    
    def getVariables(self):
        return [self]


class Add(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, at):
        return self.a.eval(at) + self.b.eval(at)
    
    def derivative(self, wrt, at):
        return 1

    def getVariables(self):
        return [self.a, self.b]
   
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


def eval(node, at):
    return node.eval(at)


def derivative(node, wrt, at):
    if node == wrt:
        return 1
    total = 0
    for variable in node.getVariables():
        #         undeep                          deep
        partial = node.derivative(variable, at) * derivative(variable, wrt, at)
        total += partial
    return total