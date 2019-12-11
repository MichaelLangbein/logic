

class InferenceEngine:
    def __init__(self):
        self.facts = []
        self.rules = []

    def addFact(self, *fact):
        if fact not in self.facts:
            self.facts.append(fact)  # add the fact
            print(f"Just learned that {fact}")
        for arg in fact[1:]:
            if not self.__isVariable(arg):
                self.addFact(arg) # add all arguments

    def addRule(self, conditions, consequence):
        self.rules.append({'conditions': conditions, 'consequence': consequence})

    def eval(self, *statement) -> bool:
        if self.__findInFacts(*statement):
            return True
        return self.__tryToProve(*statement)

    def __findInFacts(self, *args) -> bool:
        for fact in self.facts:
            if fact == args:
                return True
        return False

    def __tryToProve(self, *statement) -> bool:
        candidateRules = self.__findCandidateRules(*statement)
        for candidateRule in candidateRules:
            substitutedRule = self.__setRuleVariablesByStatement(candidateRule, statement)
            if self.__allStatementsTrue(substitutedRule['conditions']):
                self.addFact(*statement)
                return True
        return False

    def __allStatementsTrue(self, statements):
        for statement in statements:
            if not self.eval(*statement):
                return False
        return True

    '''
    -----------------  helpers -------------------------
    '''

    def __setRuleVariablesByStatement(self, rule, statement):
        substitutionDict = {}
        for ruleArg, stateArg in zip(rule['consequence'][1:], statement[1:]):
            if self.__isVariable(ruleArg):
                substitutionDict[ruleArg] = stateArg
        return self.__setRuleVariablesByDict(rule, substitutionDict)

    def __setRuleVariablesByDict(self, rule, subsDict):
        newRule = {'conditions': [], 'consequence': None}
        for condition in rule['conditions']:
            newCondition = self.__setVariablesByDict(condition, subsDict)
            newRule['conditions'].append(newCondition)
        newConsequence = self.__setVariablesByDict(rule['consequence'], subsDict)
        newRule['consequence'] = newConsequence
        return newRule

    def __setVariablesByDict(self, statement, subsDict):
        newStatement = [statement[0]]
        for arg in statement[1:]:
            if self.__isVariable(arg):
                newStatement.append(subsDict[arg])
            else:
                newStatement.append(arg)
        return newStatement

    def __findCandidateRules(self, *statement):
        candidates = []
        for rule in self.rules:
            if rule['consequence'][0] == statement[0]:
                argsFittingTogether = True
                for argRule, argStatement in zip(rule['consequence'][1:], statement[1:]):
                    argsFittingTogether = argsFittingTogether and (argRule == argStatement or self.__isVariable(argRule))
                if argsFittingTogether:
                    candidates.append(rule)
        return candidates

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
    e.addFact('single', 'john')
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

    e.addRule([
        ['rating', 'X', 'beginner'],
        ['purpose', 'X', 'fun']
    ], ['advice', 'X', 'st_sartre'])

    e.addRule([
        ['rating', 'X', 'beginner'],
        ['purpose', 'X', 'serious']
    ], ['advice', 'X', 'schloss_heidegger'])

    e.addRule([
        ['rating', 'X', 'advanced'],
        ['purpose', 'X', 'fun']
    ], ['advice', 'X', 'wittgenstein'])

    e.addRule([
        ['rating', 'X', 'advanced'],
        ['purpose', 'X', 'serious']
    ], ['advice', 'X', 'chateau_derrida'])

    e.addRule([
        ['lessons', 'X', 'less_than_30']
    ], ['rating', 'X', 'beginner'])

    e.addRule([
        ['lessons', 'X', 'more_than_30'],
        ['fitness', 'X', 'poor']
    ], ['rating', 'X', 'beginner'])

    e.addRule([
        ['lessons', 'X', 'more_than_30'],
        ['fitness', 'X', 'good']
    ], ['rating', 'X', 'advanced'])

    e.addRule([
        ['pushups', 'X', 'less_than_10']
    ], ['fitness', 'X', 'poor'])

    e.addRule([
        ['pushups', 'X', 'more_than_10']
    ], ['fitness', 'X', 'good'])

    e.addFact('pushups', 'john', 'more_than_10')
    e.addFact('purpose', 'john', 'fun')
    print(e.eval('advice', 'john', 'wittgenstein'))
    print(e.eval('advice', 'john', '?'))