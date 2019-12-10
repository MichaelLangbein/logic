from typing import Union, Any, Callable

# Todo: Rule should accept multiple premisses
# Todo: Test non-membership


class Fact:
    def __init__(self, statementDescription, truth: bool, *args):
        self.statementDescription = statementDescription
        self.truth = truth
        self.args = args

    def __str__(self) -> str:
        if self.truth:
            return f"{self.statementDescription} holds for {self.args}"
        else:
            return f"{self.statementDescription} holds *not* for {self.args}"


Predicate = Callable[[Any], Union[bool, None]]
Result = Union[Fact, None]


class Statement:
    def __init__(self, description: str, holdsTrueFunc: Predicate = lambda inpt: None):
        self.description = description
        self.holdsTrueFunc = holdsTrueFunc

    def holdsTrueFor(self, *args) -> Result:
        result = self.holdsTrueFunc(*args)
        if result is None:
            return None
        else:
            return Fact(self.description, result, args)
        

class Rule:
    def __init__(self, premise: Statement, consequence: Statement):
        self.premise = premise
        self.consequence = consequence
    
    def deriveFor(self, *args) -> Result:
        result = self.premise.holdsTrueFor(*args)
        if result is None:
            return None
        else:
            return Fact(self.consequence.description, result.truth, args)




if __name__ == "__main__":
    
    class Man:
        def __init__(self, name):
            self.name = name
        def __str__(self):
            return self.name

    class Robot:
        def __init__(self, number):
            self.number = number
        def __str__(self):
            return f"Robot Nr. {self.number}"

    def isManFunc(something) -> Union[bool, None]:
        return isinstance(something, Man)

    isMan = Statement('Is a man', isManFunc)
    isMortal = Statement('Is mortal')
    allMenAreMortal = Rule(isMan, isMortal)

    socrates = Man('Socrates')
    bender = Robot('5432532')

    derivedFact = allMenAreMortal.deriveFor(socrates)
    print(derivedFact)
    derivedFact2 = allMenAreMortal.deriveFor(bender)
    print(derivedFact2)

