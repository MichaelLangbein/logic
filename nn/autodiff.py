#%%
import numpy as np

#%%


def matMul(m1, m2):
    m1s = np.squeeze(m1)
    m2s = np.squeeze(m2)
    if m1s.shape == () or m2s.shape == ():
        result = np.squeeze(m1s * m2s)
    else:
        result = np.squeeze(m1s @ m2s)
    if result.shape == ():
        return np.array([result])
    return result


class Node:
    def eval(self) -> np.array:
        raise Exception('Eval not implemented')

    def diff(self, node) -> np.array:
        raise Exception('Diff not implemented')

    def id(self) -> str:
        raise Exception('Id not implemented')

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return __o.id() == self.id()
        return False


class Variable(Node):
    def __init__(self, value: np.array):
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
            return np.zeros(self.value.shape)

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
    def __init__(self, nodes):
        self.nodes = nodes

    def id(self):
        ids = [n.id() for n in self.nodes].join(", ")
        return f"PwProd({ids})"

    def eval(self):
        nodeVals = [n.eval() for n in self.nodes]
        return np.prod(nodeVals, 0)

    def diff(self, variable: Variable):
        if self == variable:
            return np.eye(self.eval().shape[0])
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
        return s * np.diag(apowsm1) @ da_dx

    def __str__(self) -> str:
        return f"({self.a})^{self.s}"


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
