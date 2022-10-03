#%%

def all(list, predicate):
    for entry in list:
        if not predicate(entry):
            return False
    return True

def allExcept(list, entry):
    out = []
    for e in list:
        if e != entry:
            out.append(e)
    return out

def listWithNew(list, pred, newEntry):
    newList = []
    for entry in list:
        if pred(entry):
            newList.append(newEntry)
        else:
            newList.append(entry)
    return newList


#%%

class Var:
    def __init__(self, name, range):
        self.name = name
        self.range = range

    def decided(self):
        return self.range.length == 1

    def decide(self, val):
        return Var(self.name, [val])


class Fac:
    def __init__(self, func):
        self.func = func

    def applicable(self, vars):
        pass

    def apply(self, vars):
        return self.func(vars)


def orderVars(vars, facs):
    # return most constrained var first
    return vars


def orderVals(var, vars, facs):
    # return least constraining values first
    return var.domain


def updateDomain(var, vars, facs):
    # restrict domain of var
    return var


def solve(vars, facs, rating = 1):
    if all(vars, lambda var: var.decided()):
        yield (rating, vars)

    for var in orderVars(vars, facs):
        for val in orderVals(var, vars, facs):

            # Step 1: new variable set with decided value
            varDecided = var.decide(val)
            otherVars = allExcept(vars, var)
            newVars = otherVars.append(varDecided)

            # Step 2: evaluate set. If inconsistent, stop here
            subRating = 1
            for fac in facs:
                if fac.applicable(newVars):
                    subRating *= fac.apply(newVars)
            if subRating == 0:
                continue

            # Step 3: adjust domains of other variables through lookahead
            # This step is optional because if we don't do it, inconsistent values
            # will be filtered out in the next recursion ...
            # ... but here we have a chance to do something smart
            # that removes multiple values at once.
            updatedVars = [
                updateDomain(var, newVars, facs)
                for var in newVars
            ]

            solve(updatedVars, facs, rating * subRating)



#%%
