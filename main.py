from typing import Union


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
        newRule = {'conditions': conditions, 'consequence': consequence}
        if not newRule in self.rules:
            self.rules.append(newRule)
            print(f"Just learned that {newRule}")

    def eval(self, *statement):
        print(f"Evaluating whether '{statement}' holds true")
        fact = self.__searchFacts(*statement)
        if fact: 
            return fact
        fact = self.__tryToProve(*statement)
        if fact:
            return fact
        return False

    def __searchFacts(self, *statement):
        for fact in self.facts:
            if self.__statementsEquivalentExceptVariables(fact, statement):
                return fact
        return False

    def __tryToProve(self, *statement):
        candidateRules = self.__findCandidateRules(*statement)
        for candidateRule in candidateRules:
            substitutedRule = self.__setRuleVariablesByStatement(candidateRule, statement)
            if self.__allStatementsTrue(substitutedRule['conditions']):
                substitutedStatement = substitutedRule['consequence']
                self.addFact(*substitutedStatement)
                return substitutedStatement
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
            if self.__isVariable(arg) and arg in subsDict:
                newStatement.append(subsDict[arg])
            else:
                newStatement.append(arg)
        return newStatement

    def __findCandidateRules(self, *statement):
        candidates = []
        for rule in self.rules:
            if self.__statementsEquivalentExceptVariables(rule['consequence'], statement):
                candidates.append(rule)
        return candidates

    def __statementsEquivalentExceptVariables(self, statementOne, statementTwo):
        for wordOne, wordTwo in zip(statementOne, statementTwo):
            oneIsVar = self.__isVariable(wordOne)
            twoIsVar = self.__isVariable(wordTwo)
            if (oneIsVar and twoIsVar) or (not oneIsVar and not twoIsVar):
                if wordOne != wordTwo:
                    return False
        return True

    def __isVariable(self, arg):
        return isinstance(arg, str) and arg[0].isupper()





if __name__ == '__main__':
    e = InferenceEngine() 

    # Test 3: variable in condition
    e.addRule([
        ['coffee']
    ], ['happy', 'jane'])
    e.addFact('coffee')
    print(e.eval('happy', 'X'))

    # TODO: do inference with X not an atom, but itself a statement
