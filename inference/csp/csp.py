#%%
# https://www.youtube.com/watch?v=Yo-xat4cn8M

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


def first(list, pred):
    for entry in list:
        if pred(entry):
            return entry


#%%

class Var:
    def __init__(self, name, range):
        self.name = name
        self.range = range

    def decided(self):
        return len(self.range) == 1

    def decide(self, val):
        return Var(self.name, [val])

    def __repr__(self) -> str:
        if self.decided():
            return f"Var({self.name} - {self.range[0]})"
        return f"Var({self.name} - {self.range})"


class Fac:
    def __init__(self, inputNames, func):
        self.inputNames = inputNames
        self.func = func

    def applicable(self, vars):
        for inputName in self.inputNames:
            inputVar = first(vars, lambda v: v.name == inputName)
            if not inputVar:
                return False
            if not inputVar.decided():
                return False
        return True
   
    def apply(self, vars):
        inputs = []
        for inputName in self.inputNames:
            inputVar = first(vars, lambda v: v.name == inputName)
            inputs.append(inputVar)
        return self.func(*inputs)

    def __repr__(self) -> str:
        return f"Fac({self.vars.join(', ')})"


#%%


def orderVars(vars, facs):
    # return most constrained var first
    def sortFunc(var):
        if var.decided():
            return 999999
        else:
            return len(var.range)
    vars.sort(key = sortFunc)
    return vars


def orderVals(var, vars, facs):
    # return least constraining values first
    return var.range


def updateDomain(var, vars, facs):
    # restrict domain of var
    return var


def solve(vars, facs, rating = 1):
    if all(vars, lambda var: var.decided()):
        return (rating, vars)

    for var in orderVars(vars, facs):
        for val in orderVals(var, vars, facs):

            # Step 1: new variable set with decided value
            varDecided = var.decide(val)
            otherVars = allExcept(vars, var)
            newVars = [*otherVars, varDecided]
            print(f"Trying {newVars} ...")

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

            return solve(updatedVars, facs, rating * subRating)



#%%

colors = ['R', 'G', 'B']

def differentColor(state1, state2):
    if state1.decided() and state2.decided():
        if state1.range[0] == state2.range[0]:
            return 0
    return 1

wa = Var('WA', colors)
nt = Var('NT', colors)
wa_nt = Fac(['WA', 'NT'], differentColor)
sa = Var('SA', colors)
wa_sa = Fac(['WA', 'SA'], differentColor)
nt_sa = Fac(['NT', 'SA'], differentColor)
qu = Var('QU', colors)
nt_qu = Fac(['NT', 'QU'], differentColor)
sa_qu = Fac(['SA', 'QU'], differentColor)
nw = Var('NW', colors)
qu_nw = Fac(['QU', 'NW'], differentColor)
sa_nw = Fac(['SA', 'NW'], differentColor)
vc = Var('VC', colors)
sa_vc = Fac(['SA', 'VC'], differentColor)
nw_vc = Fac(['NW', 'VC'], differentColor)
ta = Var('TA', colors)


vars = [wa, nt, sa, qu, nw, vc, ta]
facs = [wa_nt, wa_sa, nt_sa, nt_qu, sa_qu, qu_nw, sa_nw, sa_vc, nw_vc]

result = solve(vars, facs)
print(result)


# %%
