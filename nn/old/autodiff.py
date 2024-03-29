#%%
import numpy as np

from helpers import diffBySelf, eye, isZero, matMul, zeros




"""
# TODOs
 - the test `if var == self` can probably be moved into Node
 - the function `id()` can probably be moved into Node (but requires some introspection)
"""

#%%

# Derivatives on tensors: https://www.et.byu.edu/~vps/ME505/AAEM/V5-07.pdf
# https://explained.ai/matrix-calculus/index.html#sec:1.3


"""
x: dimensions (n)
y: dimensions(m)
dy/dx: (m*n)

x: dimensions (n)
Y: dimensions (u*v)
xY/dx: (u*v*n)

X: dimensions (n*m)
Y: dimensions (u*v)
dY/dX: (u*v*n*m)
"""
"""
y.diff(x)

is understood to be 

dy |
-- |
dx |
   |x_0


so that we can do gradient descent:
y_1 = y_0 - \alpha y'|_x_0
"""

#%%


class Node:
    def eval(self) -> np.array:
        raise Exception('Eval not implemented')

    def grad(self, node) -> np.array:
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
    def __init__(self, value):
        self.value = value
        self.__id = f"{np.random.rand()}{np.random.rand()}"

    def id(self):
        return self.__id

    def eval(self):
        return self.value

    def grad(self, variable: Node):
        v = self.eval()
        o = variable.eval()
        gradientDims = v.shape + o.shape
        if self == variable:
            return diffBySelf(v.shape)
        else:
            return zeros(*gradientDims)

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

    def grad(self, var: Node):
        if self == var:
            v = self.eval()
            return diffBySelf(v.shape)
        grad_n1_v = self.n1.grad(var)
        grad_n2_v = self.n2.grad(var)
        return grad_n1_v + grad_n2_v

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

    def grad(self, var: Node):
        if self == var:
            v = self.eval()
            return diffBySelf(v.shape)
        return self.n1.grad(var) - self.n2.grad(var)

    def __str__(self) -> str:
        return f"{self.n1} - {self.n2}"


class Mult(Node):
    # https://math.stackexchange.com/questions/1866757/not-understanding-derivative-of-a-matrix-matrix-product
    # https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf
    # https://math.stackexchange.com/questions/366922/product-rule-for-matrix-functions
    # https://www.cs.cmu.edu/~epxing/Class/10701-08s/recitation/mc.pdf: page 505, formula (1366)
    # https://math.stackexchange.com/questions/1819202/product-rule-for-matrix-valued-functions-and-differentiability-of-matrix-multipl
    def __init__(self, n1: Node, n2: Node):
        self.n1 = n1
        self.n2 = n2

    def id(self):
        return f"Mult({self.n1.id()}, {self.n2.id()})"

    def eval(self):
        return self.n1.eval() @ self.n2.eval()

    def grad(self, var: Node):
        if self == var:
            v = self.eval()
            return diffBySelf(v.shape)
        v = var.eval()
        n1 = self.n1.eval()
        n2 = self.n2.eval()
        d_n1 = self.n1.grad(var)
        d_n2 = self.n2.grad(var)
        p1 = matMul(d_n1, n2, 1) #len(n2.shape))
        p2 = matMul(n1, d_n2, 1) #len(n1.shape))
        return p1 + p2
    
        # d_n1 = self.n1.diff(var)
        # d_n2 = self.n2.diff(var)
        # d_n1n2_v = d_n1 @ v @ n2 + n1 @ d_n2 @ v
        # # https://www.juanklopper.com/wp-content/uploads/2015/03/III_08_Left_and_right_inverses_Pseudoinverses.html
        # v_rightInverse = v.T @ np.linalg.pinv(np.tensordot(v, v.T, 0))
        # d_n1n2 = np.tensordot(d_n1n2_v, v_rightInverse, 0)
        # return d_n1n2

    def __str__(self) -> str:
        return f"{self.n1} * {self.n2}"


class Inv(Node):
    def __init__(self, n: Node):
        self.n = n

    def id(self):
        return f"Inv({self.n.id()})"

    def eval(self):
        return np.invert(self.n.eval())

    def grad(self, var):
        """ https://math.stackexchange.com/questions/1471825/derivative-of-the-inverse-of-a-matrix """
        if self == var:
            v = self.eval()
            return diffBySelf(v.shape)
        nV = self.n.eval()
        nD = self.n.grad(var)
        nI = np.invert(nV)
        return - (nI * (nD * nI))

    def __str__(self) -> str:
        return f"({self.n})^-1"


class Exp(Node):
    def __init__(self, n: Node):
        self.n = n

    def id(self):
        return f"Exp({self.n.id()})"

    def eval(self):
        return np.exp(self.n.eval())

    def grad(self, var: Node):
        if self == var:
            v = self.eval()
            return diffBySelf(v.shape)
        nD = self.n.grad(var)
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

    def grad(self, var: Node):
        if self == var:
            v = self.eval()
            return diffBySelf(v.shape)
        u = self.u.eval()
        uD = self.u.grad(var)
        ddu_lnu = np.diag(1 / u)
        return ddu_lnu * uD

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
        return aV / bV

    def grad(self, variable: Variable):
        if self == variable:
            v = self.eval()
            return diffBySelf(v.shape)
        a = self.a.eval()
        b = self.b.eval()
        da = self.a.grad(variable)
        db = self.b.grad(variable)
        return (da * b - a * db) / b**2

    def __str__(self) -> str:
        return f"({self.a} ./ {self.b})"

        
class PwProd(Node):
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

    def grad(self, variable: Variable):
        if self == variable:
            v = self.eval()
            return diffBySelf(v.shape)
        """
            d/dx uv = (du/dx)^T v  +  (dv/dx)^T u
            d/du uv = (du/du)^T v
                    = eye * v
        """
        aVal = self.a.eval()
        bVal = self.b.eval()
        aDif = self.a.grad(variable)
        bDif = self.b.grad(variable)
        aDifT = aDif if np.isscalar(aDif) else aDif.transpose()
        bDifT = bDif if np.isscalar(bDif) else bDif.transpose()
        s = (aDifT * bVal) + (bDifT * aVal)
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

    def grad(self, variable: Variable):
        if self == variable:
            v = self.eval()
            return diffBySelf(v.shape)
        diffVal = self.node.grad(variable)
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

    def grad(self, variable: Variable):
        if self == variable:
            v = self.eval()
            return diffBySelf(v.shape)
        """
            d/dx sum(u) = [d/dx1 sum(u), d/dx2 sum(u), ...]
                        = col_sum(du/dx)
        """
        nodeDiff = self.node.grad(variable)
        return np.sum(nodeDiff, 0)

    def __str__(self) -> str:
        return f"innersum({self.node})"


class ScalarPower(Node):
    def __init__(self, a: Node, s: float):
        self.a = a
        self.s = s

    def id(self):
        return f"ScalarPower({self.a.id()}, {self.s})"

    def eval(self):
        av = self.a.eval()
        return np.power(av, self.s)

    def grad(self, x: Node):
        if self == x:
            v = self.eval()
            return diffBySelf(v.shape)
        """
            d/dx a^s = s a^(s-1) da/dx

        """
        s = self.s
        av = self.a.eval()
        apowsm1 = av**(s-1)
        da_dx = self.a.grad(x)
        return s * (apowsm1 * da_dx)

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
