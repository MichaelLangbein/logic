from math import inf
from typing import Iterator, Callable, Any, List

"""
  Variables:
   - a variable is *fresh* when it has no association.
  
  Substitutions:
   - a substitution is a frame: [{x: 1, y: 'v', z: x}]
  
  Goals: (functions ending in 'G')
   - a goal is a function nameG: subs -> subs[] 
     That is a function that maps one substitution to a stream of zero or more substitutions.
  
  Relations: (functions ending in 'o')
   - a relation is a function that takes 0 or more variables and returns a goal:
"""

class Var:
    def __init__(self, name):
        self.name = name

Subst = dict

SubstStream = Iterator[dict]

Goal = Callable[[Subst], SubstStream]

Relation = Callable[[List[Any]], Goal]


def emptyStream() -> SubstStream:
    yield {}



def evalGoals(subst: Subst, goals: List[Goal]) -> SubstStream:
    firstGoal = goals[0]
    restGoals = goals[1:]
    stream = firstGoal(subst)
    for s in stream:
        if restGoals:
            sstream = evalGoals(s, restGoals)
            for ss in sstream:
                yield ss
        else:
            yield s


def andR(goals: List[Goal]) -> Goal:
    def g(subst: Subst) -> SubstStream:
        stream = evalGoals(subst, *goals)
        for s in stream:
            yield s
    return g


def orR(goals: List[Goal]) -> Goal:
    pass


def eqR(termA, termB) -> Goal:
    pass


def evalGoal(goal: Goal, subst: Subst):
    stream = goal(subst)
    for s in stream:
        yield s


def take(n, stream):
    out = []
    i = -1
    for s in stream:
        out.append(s)
        i += 1
        if i >= n:
            break
    return out


def runN(n, goal: Goal):
    subsStr = evalGoal(goal, {})
    return take(n, subsStr)


def run(goal: Goal):
    return runN(inf, goal)