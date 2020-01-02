from ie.base import Fact, Object, Relation, TestableRelation, Rule, Variable
from ie.substitution import backwardSubstituteRule, forwardSubstituteRule, matchExpressions
from typing import List, Union, Type, Callable


"""
    - remember once-made deductions
    
    - if information is not sufficient, ask user
    
    - would the code be simpler if we returned subst-dicts instead of substituted statements (especially the 'and' and 'or' functions)?
"""


def log(func):
    def wrapped(*args):
        print(f"Calling {func.__name__}{args} ...")
        result = func(*args)
        print(f"{func.__name__}{args} => {result}")
        return result
    return wrapped


class InferenceEngine:
    def __init__(self):
        self.facts = []
        self.rules = []

    def addFact(self, *expression):
        if expression not in self.facts:
            self.facts.append(expression)
        if len(expression) > 1:
            for word in expression:
                if isinstance(word, Fact):
                    self.addFact(word)

    def addRule(self, rule: Rule):
        if rule not in self.rules:
            self.rules.append(rule)
        for expression in rule.condition:
            if not isinstance(expression, tuple):
                if not isinstance(expression, Variable):
                    self.addFact(expression)
        for expression in rule.consequence:
            if not isinstance(expression, tuple):
                if not isinstance(expression, Variable):
                    self.addFact(expression)

    def __findInFacts(self, *expression):
        candidates = []
        for fact in self.facts:
            if matchExpressions(fact, expression):
                candidates.append(fact)
        return candidates

    def __findInRules(self, *conseq):
        candidates = []
        for rule in self.rules:
            if matchExpressions(rule.consequence, conseq):
                candidates.append(rule)
        return candidates
    
    @log
    def evalRule(self, rule: Rule):
        """ Returns a list of all the substitutions of ``rule.consequence``, 
            for which ``rule.condition`` holds true
        """

        conditionCandidates = self.evalExpression(*(rule.condition))
        consequenceCandidates = []
        for conditionCandidate in conditionCandidates:
            substRule = forwardSubstituteRule(rule, *conditionCandidate)
            consequenceCandidates.append(substRule.consequence)
        return consequenceCandidates

    @log
    def evalExpression(self, *expression):
        """ Returns a list of all the substitutions of ``expression``, 
            for which ``expression`` holds true
        """

        relation = expression[0]
        args = expression[1:]

        # Step 1: search known facts
        found = self.__findInFacts(*expression)

        # Step 2: if testable, test.
        if isinstance(relation, TestableRelation):
            found += relation.testRelation(self, *args)

        # Step 3: infer from known rules
        candidateRules = self.__findInRules(*expression)
        for rule in candidateRules:
            substRule = backwardSubstituteRule(rule, *expression)
            found += self.evalRule(substRule)

        return found
    
    def __repr__(self):
        return 'IE'


RelationTestFunction = Type[Callable[[InferenceEngine, List], List]]
