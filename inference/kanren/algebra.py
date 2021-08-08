from inference.kanren.main import Var, isVar, Subst, Goal, Relation


def addR(a, b, s) -> Goal:
    def addG(subst: Subst) -> SubstStream:
        if isVar(a):
            yield a
        if isVar(b):
            yield b
    return addG