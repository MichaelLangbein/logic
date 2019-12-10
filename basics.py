from typing import Optional, List


class Statement:
    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return self.description


class Fact:
    def __init__(self, statement: Statement, truth: Optional[bool]):
        self.statement = statement
        self.truth = truth

    def __repr__(self):
        if self.truth is True:
            return f"'{self.statement}' holds true"
        elif self.truth is False:
            return f"'{self.statement}' does not hold true"
        else: 
            return f"It is unknown if '{self.statement}' holds true"


class Rule:
    def __init__(self, premises: List[Statement], consequence: Statement):
        self.premises = premises
        self.consequence = consequence

    def eval(self, facts: List[Fact]) -> Fact:
        allTrue: Optional[bool] = True
        for premise in self.premises:
            fact = next(f for f in facts if f.statement.description == premise.description)
            allTrue = allTrue and fact.truth
        if allTrue:
            return Fact(self.consequence, True)
        else: 
            return Fact(self.consequence, None)



if __name__ == "__main__":
    
    evaIsHappyS = Statement('Eva is happy')
    michaelIsHappyS = Statement('Michael is happy')
    thereIsCoffeeS = Statement('There is coffee')
    thereIsCoffeeF = Fact(thereIsCoffeeS, True)
    
    ifCoffeeEvaHappyR = Rule([thereIsCoffeeS], evaIsHappyS)
    ifEvaHappyMichaelHappyR = Rule([evaIsHappyS], michaelIsHappyS)

    evaIsHappyF = ifCoffeeEvaHappyR.eval([thereIsCoffeeF])
    michaelIsHappyF = ifEvaHappyMichaelHappyR.eval([evaIsHappyF])

    print(evaIsHappyF)
    print(michaelIsHappyF)