
class Object:
    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return self.description


class Relation(Object):
    def __init__(self, description):
        super(Relation, self).__init__(description)



class Variable:
    def __init__(self, description, cls=Object):
        self.description = description
        self.cls = cls

    def __repr__(self):
        return self.description


class Rule:
    def __init__(self, condition, consequence):
        self.condition = condition
        self.consequence = consequence

    def __repr__(self):
        return f"if {self.condition} => {self.consequence}"


def getVariables(query):
    vrbls = []
    isSingleWord = False if isinstance(query, tuple) else True
    if isSingleWord:
        query = (query,)
    for word in query:
        if isinstance(word, Variable):
            vrbls.append(word)
        elif isinstance(word, tuple):
            subVrbls = getVariables(word)
            vrbls += subVrbls
    return vrbls


def substitute(query, tDict):
    # sanity check
    variablesInQuery = getVariables(query)
    newVrblValuesInDict = getVariables(tDict.values())
    for v in variablesInQuery:
        if v in newVrblValuesInDict:
            raise Exception(f"The phrase {query} already has a variable named '{v}'. Please rename this variable.")

    substituted = []
    for word in query:
        if isinstance(word, Variable):
            if word in tDict:
                substituted.append(tDict[word])
            else:
                substituted.append(word)
        elif isinstance(word, tuple):
            subSubstituted = substitute(word, tDict)
            substituted.append(subSubstituted)
        else:
            substituted.append(word)
    return tuple(substituted)


def matches(vQuery, fact):
    if len(vQuery) != len(fact):
        return False
    tDict = {}
    for vw, fw in zip(vQuery, fact):
        if isinstance(vw, Variable):
            tDict[vw] = fw
        elif vw != fw:
            return False
    return tDict


class InferenceEngine:
    def __init__(self):
        self.facts = []
        self.rules = []
        self.learned = []

    def addFact(self, *fact):
        if fact not in self.facts:
            self.facts.append(fact)

    def addRule(self, condition, consequence):
        rule = Rule(condition, consequence)
        if rule not in self.rules:
            self.rules.append(rule)
    
    def addLearned(self, *query):
        if len(getVariables(query)) == 0:
            if query not in self.learned:
                self.learned.append(query)

    def matchInFacts(self, *query):
        for fact in self.facts + self.learned:
            tDict = matches(query, fact)
            if tDict is not False:
                yield tDict

    def matchInRules(self, *query):
        if query not in self.learned:
            for rule in self.rules:
                tDict = matches(rule.consequence, query)
                if tDict:
                    substRule = Rule(substitute(rule.condition, tDict), query)
                    self.addLearned(query)
                    yield substRule

    def eval(self, *query):
        print(f"now evaluating: {query}")
        operator = query[0]
        operands = query[1:]
        if operator in ['and', 'or', 'calc', 'unequal', 'not']:  # special forms
            if operator == 'and':
                for tDict in self.And(*operands):
                    yield tDict
            elif operator == 'or':
                for tDict in self.Or(*operands):
                    yield tDict
            elif operator == 'calc':
                function = operands[0]
                args = operands[1:]
                for tDict in function(args):
                    yield tDict
            elif operator == 'not':
                for tDict in self.Not(*operands):
                    yield tDict
            elif operator == 'unequal':
                if operands[0] != operands[1]:
                    yield {}
        else:
            for tDict in self.matchInFacts(*query):
                yield tDict
            for rule in self.matchInRules(*query):
                for tDict in self.eval(*(rule.condition)):
                    yield tDict

    def evalAndSubstitute(self, *query):
        for tDict in self.eval(*query):
            yield substitute(query, tDict)

    def __repr__(self):
        return 'IE'

    def And(self, firstArg, *restArgs):
        """
            The first conjunct creates a stream of tDicts.
            Every subsequent conjunct filters that stream.
            Cancels early when the sream has become empty.
        """
        for tDict in self.eval(*firstArg):
            if len(restArgs) == 0:
                yield tDict
            else:
                restArgs = [substitute(arg, tDict) for arg in restArgs]
                for subTDict in self.And(*restArgs):
                    tDict.update(subTDict)
                    yield tDict
            
    def Or(self, *args):
        yield

    def Not(self, *args):
        yield

    def allCombinations(self, listOfGenerators):
        firstGen = listOfGenerators[0]
        restGen = listOfGenerators[1:]
        if len(restGen) == 0:
            for result in firstGen:
                yield [result]
        else:
            for result in firstGen:
                for subresults in self.allCombinations(restGen):  # TODO: performance? 'self.allCombinations' is called repeatedly!
                    yield [result] + subresults


