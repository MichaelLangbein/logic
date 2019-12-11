

class InferenceEngine:
    def __init__(self):
        self.facts = []
        self.rules = []

    def addFact(self, *fact):
        self.facts.append(fact)  # add the fact
        for arg in fact[1:]:
            if not self.__isVariable(arg):
                self.addFact(arg) # add all arguments

    def addRule(self, conditions, consequence):
        self.rules.append({'conditions': conditions, 'consequence': consequence})

    def eval(self, *args) -> bool:
        alreadyKnown = self.__findInFacts(*args)
        if alreadyKnown:
            return True
        return self.__tryToProve(*args)

    def evalRuleWith(self, rule, variableDictionary) -> list:
        for condition in rule['conditions']:
            statementWithVals = self.__replaceVarsWithVals(condition, variableDictionary)
            statementTrue = self.eval(*statementWithVals)
            if not statementTrue:
                return []
        return self.__replaceVarsWithVals(rule['consequence'], variableDictionary)

    def __replaceVarsWithVals(self, statement, variableDict):
        substitutedStatement = []
        substitutedStatement.append(statement[0])
        for arg in statement[1:]:
            if self.__isVariable(arg):
                substitutedStatement.append(variableDict[arg])
            else:
                substitutedStatement.append(arg)
        return tuple(substitutedStatement)

    def __findInFacts(self, *args) -> bool:
        for fact in self.facts:
            if fact == args:
                return True
        return False

    def __tryToProve(self, *statement) -> bool:
        for rule in self.rules:
            if statement[0] == rule['consequence'][0]:
                argNames = rule['consequence'][1:]
                argDict = dict(zip(argNames, statement[1:]))
                newFact = self.evalRuleWith(rule, argDict)
                self.addFact(*newFact)
                if newFact == statement:
                    return True
        return False

    def __isVariable(self, arg):
        return isinstance(arg, str) and arg[0].isupper()





if __name__ == '__main__':
    e = InferenceEngine() 
    
    # Test 1: testing variable substitution
    e.addRule([
        ['famous', 'X'],
        ['single', 'john']
    ],
    ['loves', 'john', 'X'])
    e.addFact('famous', 'brad pitt')
    print(e.eval('loves', 'john', 'brad pitt'))


    # Test 2: testing deep chaining
    e.addRule([
        ['coffee']
    ], ['happy', 'jane'])
    e.addRule([
        ['happy', 'jane']
    ], ['happy', 'michael'])
    e.addFact('coffee')
    print(e.eval('happy', 'michael'))

    # TODO: do inference with X not an atom, but itself a statement