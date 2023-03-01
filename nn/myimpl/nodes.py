import numpy as np


class Node(np.ndarray):

    def __new__(subtype, shape,
                dtype=float,
                buffer=None,
                offset=0,
                strides=None,
                order=None):
        """
        craetes a new object that wraps an numpy.ndarray into a structure that
        represents a node in a computational graph
        """

        newobj = np.ndarray.__new__(
            subtype, shape, dtype,
            buffer, offset, strides,
            order
        )

        return newobj

    def _nodify(self, method_name, other, opname, self_first=True):
        """
        augments the operation of given arithmetic super method
        by creating and returning an OperationalNode for the operation

        Parameters:
        ----------
        method_name: String
            the name of the super method to be augmented
        other: Node | np.ndarray | Number
            the other operand to the operation
        opname: String
            the name of OperationalNode
        self_first: Boolean
            a flag indicating if self is the 1st operand in non commutative ops

        Returns: OperationalNode
        """
        if not isinstance(other, Node):
            other = ConstantNode.create_using(other)
        opvalue = getattr(np.ndarray, method_name)(self, other)

        return OperationalNode.create_using(opvalue, opname,
            self if self_first else other,
            other if self_first else self
        )


    def __add__(self, other):
        return self._nodify('__add__', other, 'add')

    def __radd__(self, other):
        return self._nodify('__radd__', other, 'add')

    def __sub__(self, other):
        return self._nodify('__sub__', other, 'sub')

    def __rsub__(self, other):
        return self._nodify('__rsub__', other, 'sub', False)

    def __mul__(self, other):
        return self._nodify('__mul__', other, 'mul')

    def __rmul__(self, other):
        return self._nodify('__rmul__', other, 'mul')

    def __div__(self, other):
        return self._nodify('__div__', other, 'div')

    def __rdiv__(self, other):
        return self._nodify('__rdiv__', other, 'div', False)

    def __truediv__(self, other):
        return self._nodify('__truediv__', other, 'div')

    def __rtruediv__(self, other):
        return self._nodify('__rtruediv__', other, 'div', False)

    def __pow__(self, other):
        return self._nodify('__pow__', other, 'pow')

    def __rpow__(self, other):
        return self._nodify('__rpow__', other, 'pow', False)

    @property
    def T(self):
        """
        augments numpy's T attribute by creating a node for the operation
        """
        opvalue = np.transpose(self)
        return OperationalNode.create_using(opvalue, 'transpose', self)


class OperationalNode(Node):

    # a static attribute to count for unnamed nodes
    nodes_counter = {}

    @staticmethod
    def create_using(opresult, opname, operand_a, operand_b=None, name=None):
        """
        craetes an graph node representing an operation

        Parameters:
        ----------
        opresult: np.ndarray
            the result of the operation
        opname: String
            the name of the operation
        operand_a: Node
            the first operand to the operation
        operand_b: Node
            the second operand to the operation if any
        name: String
            the name of the node

        Returns: OperationalNode
        """

        obj = OperationalNode(
            strides=opresult.strides,
            shape=opresult.shape,
            dtype=opresult.dtype,
            buffer=np.copy(opresult)
        )

        obj.opname = opname
        obj.operand_a = operand_a
        obj.operand_b = operand_b

        if name is not None:
            obj.name = name
        else:
            if opname not in OperationalNode.nodes_counter:
                OperationalNode.nodes_counter[opname] = 0

            node_id = OperationalNode.nodes_counter[opname]
            OperationalNode.nodes_counter[opname] += 1
            obj.name = "%s_%d" % (opname, node_id)

        return obj


class ConstantNode(Node):

     # a static attribute to count the unnamed instances
     count = 0

     @staticmethod
     def create_using(val, name=None):
        """
        creates a graph node representing a constant

        Parameters:
        ----------
        val: np.ndarray | Number
         the value of the constant
        name: String
         the node's name
        """
        if not isinstance(val, np.ndarray):
            val = np.array(val, dtype=float)

        obj = ConstantNode(
            strides=val.strides,
            shape=val.shape,
            dtype=val.dtype,
            buffer=val
        )
        if name is not None:
            obj.name = name
        else:
            obj.name = "const_%d" % (ConstantNode.count)
            ConstantNode.count += 1

        return obj


class VariableNode(Node):

     # a static attribute to count the unnamed instances
     count = 0

     @staticmethod
     def create_using(val, name=None):
        """
        creates a graph node representing a variable

        Parameters:
        ----------
        val: np.ndarray | Number
            the value of the constant
        name: String
            the node's name
        """
        if not isinstance(val, np.ndarray):
            val = np.array(val, dtype=float)

        obj = VariableNode(
            strides=val.strides,
            shape=val.shape,
            dtype=val.dtype,
            buffer=val
        )
        if name is not None:
            obj.name = name
        else:
            obj.name = "_%d" % (VariableNode.count)
            VariableNode.count += 1

        return obj





def sum(array, axis=None, keepdims=False, name=None):
    """
    defines a node in the computational graph representing a sum operation

    Parameters:
    ----------
    array: Node | ndarray | number
        the array to be summed
    axis: int
        the axis to perform the sum on
    keepdims: Boolean
        a flag to determine if the dimensions are kept
    name: String
        node's name in the graph
    """
    if not isinstance(array, Node):
        array = ConstantNode.create_using(array)
    opvalue = np.sum(array, axis=axis, keepdims=keepdims)

    return OperationalNode.create_using(opvalue, 'sum', array, name=name)

def mean(array, axis=None, name=None):
    """
    defines a node in the computational graph representing a mean operation

    Parameters:
    ----------
    array: Node | ndarray | number
        the array to be averaged
    axis: int
        the axis to perform the averaging on
    name: String
        node's name in the graph
    """
    if not isinstance(array, Node):
        array = ConstantNode.create_using(array)
    opvalue = np.mean(array, axis=axis)

    return OperationalNode.create_using(opvalue, 'mean', array, name=name)

def exp(array, name=None):
    """
    defines a node in the computational graph representing an exp operation

    Parameters:
    ----------
    array: Node | ndarray | number
        the array to be exp-ed
    name: String
        node's name in the graph
    """
    if not isinstance(array, Node):
        array = ConstantNode.create_using(array)
    opvalue = np.exp(array)

    return OperationalNode.create_using(opvalue, 'exp', array, name=name)

def log(array, name=None):
    """
    defines a node in the computational graph representing an log operation

    Parameters:
    ----------
    array: Node | ndarray | number
        the array to be log-ed
    name: String
        node's name in the graph
    """
    if not isinstance(array, Node):
        array = ConstantNode.create_using(array)
    opvalue = np.log(array)

    return OperationalNode.create_using(opvalue, 'log', array, name=name)

def max(array, axis=None, keepdims=False, name=None):
    """
    defines a node in the computational graph representing a max operation

    Parameters:
    ----------
    array: Node | ndarray | number
        the array to be maxed out
    axis: int
        the axis to perform the max out on
    keepdims: Boolean
        a flag to determine if the dimensions are kept
    name: String
        node's name in the graph
    """
    if not isinstance(array, Node):
        array = ConstantNode.create_using(array)
    opvalue = np.max(array, axis=axis, keepdims=keepdims)
    opnode = OperationalNode.create_using(opvalue, 'max', array, name=name)

    # save info for gradient computation
    opnode.axis = axis
    opnode.keepdims = keepdims
    opnode.with_keepdims = np.max(array, axis=axis, keepdims=True)

    return opnode


def where(condition, array_a, array_b, name=None):
    """
    defines a node in the computational graph representing a where selection
    operation

    Parameters:
    ----------
    condition: ndarray of Boolean
        the selection condition
    array_a: Node | ndarray | number
        the value to select from when the condition is True
    array_b: Node | ndarray | number
        the value to select from when the condition is False
    name: String
        the name of the node
    """
    if not isinstance(array_a, Node):
        nd_array_a = np.full_like(condition, array_a)
        array_a = ConstantNode.create_using(nd_array_a)
    if not isinstance(array_b, Node):
        nd_array_b = np.full_like(condition, array_b)
        array_b = ConstantNode.create_using(nd_array_b)
    opvalue = np.where(condition, array_a, array_b)
    opnode = OperationalNode.create_using(opvalue, 'where', array_a, array_b, name=name)
    opnode.condition = condition  # save condition for gradient computation

    return opnode

def sin(array, name=None):
    """
    defines a node in the computational graph representing a sin operation

    Parameters:
    ----------
    array: Node | ndarray | number
        the array to be sin-ed
    name: String
        node's name in the graph
    """
    if not isinstance(array, Node):
        array = ConstantNode.create_using(array)
    opvalue = np.sin(array)

    return OperationalNode.create_using(opvalue, 'sin', array, name=name)

def cos(array, name=None):
    """
    defines a node in the computational graph representing a cos operation

    Parameters:
    ----------
    array: Node | ndarray | number
        the array to be sin-ed
    name: String
        node's name in the graph
    """
    if not isinstance(array, Node):
        array = ConstantNode.create_using(array)
    opvalue = np.cos(array)

    return OperationalNode.create_using(opvalue, 'cos', array, name=name)

def softmax_cross_entropy(logits, labels, name=None):
    """
    defines a softmax-cross-entropy op as a primitive for numerical stability

    Parameters:
    ----------
    logits: Node| ndarray| Number
        the model's prediction
    labels:
        the true labels
    name: String
        node's name in the graph
    """
    if not isinstance(logits, Node):
        logits = ConstantNode.create_using(logits)
    if not isinstance(labels, Node):
        labels = ConstantNode.create_using(labels)

    logits_max = np.max(logits, axis=1, keepdims=True)
    exp_op = np.exp(logits - logits_max)
    logits_softmax = exp_op / np.sum(exp_op, axis=1, keepdims=True)

    cross_entropy = -1 * np.mean(labels * np.log(logits_softmax + 1e-7))

    opnode = OperationalNode.create_using(
        cross_entropy,
        'softmax_cross_entropy',
        logits,
        name=name
    )

    # save info for gradient calculations
    opnode.softmax_val = logits_softmax
    opnode.labels = labels

    return opnode

def reshape(array, new_shape, name=None):
    """
    defines a node in the computational graph representing a reshape operation

    Parameters:
    ----------
    array: Node| ndarray
        the array to be reshaped
    new_shape: iterable
        the new shape to put the array in
    name: String
        node's name in the graph
    """
    if not isinstance(array, Node):
        array = ConstantNode.create_using(array)
    opvalue = np.reshape(array, new_shape)

    return OperationalNode.create_using(opvalue, 'reshape', array, name=name)

def squeeze(array, axis=None, name=None):
    """
    defines a node in the computational graph representing a squeeze operation

    Parameters:
    ----------
    array: Node| ndarray
        the array to be squeezed
    axis: iterable
        the 1 axes to be squeezed out of the array
    name: String
        node's name in the graph
    """
    if not isinstance(array, Node):
        array = ConstantNode.create_using(array)
    opvalue = np.squeeze(array, axis=axis)

    return OperationalNode.create_using(opvalue, 'squeeze', array, name=name)

def reset():
    """ resets the count for all node types
    """
    OperationalNode.nodes_counter = {}
    ConstantNode.count = 0
    VariableNode.count = 0



def add_grad(prev_adjoint, node):
    return [prev_adjoint, prev_adjoint]

def sub_grad(prev_adjoint, node):
    return [prev_adjoint, -1 * prev_adjoint]

def mul_grad(prev_adjoint, node):
    return [
        prev_adjoint * node.operand_b,
        prev_adjoint * node.operand_a
    ]

def div_grad(prev_adjoint, node):
    return [
        prev_adjoint / node.operand_b,
        -1 * prev_adjoint * node.operand_a / node.operand_b ** 2
    ]

def pow_grad(prev_adjoint, node):
    return [
        prev_adjoint * node.operand_b * (node.operand_a ** (node.operand_b - 1)),
        prev_adjoint * node * cg.log(node.operand_a)
    ]

def transpose_grad(prev_adjoint, node):
    return [prev_adjoint.T, None]

def sum_grad(prev_adjoint, node):
    return [prev_adjoint * np.ones_like(node.operand_a), None]

def mean_grad(prev_adjoint, node):
    return [prev_adjoint * node * np.ones_like(node.operand_a), None]

def exp_grad(prev_adjoint, node):
    return [prev_adjoint * node, None]

def log_grad(prev_adjoint, node):
    return [prev_adjoint * (1. / node.operand_a), None]

def max_grad(prev_adjoint, node):
    doperand_a = cg.where(node.operand_a == node.with_keepdims, 1, 0)
    normalizers = cg.sum(doperand_a, axis=node.axis, keepdims=True)
    normalized_doperand_a = doperand_a / normalizers

    return [prev_adjoint * normalized_doperand_a, None]

class Node:
    def __init__(self, opresult, operand_a, operand_b=Null, name=None):
        self.opresult = opresult
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.name = name

class ConstantNode(Node):
    pass

class Dot(Node):
    def __init__(self, array_a, array_b, name=None):
        """
        defines a node in the computational graph representing an array product op

        Parameters:
        ----------
        array_a: Node | ndarray | number
            the first operand to the product
        array_b: Node | ndarray | number
            the second operand to the product
        name: String
            the name of the node
        """
        if not isinstance(array_a, Node):
            array_a = ConstantNode.create_using(array_a)
        if not isinstance(array_b, Node):
            array_b = ConstantNode.create_using(array_b)
        opvalue = np.dot(array_a, array_b)

        super().__init__(opvalue, array_a, array_b, name)

    def grad(self, prev_adjoint, node):
        prev_adj = prev_adjoint
        op_a = node.operand_a
        op_b = node.operand_b

        if prev_adjoint.ndim == 1:
            prev_adj = cg.reshape(prev_adjoint, (1, -1))
        
        if node.operand_b.ndim == 1:
            op_b = cg.reshape(op_b, (-1, 1))

        if node.operand_a.ndim == 1:
            op_a = cg.reshape(op_a, (1, -1))

        return [
            Dot(prev_adj, op_b.T),
            Dot(op_a.T, prev_adj)
        ]

def where_grad(prev_adjoint, node):
    doperand_a = np.zeros_like(node.operand_a)
    doperand_b = np.ones_like(node.operand_b)

    doperand_a[node.condition] = 1
    doperand_b[node.condition] = 0

    return [prev_adjoint * doperand_a, prev_adjoint * doperand_b]

def sin_grad(prev_adjoint, node):
    return [prev_adjoint * cg.cos(node.operand_a), None]

def cos_grad(prev_adjoint, node):
    return [-1 * prev_adjoint * cg.sin(node.operand_a), None]

def softmax_cross_entropy_grad(prev_adjoint, node):
    return [
        prev_adjoint * (node.softmax_val - node.labels),
        None
    ]

def reshape_grad(prev_adjoint, node):
    return [
        cg.reshape(prev_adjoint, node.operand_a.shape),
        None
    ]

def squeeze_grad(prev_adjoint, node):
    return [
        cg.reshape(prev_adjoint, node.operand_a.shape),
        None
    ]

def unbroadcast_adjoint(node, adjoint):
    """
    puts the adjoint into the correct shape by summing over all the
    brodacsted dimensions. The underlying principle is notthing but
    the multi chain rule.

    Parameters:
    ----------
    node: Node
        the node to check if its adjoint is broadcasted
    adjoint: ndarray
        the the adjoint of the node that might need fixing
    """
    correct_adjoint = adjoint

    if node.shape != adjoint.shape:
        dimensions_diff = np.abs(adjoint.ndim - node.ndim)
        if dimensions_diff != 0:
            summation_dims = tuple(range(dimensions_diff))
            correct_adjoint = cg.sum(adjoint, axis=summation_dims)

            originally_ones = tuple([axis  for axis, size in enumerate(node.shape) if size == 1])
            if len(originally_ones) != 0:
                correct_adjoint = cg.sum(correct_adjoint, axis=axis, keepdims=True)

    return correct_adjoint




def gradient(node):
    """
    computes and returns the gradient of the given node wrt to VariableNodes
    the function implements a breadth-first-search (BFS) to traverse the
    computational graph from the gievn node back to VariableNodes

    Parameters:
    ----------
    node: Node
        the node to compute its gradient
    """

    adjoint = defaultdict(int)
    grad = {}
    queue = NodesQueue()

    # put the given node in the queue and set its adjoint to one
    adjoint[node.name] = ConstantNode.create_using(np.ones(node.shape))
    queue.push(node)

    while len(queue) > 0:
        current_node = queue.pop()

        if isinstance(current_node, ConstantNode):
            continue
        if isinstance(current_node, VariableNode):
            grad[current_node.name] = adjoint[current_node.name]
            continue

        current_adjoint = adjoint[current_node.name]
        current_op = current_node.opname

        op_grad = getattr(grads, '{}_grad'.format(current_op))
        next_adjoints = op_grad(current_adjoint, current_node)

        adjoint[current_node.operand_a.name] = grads.unbroadcast_adjoint(
            current_node.operand_a,
            adjoint[current_node.operand_a.name] + next_adjoints[0]
        )
        if current_node.operand_a not in queue:
            queue.push(current_node.operand_a)

        if current_node.operand_b is not None:
            adjoint[current_node.operand_b.name] = grads.unbroadcast_adjoint(
                current_node.operand_b,
                adjoint[current_node.operand_b.name] + next_adjoints[1]
            )
            if current_node.operand_b not in queue:
                queue.push(current_node.operand_b)

    return grad


def check_gradient(fx, args, suspect):
    """
    checks the correctness of the suspect derivative value against
    the value of the numerical approximation of the derivative

    Parameters:
    ----------
    fx: callable
        The function to check its derivative
    wrt: int
        0-based index of the variable to differntiate with respect to
    args: list
        the values of the function variables at the derivative point
    suspect: float
        the the suspected value of the derivative to check
    """
    h = 1.e-7
    approx_grad = []

    for i in range(len(args)):
        shifted_args = args[:]
        shifted_args[i] = shifted_args[i] + h
        approx_grad.append((fx(*shifted_args) - fx(*args)) / h)

    return np.allclose(approx_grad, suspect)
