from ie.base import Rule, Variable


def tolist(something):
    try:
        return list(something)
    except:
        return [something]


def listUnion(list1, list2):
    if list1 is None:
        return list2
    if list2 is None:
        return list1
    uList = list1
    for entry in list2:
        if entry not in list1:
            uList.append(entry)
    return uList


def listIntersection(list1, list2):
    if list1 is None:
        return list2
    if list2 is None:
        return list1
    iList = []
    for entry in list1:
        if entry in list2:
            iList.append(entry)
    return iList


def dictUnion(dict1, dict2):
    if dict1 is None:
        return dict2
    if dict2 is None:
        return dict1
    uDict = {}
    keys = listUnion(tolist(dict1.keys()), tolist(dict2.keys()))
    for key in keys:
        d1v = d2v = None
        if key in dict1:
            d1v = tolist(dict1[key])
        if key in dict2:
            d2v = tolist(dict2[key])
        uDict[key] = listUnion(d1v, d2v)
    return uDict


def dictIntersection(dict1, dict2):
    if dict1 is None:
        return dict2
    if dict2 is None:
        return dict1
    iDict = {}
    keys = listUnion(tolist(dict1.keys()), tolist(dict2.keys()))
    for key in keys:
        d1v = d2v = None
        if key in dict1:
            d1v = tolist(dict1[key])
        if key in dict2:
            d2v = tolist(dict2[key])
        iDict[key] = listIntersection(d1v, d2v)
    return iDict


def dictUnionListIntersection(dict1, dict2):
    if dict1 is None:
        return dict2
    if dict2 is None:
        return dict1
    uDict = {}
    keys = listUnion(tolist(dict1.keys()), tolist(dict2.keys()))
    for key in keys:
        d1v = d2v = None
        if key in dict1:
            d1v = tolist(dict1[key])
        if key in dict2:
            d2v = tolist(dict2[key])
        uDict[key] = listIntersection(d1v, d2v)
    return uDict


def matchExpressions(expr1, expr2):
    if len(expr1) != len(expr2):
        return False
    for w1, w2 in zip(expr1, expr2):
        if not isinstance(w1, Variable) and not isinstance(w2, Variable):
            if w1 != w2:
                return False
        if isinstance(w1, Variable) and not isinstance(w2, Variable):
            if not isinstance(w2, w1.cls):
                return False
        if isinstance(w2, Variable) and not isinstance(w1, Variable):
            if not isinstance(w1, w2.cls):
                return False
    return True


def backwardSubstituteRule(rule: Rule, *consequence):
    translationDict = getTranslationDict(rule.consequence, consequence)
    newCondition = substituteExpressionWithDict(rule.condition, translationDict)
    return Rule(tuple(newCondition), consequence)


def forwardSubstituteRule(rule: Rule, *condition):
    translationDict = getTranslationDict(rule.condition, condition)
    newConsequence = substituteExpressionWithDict(rule.consequence, translationDict)
    return Rule(condition, tuple(newConsequence))


def substituteExpressionWithDict(expression, translationDict):
    substituted = []
    for subexpression in expression:
        if isinstance(subexpression, tuple):
            substituted.append( substituteExpressionWithDict(subexpression, translationDict) )
        elif isinstance(subexpression, Variable) and subexpression in translationDict:
            substituted.append( translationDict[subexpression] )
        else:
            substituted.append( subexpression )
    return tuple(substituted)


def getTranslationDict(variableExpression, substitutedExpression):
    translationDict = {}
    for rw, ew in zip(variableExpression, substitutedExpression):
        if isinstance(rw, tuple):
            translationDict.update( getTranslationDict(rw, ew) )
        elif isinstance(rw, Variable):
            translationDict[rw] = ew
    return translationDict


def dictValMap(d, func):
    for key in d:
        d[key] = func(d[key])
    return d


class Root:
    def __init__(self, leaves):
        self.leaves = leaves


class Node:
    def __init__(self, key, val, leaves):
        self.key = key
        self.val = val
        self.leaves = leaves


def createSubstitutionTree(d: dict):
    leaves = createLeaves(d)
    root = Root(leaves)
    return root


def createLeaves(d):
    key, vals, rest = dictPop(d)
    leaves = [Node(key, val, []) for val in vals]
    if rest:
        for leave in leaves:
            leave.leaves = createLeaves(rest)
    return leaves        


def dictPop(d):
    newDict = dict(d)
    key = list(newDict.keys())[0]
    val = newDict.pop(key)
    return key, val, newDict


def getAllPaths(root: Root):
    paths = []
    for leave in root.leaves:
        paths += getLeavePaths(leave)
    return paths


def getLeavePaths(node: Node):
    step = {node.key: node.val}
    subpaths = []
    for leave in node.leaves:
        subpaths += getLeavePaths(leave)
    if subpaths:
        for subpath in subpaths:
            subpath.update(step)
        return subpaths
    else:
        return [step]
