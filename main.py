from typing import Optional, Union, Any, Callable, List



class Fact:
    def __init__(self, statementDescription, truth: Optional[bool], *args):
        self.statementDescription = statementDescription
        self.truth = truth
        self.args = args

    def __str__(self) -> str:
        if self.truth is True:
            return f"'{self.statementDescription}' holds for {self.args}"
        elif self.truth is False:
            return f"'{self.statementDescription}' holds *not* for {self.args}"
        else:
            return f"It is unknown if '{self.statementDescription}' holds for {self.args}"



Predicate = Callable[[Any], Optional[bool]]


class Statement:
    def __init__(self, description: str, holdsTrueFunc: Predicate = lambda inpt: None):
        self.description = description
        self.holdsTrueFunc = holdsTrueFunc

    def holdsTrueFor(self, *args) -> Fact:
        result = self.holdsTrueFunc(*args)
        return Fact(self.description, result, args)
        

class Rule:
    def __init__(self, premises: List[Statement], consequence: Statement):
        self.premises = premises
        self.consequence = consequence
    
    def deriveFor(self, *args) -> Fact:
        allPremissesFulfilled: Optional[bool] = True
        for premise in self.premises:
            result = premise.holdsTrueFor(*args)
            allPremissesFulfilled = allPremissesFulfilled and result.truth
        if allPremissesFulfilled is True:
            return Fact(self.consequence.description, allPremissesFulfilled, args)
        else:
            return Fact(self.consequence.description, None, args)



if __name__ == "__main__":
    
    class Man:
        def __init__(self, name):
            self.name = name
        def __repr__(self):
            return self.name

    class Robot:
        def __init__(self, number):
            self.number = number
        def __repr__(self):
            return f"Robot Nr. {self.number}"

    def isManFunc(something) -> Optional[bool]:
        return isinstance(something, Man)

    isMan = Statement('Is a man', isManFunc)
    isMortal = Statement('Is mortal')
    allMenAreMortal = Rule([isMan], isMortal)

    socrates = Man('Socrates')
    bender = Robot('5432532')

    derivedFact = allMenAreMortal.deriveFor(socrates)
    print(derivedFact)
    derivedFact2 = allMenAreMortal.deriveFor(bender)
    print(derivedFact2)

