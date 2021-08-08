from inference.kanren.main import Var, Goal, Relation, Subst, SubstStream, falseSubst, walk, walkx, eqR



def carR(lst, head):
    body = Var('body')
    return eqR([head, body], lst)


def cdrR(lst, body):
    head = Var('head')
    return eqR([head, body], lst)


def consR(head, body, lst) -> Goal:
    return eqR([head, body], lst)





