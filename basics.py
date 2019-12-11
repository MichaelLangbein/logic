from typing import List



class Fact:
    def __init__(self, description, *args):
        self.description = description
        self.args = args


class Relation:
    def __init__(self, description):
        self.description = description
        self.entries = []

    def add(self, *args):
        self.entries.append(args)

    def includes(self, *args):
        for entry in self.entries:
            if entry == args:
                return True
        return False

    def v(self, *args):
        return Fact(self.description, *args)



class Rule:
    def __init__(self, conditions, consequences):
        self.conditions = conditions
        self.consequences = consequences


class InferenceEngine:
    def __init__(self):
        self.facts: List[Fact] = []
        self.relations: List[Relation] = []
        self.rules: List[Rule] = []

    def addFacts(self, *newFacts: List[Fact]):
        self.facts += newFacts

    def addRelations(self, *newRelations: List[Relation]):
        self.relations += newRelations

    def addRules(self, *newRules: List[Rule]):
        self.rules += newRules

    def eval(self, candidateFact: Fact):
        alreadyKnown = self.__findInFacts(candidateFact)
        if alreadyKnown:
            return True
        proven = self.__tryToDeduce(candidateFact)
        return proven

    def __findInFacts(self, candidate: Fact):
        for fact in self.facts:
            if fact.description == candidate.description:
                return True
        return False

    def __tryToDeduce(self, candidate: Fact):
        for rule in self.rules:
            if rule.consequences.includes(candidate.description):
                args = self.__getArgumentsForRule(rule)
                for arg in args:
                    newFacts = rule.eval(arg)
                    self.addFacts(newFacts)
                    if newFacts.include(candidate):
                        return True
        return False
        



if __name__ == '__main__':
    engine = InferenceEngine() 
    john = Fact('John')
    engine.addFacts(john)
    print(engine.eval(john))

    jane = Fact('Jane')
    engine.addFacts(jane)
    likes = Relation('likes')
    likes.add(jane, john)
    engine.addRelations(likes)
    print(engine.eval(likes.v(jane, john)))

    likes.add(john, jane)
    couple = Relation('couple')
    coupleIf = Rule([likes.v('X', 'Y'), likes.v('Y', 'X')], [couple.v('X', 'Y'), couple.v('Y', 'X')])
    engine.addRelations(couple)
    engine.addRules(coupleIf)
    print(engine.eval(couple.v(jane, john)))
