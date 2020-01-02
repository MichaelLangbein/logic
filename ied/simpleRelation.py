from ied.base import TestableRelation
from ied.engine import InferenceEngine
from ied.substitution import substituteExpression, matchRightToLeft



class Root:
    def __init__(self, leaves):
        self.leaves = leaves
    def  __repr__(self):
        return 'root'

class Node:
    def __init__(self, val, leaves):
        self.val = val
        self.leaves = leaves
    def __repr__(self):
        return self.val


def createSubstitutionTree(d: list):
    leaves = createLeaves(d)
    root = Root(leaves)
    return root


def createLeaves(d):
    vals, rest = listPop(d)
    leaves = [Node(val, []) for val in vals]
    if rest:
        for leave in leaves:
            leave.leaves = createLeaves(rest)
    return leaves        


def listPop(l):
    newList = list(l)
    val = newList.pop()
    return val, newList


def getAllPaths(root: Root):
    paths = []
    for leave in root.leaves:
        paths += getLeavePaths(leave)
    return paths


def getLeavePaths(node: Node):
    subpaths = []
    for leave in node.leaves:
        subpaths += getLeavePaths(leave)
    if subpaths:
        subpaths = [tuple(list(subpath) + list(node.val)) for subpath in subpaths]
        return subpaths
    else:
        return [node.val]



def evalAll(ie: InferenceEngine, *args):
    argLists = []
    for arg in args:
        if not isinstance(arg, tuple): arg = (arg,)
        substArgs = ie.evalAndSubstituteExpression(*arg)
        if not substArgs:
            return False
        argLists.append(substArgs)
    
    root = createSubstitutionTree(argLists)
    allCombs = getAllPaths(root)

    return allCombs


class SimpleTestableRelation(TestableRelation):
    """
        Contrary to ``TestableRelation``s, a ``SimpleTestableRelation`` gives to the ``relationTestFunction`` only fully evaluated and substituted arguments.
        This way, the user does not need to evaluate any subexpressions. Also, the user only needs to return ``True`` or ``False`` instead of a TruthSet.
        However, this can have a performance impact: in a ``TestableRelation`` like ``And``, we don't need to evaluate all subexpressions if the first one already turns out to be false.
    """

    def __init__(self, description, relationTestFunction):
        super().__init__(description, relationTestFunction)

    def testRelation(self, ie, *args):
        combinations = evalAll(ie, *args)
        if not combinations:
            return []

        trueTDicts = []
        for combination in combinations:
            if self.relationTestFunction(*combination):
                tDict = matchRightToLeft(combination, args)
                trueTDicts.append(tDict)

        return trueTDicts