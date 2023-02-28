from abc import ABC
import numpy as np


class Node(ABC):
    def eval(self, at):
        pass
    def derivative(self, wrt, at):
        pass


class Constant(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, at):
        return self.value
    
    def derivative(self, wrt, at):
        return 0


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


class Add(Node):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, at):
        return self.a.eval(at) + self.b.eval(at)
    
    def derivative(self, wrt, at):
        return 1

   
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
    
        

def eval(node, at):
    return node.eval(at)


def derivative(node, wrt):
    total = 0
    for variable in node.variables:
        #         undeep                      deep
        partial = node.derivative(variable) * derivative(variable, wrt)
        total += partial
    return total