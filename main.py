

class InferenceEngine:
    def __init__(self):
        self.facts = []
        self.rules = []

    def addFact(self, *args):
        self.facts.append(args)

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
            if arg[0].islower():
                substitutedStatement.append(arg)
            else:
                substitutedStatement.append(variableDict[arg])
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





if __name__ == '__main__':
    e = InferenceEngine() 
    e.addFact('john')
    print(e.eval('john'))

    e.addFact('likes', 'jane', 'john')
    print(e.eval('likes', 'jane', 'john'))

    e.addFact('likes', 'john', 'jane')
    e.addRule([
        ['likes', 'X', 'Y'], 
        ['likes', 'Y', 'X']
    ],
    ['couple', 'X', 'Y']
    )
    print(e.eval('couple', 'jane', 'john'))

    e.addFact('coffee')
    e.addRule([
        ['coffee']
    ],
    ['happy', 'jane']
    )
    print(e.eval('happy', 'jane'))


    e.addRule([
        ['famous', 'X'],
        ['single', 'john']
    ],
    ['loves', 'john' 'X'])
    e.addFact('famous', 'Brad Pitt')
    print(e.eval('loves', 'john', 'Brad Pitt'))
