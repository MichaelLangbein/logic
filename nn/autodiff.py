#%%
import numpy as np
import Tensor from tensor


# Derivatives on tensors: https://www.et.byu.edu/~vps/ME505/AAEM/V5-07.pdf
# https://explained.ai/matrix-calculus/index.html#sec:1.3

"""
# TODOs
 - the test `if var == self` can probably be moved into Node
 - the function `id()` can probably be moved into Node (but requires some introspection)
"""

#%%


class Node:
    def eval(self) -> np.array:
        raise Exception('Eval not implemented')

    def diff(self, node) -> np.array:
        raise Exception('Diff not implemented')

    # def id(self) -> str:
    #     className = self.__class__.__name__
    #     attributeNames = inspect.getargspec(Super.__init__)
    #     args = [self.__getattribute__(name) for name in attributeNames]
    #     argsString = [arg.id() for arg in args].join(", ")
    #     return f"{className}(${argsString})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return __o.id() == self.id()
        return False


class Variable(Node):
    def __init__(self, value: Tensor):
        self.value = value
        self.__id = f"{np.random.rand()}{np.random.rand()}"

    def id(self):
        return self.__id

    def eval(self):
        return self.value

    def diff(self, variable: Node):
        if self == variable:
            return np.eye(self.value.shape[0])
        else:
            return 0

    def __str__(self) -> str:
        return f"{self.value}"


class Zero(Variable):
    def __init__(self, shape):
        super().__init__(np.zeros(shape))

    def __str__(self) -> str:
        return "0"


class One(Variable):
    def __init__(self, shape):
        super().__init__(np.ones(shape))

    def __str__(self) -> str:
        return "1"


class Add(Node):
    def __init__(self, n1: Node, n2: Node):
        self.n1 = n1
        self.n2 = n2

    def id(self):
        return f"Add({self.n1.id()}, {self.n2.id()})"

    def eval(self):
        return self.n1.eval() + self.n2.eval()

    def diff(self, var: Node):
        if self == var:
            return np.eye(self.eval().shape[0])
        return self.n1.diff(var) + self.n2.diff(var)

    def __str__(self) -> str:
        return f"{self.n1} + {self.n2}"


class Minus(Node):
    def __init__(self, n1: Node, n2: Node):
        self.n1 = n1
        self.n2 = n2

    def id(self):
        return f"Minus({self.n1.id()}, {self.n2.id()})"

    def eval(self):
        return self.n1.eval() - self.n2.eval()

    def diff(self, var: Node):
        if self == var:
            return np.eye(self.eval().shape[0])
        return self.n1.diff(var) - self.n2.diff(var)

    def __str__(self) -> str:
        return f"{self.n1} - {self.n2}"


class Mult(Node):
    def __init__(self, n1: Node, n2: Node):
        self.n1 = n1
        self.n2 = n2

    def id(self):
        return f"Mult({self.n1.id()}, {self.n2.id()})"

    def eval(self):
        return matMul(self.n1.eval(), self.n2.eval())

    def diff(self, var: Node):
        if self == var:
            return np.eye(self.eval().shape[0])
        n1 = self.n1.eval()
        n2 = self.n2.eval()
        d_n1 = self.n1.diff(var)
        d_n2 = self.n2.diff(var)
        return matMul(d_n1, n2) + matMul(n1, d_n2)

    def __str__(self) -> str:
        return f"{self.n1} * {self.n2}"


class Inv(Node):
    def __init__(self, n: Node):
        self.n = n

    def id(self):
        return f"Inv({self.n.id()})"

    def eval(self):
        return np.invert(self.n.eval())

    def diff(self, var):
        """ https://math.stackexchange.com/questions/1471825/derivative-of-the-inverse-of-a-matrix """
        if self == var:
            return np.eye(self.eval().shape[0])
        nV = self.n.eval()
        nD = self.n.diff(var)
        nI = np.invert(nV)
        return - matMul(nI, matMul(nD, nI))

    def __str__(self) -> str:
        return f"({self.n})^-1"


class Div(Node):
    def __init__(self, n1: Node, n2: Node):
        self.n = Mult(n1, Inv(n2))

    def id(self):
        return f"Div({self.n.id()})"

    def eval(self):
        return self.n.eval()

    def diff(self, var: Node):
        if self == var:
            return np.eye(self.eval().shape[0])
        return self.n.diff(var)

    def __str__(self) -> str:
        return f"{self.n}"


class Exp(Node):
    def __init__(self, n: Node):
        self.n = n

    def id(self):
        return f"Exp({self.n.id()})"

    def eval(self):
        return np.exp(self.n.eval())

    def diff(self, var: Node):
        if self == var:
            return np.eye(self.eval().shape[0])
        nD = self.n.diff(var)
        eV = self.eval()
        return nD * eV

    def __str__(self) -> str:
        return f"exp({self.n})"


class Ln(Node):
    def __init__(self, u: Node):
        self.u = u

    def id(self):
        return f"Ln({self.u.id()})"

    def eval(self):
        return np.log(self.u.eval())

    def diff(self, var: Node):
        if self == var:
            return np.eye(self.eval().shape[0])
        u = self.u.eval()
        uD = self.u.diff(var)
        ddu_lnu = np.diag(1 / u)
        return matMul(ddu_lnu, uD)

    def __str__(self) -> str:
        return f"ln({self.u})"


class PwDiv(Node):
    """
        point-wise divide
    """
    def __init__(self, a: Node, b: Node):
        self.a = a
        self.b = b

    def id(self):
        return f"PwDiv({self.a.id()}, {self.b.id()})"

    def eval(self):
        aV = self.a.eval()
        bV = self.b.eval()
        return np.divide(aV, bV)

    def diff(self, variable: Variable):
        if self == variable:
            return np.eye(self.eval().shape[0])
        a = self.a.eval()
        b = self.b.eval()
        da = self.a.diff(variable)
        db = self.b.diff(variable)
        return (da * b - a * db) / b**2

    def __str__(self) -> str:
        return f"({self.a} ./ {self.b})"

        
class PwProd:
    """
        Point-wise product
    """
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def id(self):
        ids = f"{self.a.id()}, {self.b.id()}"
        return f"PwProd({ids})"

    def eval(self):
        aVal = self.a.eval()
        bVal = self.b.eval()
        return np.prod([aVal, bVal], 0)

    def diff(self, variable: Variable):
        if self == variable:
            return np.eye(self.eval().shape[0])
        """
            d/dx uv = (du/dx)^T v  +  (dv/dx)^T u
            d/du uv = (du/du)^T v
                    = eye * v
        """
        aVal = self.a.eval()
        bVal = self.b.eval()
        aSqu = matMul(np.eye(aVal.shape[0]), aVal)
        bSqu = matMul(np.eye(bVal.shape[0]), bVal)
        aDif = self.a.diff(variable)
        bDif = self.b.diff(variable)
        aDifT = aDif if np.isscalar(aDif) else aDif.transpose()
        bDifT = bDif if np.isscalar(bDif) else bDif.transpose()
        s = matMul(aDifT, bSqu) + matMul(bDifT, aSqu)
        return s

    def __str__(self) -> str:
        entries = [n for n in self.nodes].join(", ")
        return f"prod({entries})"


class ScalarMult(Node):
    def __init__(self, scalar: float, node: Node):
        self.scalar = scalar
        self.node = node

    def id(self):
        return f"ScalarMult({self.scalar}, {self.node.id()})"

    def eval(self):
        nodeVal = self.node.eval()
        return self.scalar * nodeVal

    def diff(self, variable: Variable):
        if self == variable:
            return np.eye(self.eval().shape[0])
        diffVal = self.node.diff(variable)
        return self.scalar * diffVal

    def __str__(self) -> str:
        return f"{self.scalar} * {self.node}"


class InnerSum(Node):
    def __init__(self, node: Node):
        self.node = node

    def id(self):
        return f"InnerSum({self.node.id()})"
    
    def eval(self):
        nodeVal = self.node.eval()
        return np.sum(nodeVal)

    def diff(self, variable: Variable):
        if self == variable:
            return np.eye(self.eval().shape[0])
        """
            d/dx sum(u) = [d/dx1 sum(u), d/dx2 sum(u), ...]
                        = col_sum(du/dx)
        """
        nodeDiff = self.node.diff(variable)
        return np.sum(nodeDiff, 0)

    def __str__(self) -> str:
        return f"innersum({self.node})"


# def Pow(Node):
#     def __init__(self, base: Node, pow: Node):
#         self.base = base
#         self.pow = pow

#     def eval(self):
#         return np.power(self.base.eval(), self.pow.eval())

#     def diff(self, var: Node):
#         """
#             a = e^log(a)
#             a^b = e^(log(a) * b)
#             d a^b / dx = d/dx e^(log(a) * b)
#                        = d/dx (log(a) * b) e^(log(a) * b)
#                        = d/dx (log(a) * b) a^b
#                        = (a'b/a + log(a)b') * a^b
#         """


class ScalarPower(Node):
    def __init__(self, a: Node, s: float):
        self.a = a
        self.s = s

    def id(self):
        return f"ScalarPower({self.a.id()}, {self.s})"

    def eval(self):
        av = self.a.eval()
        return np.power(av, self.s)

    def diff(self, x: Node):
        if self == x:
            return np.eye(self.eval().shape[0])
        """
            d/dx a^s = s a^(s-1) da/dx

        """
        s = self.s
        av = self.a.eval()
        apowsm1 = av**(s-1)
        da_dx = self.a.diff(x)
        return s * matMul(apowsm1, da_dx)

    def __str__(self) -> str:
        return f"({self.a})^{self.s}"


# class Sigmoid(Node):
#     def __init__(self, a: Node):
#         # input
#         self.a = a
#         # sigmoid of input
#         num = One(1)
#         negX = ScalarMult(-1, self.a)
#         den = Add(One(1), Exp(negX))
#         sigmoid = PwDiv(num, den)
#         # store for later
#         self.func = sigmoid

#     def id(self):
#         return f"Sigmoid({self.a.id()})"

#     def eval(self):
#         return self.func.eval()

#     def diff(self, x: Node):
#         if self == x:
#             return np.eye(self.eval().shape[0])
#         return self.func.diff(x)

#     def __str__(self) -> str:
#         return f"Sigmoid({self.a})"


def Sigmoid(x: Node):
    num = One(1)
    negX = ScalarMult(-1, x)
    den = Add(One(1), Exp(negX))
    return PwDiv(num, den)


def Softmax(x: Node):
    num = Exp(x)
    den = InnerSum(Exp(x))
    return PwDiv(num, den)


def SSE(y: Node, yObs: np.array):
    yObsV = Variable(yObs)
    eV = Minus(y, yObsV)
    seV = ScalarPower(eV, 2)
    sseV = InnerSum(seV)
    return sseV


# %%
