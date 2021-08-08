from math import inf
from typing import Iterator, Callable, Any, List, Union





class Var:
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        return isinstance(other, Var) and other.name == self.name
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name
    def __hash__(self):
        return hash(self.name)


falseSubst = None

Subst = Union[dict, falseSubst]

SubstStream = Iterator[Subst]

# A goal is a reified relation - the relation's parameters & variables are set, now the goal can be used to stream substitutions through.
Goal = Callable[[Subst], SubstStream]

# A relation is a function of arguments, of which some or all may be variables
Relation = Callable[[List[Any]], Goal]


def isVar(x):
    return isinstance(x, Var)


def emptyStream() -> SubstStream:
    yield {}


def walk(var: Var, subst: Subst) -> Any:
    if var in subst:
        val = subst[var]
        if isVar(val):
            return walk(val, subst)
        else:
            return val
    else:
        return var


def walkx(x: Any, subst: Subst) -> Any:
    if isVar(x):
        return walk(x, subst)
    else:
        return x


def reify(var: Var, subst: Subst) -> Subst:
    if subst == falseSubst:
        return subst
    if not var in subst:
        return subst
    val = subst[var]
    if isVar(val):
        val = walk(val, subst)
        if not isVar(val):
            subst[var] = val
    return subst


def serial(subst: Subst, *goals: List[Goal]) -> SubstStream:
    firstGoal = goals[0]
    restGoals = goals[1:]
    stream = firstGoal(subst)
    for s in stream:
        if s == falseSubst:
            yield s
        if restGoals:
            sstream = serial(s, *restGoals)
            for ss in sstream:
                yield ss
        else:
            yield s


def parallel(subst: Subst, *goals: List[Goal]) -> SubstStream:
    for goal in goals:
        stream = goal(subst)
        for s in stream:
            yield s


def andR(*goals: List[Goal]) -> Goal:
    def andG(subst: Subst) -> SubstStream:
        stream = serial(subst, *goals)
        for s in stream:
            yield s
    return andG


def orR(*goals: List[Goal]) -> Goal:
    def orG(subst: Subst) -> SubstStream:
        stream = parallel(subst, *goals)
        for s in stream:
            yield s
    return orG


def eqR(a, b) -> Goal:
    def eqG(subst: Subst) -> SubstStream:
        a = walkx(a, subst)
        b = walkx(b, subst)
        if (a == b):
            yield subst
        elif isVar(a):
            subst[a] = b
            yield subst
        elif isVar(b):
            subst[b] = a
            yield subst
        elif isinstance(a, list) and isinstance(b, list):
            subGoals = [eqR(sa, sb) for sa, sb in zip(a, b)]
            for s in serial(subst, *subGoals):
                yield s
        else:
            yield falseSubst
    return eqG


def evalGoal(goal: Goal, targetVars: List[Var], subst: Subst):
    stream = goal(subst)
    for s in stream:
        if s == falseSubst:
            yield falseSubst
        else:
            for v in targetVars:
                s = reify(v, s)
            slimS = {}
            for v in targetVars:
                if v in s:
                    slimS[v] = s[v]
            yield slimS


def take(n, stream):
    out = []
    i = -1
    for s in stream:
        if s is not falseSubst:
            out.append(s)
        i += 1
        if i >= n:
            break
    return out


def runN(n, vars: List[Var], goal: Goal):
    subsStr = evalGoal(goal, vars, {})
    return take(n, subsStr)


def run(vars: List[Var], goal: Goal):
    return runN(inf, vars, goal)