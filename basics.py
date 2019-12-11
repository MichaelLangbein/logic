from typing import List




class Relation:
    def __init__(self, description, nr):
        self.description = description
        self.nr = nr
        self.entries = []

    def add(self, *args):
        self.entries.append(args)

    def eval(self, *args):
        for entry in self.entries:
            if entry == args:
                return True
        return False


# A property is a unary relation
class Property(Relation):
    def __init__(self, description):
        super().__init__(description, 1)


# An object is a unary relation with one member
class Object(Relation):
    def __init__(self, description):
        super().__init__(description, 1)
        self.add(description)

    def add(self, *args):
        pass

    def eval(self):
        return True



class Rule:
    def __init__(self, conditions, consequences):
        self.conditions = conditions
        self.consequences = consequences


class InferenceEngine:
    def __init__(self):
        self.facts: List[Relation] = []
        self.rules: List[Rule] = []

    def addFacts(self, *newFacts: List[Relation]):
        self.facts += newFacts

    def addRules(self, *newRules: List[Rule]):
        self.rules += newRules

    def eval(self, candidateFact):
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
    john = Object('John')
    engine.addFacts(john)
    print(engine.eval(john))

    jane = Object('Jane')
    likes = Relation('likes', 2)
    likes.add(jane, john)
    engine.addFacts(jane, likes)
    print(engine.eval(likes.v(jane, john)))

    likes.add(john, jane)
    couple = Relation('couple', 2)
    coupleIf = Rule([likes.v('X', 'Y'), likes.v('Y', 'X')], [couple.v('X', 'Y'), couple.v('Y', 'X')])
    engine.addFacts(couple)
    engine.addRules(coupleIf)
    print(engine.eval(couple.v(jane, john)))

    coffeeThere = Object('There is coffee')
    happy = Relation('Is happy', 1)
    janeHappyIfCoffee = Rule([coffeeThere], [happy.v(jane)])
    engine.addFacts(coffeeThere, happy)
    engine.addRules(janeHappyIfCoffee)
    print(engine.eval(happy.v(jane)))
