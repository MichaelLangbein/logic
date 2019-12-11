from typing import List



class Fact:
    def __init__(self, relation, *args):
        self.relation = relation
        self.args = args


class Relation:
    def __init__(self, description, nr, keys = []):
        self.description = description
        self.nr = nr
        self.entries = []
        self.keys = keys

    def add(self, *args):
        self.entries.append(args)

    def eval(self, *args):
        for entry in self.entries:
            if entry == args:
                return True
        return False

    def v(self, *keys):
        self.keys = keys
        return self


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
    def __init__(self, conditions: List[Relation], consequences: List[Relation]):
        self.conditions = conditions
        self.consequences = consequences

    def eval(self, inputDict) -> List[Fact]:
        try:
            for condition in self.conditions:
                keys = contion.keys
                args = [inputDict[key] for key in keys]
            outputs = []
            for consequence in self.consequences:
                keys = consequence.keys
                args = [inputDict[key] for key in keys]
                newFact = Fact(consequence, *args)
                outputs.push(newFact)
            return outputs
        except:
            return []



class InferenceEngine:
    def __init__(self):
        self.facts: List[Fact] = []
        self.relations: List[Relation] = []
        self.rules: List[Rule] = []

    def addRelations(self, *newRelations: List[Relation]):
        self.relations += newRelations

    def addRules(self, *newRules: List[Rule]):
        self.rules += newRules

    def __addFacts(self, *newFacts: List[Fact]):
        self.facts += newFacts

    def eval(self, relation, *args):
        alreadyKnown = self.__findInFacts(relation, *args)
        if alreadyKnown:
            return True
        proven = self.__tryToDeduce(relation, *args)
        return proven

    def __findInFacts(self, relation, *args):
        for fact in self.facts:
            if fact.relation == relation and fact.args == args:
                return True
        return False

    def __tryToDeduce(self, relation, *args):
        for rule in self.rules:
            if rule.consequences.index(relation):
                args = self.__getArgumentsForRule(rule)
                for arg in args:
                    newFacts = rule.eval(arg)
                    self.__addFacts(newFacts)
                    for fact in newFacts:
                        if fact.relation == relation and fact.args == args:
                            return True
        return False
        
    def __getArgumentsForRule(self, rule: Rule):
        return []



if __name__ == '__main__':
    engine = InferenceEngine() 
    john = Object('John')
    engine.addRelations(john)
    print(engine.eval(john))

    jane = Object('Jane')
    likes = Relation('likes', 2)
    likes.add(jane, john)
    engine.addRelations(jane, likes)
    print(engine.eval(likes, jane, john))

    likes.add(john, jane)
    couple = Relation('couple', 2)
    coupleIf = Rule([likes.v('X', 'Y'), likes.v('Y', 'X')], [couple.v('X', 'Y'), couple.v('Y', 'X')])
    engine.addRelations(couple)
    engine.addRules(coupleIf)
    print(engine.eval(couple, jane, john))

    coffeeThere = Object('There is coffee')
    happy = Relation('Is happy', 1)
    janeHappyIfCoffee = Rule([coffeeThere], [happy.v(jane)])
    engine.addRelations(coffeeThere, happy)
    engine.addRules(janeHappyIfCoffee)
    print(engine.eval(happy, jane))
