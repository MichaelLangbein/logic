#%%
import numpy as np



#%%


def matMul(m1, m2):
    if type(m1) == int or type(m2) == int:
        return np.squeeze(m1 * m2)
    return np.squeeze(m1 @ m2)


class Node:
    def eval(self) -> np.array:
        raise Exception('Eval not implemented')

    def diff(self, node) -> np.array:
        raise Exception('Diff not implemented')


class Variable(Node):
    def __init__(self, value: np.array):
        self.value = value

    def eval(self):
        return self.value

    def diff(self, variable: Node):
        if self == variable:
            return np.eye(self.value.shape[0])
        else:
            return np.zeros(self.value.shape)



class Zero(Variable):
    def __init__(self, shape):
        super().__init__(np.zeros(shape))


class One(Variable):
    def __init__(self, shape):
        super().__init__(np.ones(shape))



class Add(Node):
    def __init__(self, n1: Node, n2: Node):
        self.n1 = n1
        self.n2 = n2

    def eval(self):
        return self.n1.eval() + self.n2.eval()

    def diff(self, var: Node):
        return self.n1.diff(var) + self.n2.diff(var)


class Min(Node):
    def __init__(self, n1: Node, n2: Node):
        self.n1 = n1
        self.n2 = n2

    def eval(self):
        return self.n1.eval() - self.n2.eval()

    def diff(self, var: Node):
        return self.n1.diff(var) - self.n2.diff(var)



class Mult(Node):
    def __init__(self, n1: Node, n2: Node):
        self.n1 = n1
        self.n2 = n2

    def eval(self):
        return matMul(self.n1.eval(), self.n2.eval())

    def diff(self, var: Node):
        return matMul(self.n1.diff(var), self.n2.eval()) + matMul(self.n1.eval(), self.n2.diff(var))


class Inv(Node):
    def __init__(self, n: Node):
        self.n = n

    def eval(self):
        return np.invert(self.n.eval())

    def diff(self, var):
        """ https://math.stackexchange.com/questions/1471825/derivative-of-the-inverse-of-a-matrix """
        nV = self.n.eval()
        nD = self.n.diff(var)
        nI = np.invert(nV)
        return - matMul(nI, matMul(nD, nI))



class Div(Node):
    def __init__(self, n1: Node, n2: Node):
        self.n = Mult(n1, Inv(n2))

    def eval(self):
        return self.n.eval()

    def diff(self, var: Node):
        return self.n.diff(var)


class Exp(Node):
    def __init__(self, n: Node):
        self.n = n

    def eval(self):
        return np.exp(self.n.eval())

    def diff(self, var: Node):
        nD = self.n.diff(var)
        eV = self.eval()
        return nD * eV


class PwDiv(Node):
    """
        point-wise divide
    """
    def __init__(self, a: Node, b: Node):
        self.nodes = [a, b]

    def eval(self):
        [aV, bV] = [n.eval() for n in self.nodes]
        return np.divide(aV, bV)

    def diff(self, variable: Variable):
        [a, b] = [n.eval() for n in self.nodes]
        [da, db] = [n.diff(variable) for n in self.nodes]
        return (da * b - a * db) / b**2


        
class PwProd:
    """
        Point-wise product
    """
    def __init__(self, nodes):
        self.nodes = nodes

    def eval(self):
        nodeVals = [n.eval() for n in self.nodes]
        return np.prod(nodeVals, 0)

    def diff(self, variable: Variable):
        """
            d/dx uv = (du/dx)^T v  +  (dv/dx)^T u
            d/du uv = (du/du)^T v
                    = eye * v
        """
        nodeVals = [n.eval() for n in self.nodes]
        nodeDiffs = [n.diff(variable) for n in self.nodes]
        s = np.zeros(nodeDiffs[0].shape)
        for i in range(len(self.nodes)):
            p = np.ones(nodeDiffs[0].shape)
            for j in range(len(self.nodes)):
                e = nodeDiffs[j].transpose() if i == j else nodeVals[j]
                p *= e
            s += p
        return s




class ScalarMult(Node):
    def __init__(self, scalar: float, node: Node):
        self.scalar = scalar
        self.node = node

    def eval(self):
        nodeVal = self.node.eval()
        return self.scalar * nodeVal

    def diff(self, variable: Variable):
        diffVal = self.node.diff(variable)
        return self.scalar * diffVal


class InnerSum(Node):
    def __init__(self, node: Node):
        self.node = node
    
    def eval(self):
        nodeVal = self.node.eval()
        return np.sum(nodeVal)

    def diff(self, variable: Variable):
        """
            d/dx sum(u) = [d/dx1 sum(u), d/dx2 sum(u), ...]
                        = col_sum(du/dx)
        """
        nodeDiff = self.node.diff(variable)
        return np.sum(nodeDiff, 0)



def Sigmoid(x: Node):
    num = One(1)
    negX = ScalarMult(-1, x)
    den = Add(One(1), Exp(negX))
    return PwDiv(num, den)


def Softmax(x: Node):
    num = Exp(x)
    den = InnerSum(Exp(x))
    return PwDiv(num, den)



# %%
