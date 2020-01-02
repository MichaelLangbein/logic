from ied.base import Fact, Object, Relation, TestableRelation, Rule, Variable
from ied.substitution import matchLeftToRight, matchRightToLeft, substituteRule, substituteExpression
from ied.helpers import unique
from typing import List


def log(func):
    def wrapped(*args):
        print(f"{args} ...")
        result = func(*args)
        print(f"... => {result}")
        return result
    return wrapped



class InferenceEngine:

    def __init__(self):
        self.facts: List[Fact] = []
        self.rules: List[Rule] = []


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
        foundDicts = []
        for fact in self.facts:
            match = matchRightToLeft(fact, expression)
            if match is not False:
                foundDicts.append(match)
        return unique(foundDicts)


    def __findCandidateRules(self, *expression):
        candidates = []
        for rule in self.rules:
            match = matchLeftToRight(rule.consequence, expression)
            if match is not False:
                candidates.append(substituteRule(rule, match))
        return candidates

    @log
    def evalExpression(self, *expression):

        # objects just evaluate to true
        if len(expression) == 1 and isinstance(expression[0], Object):
            return [{}]

        # find in kb
        foundDicts = self.__findInFacts(*expression)
        if foundDicts == [{}]:
            return foundDicts
        
        # if expression is testable, test.
        testedDicts = []
        if isinstance(expression[0], TestableRelation):
            testedDicts = expression[0].testRelation(self, *(expression[1:]))
            if testedDicts == [{}]:
                return testedDicts

        # try to deduce expression from rules.
        deducedDicts = []
        for candidate in self.__findCandidateRules(*expression):
            conditionDicts = self.evalExpression(*(candidate.condition))
            if conditionDicts == [{}]:
                return conditionDicts
            deducedDicts += conditionDicts

        # TODO: if no condition is met, ask user for required facts

        return unique(foundDicts + testedDicts + deducedDicts)


    def evalAndSubstituteExpression(self, *expression):
        tDicts = self.evalExpression(*expression)
        if tDicts == True:
            return [expression]
        substitutions = [substituteExpression(expression, tDict) for tDict in tDicts]
        return substitutions


    def __repr__(self):
        return 'IE'