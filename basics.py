from typing import Optional, List


class Statement:
    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return self.description


class Fact:
    def __init__(self, description: str, truth: Optional[bool]):
        self.description = description
        self.truth = truth

    def __repr__(self):
        if self.truth is True:
            return f"'{self.description}' holds true"
        elif self.truth is False:
            return f"'{self.description}' does not hold true"
        else: 
            return f"It is unknown if '{self.description}' holds true"


class Rule:
    def __init__(self, premises: List[Statement], consequence: Statement):
        self.premises = premises
        self.consequence = consequence

    def eval(self, facts: List[Fact]) -> Fact:
        allTrue: Optional[bool] = True
        for premise in self.premises:
            fact = next(f for f in facts if f.description == premise.description)
            allTrue = allTrue and fact.truth
        if allTrue:
            return Fact(self.consequence.description, True)
        else: 
            return Fact(self.consequence.description, None)



if __name__ == "__main__":
    
    thereIsCoffeeF = Fact('There is coffee', True)
    evaIsHappyS = Statement('Eva is happy')
    michaelIsHappyS = Statement('Michael is happy')
    
    ifCoffeeEvaHappyR = Rule([thereIsCoffeeF], evaIsHappyS)
    ifEvaHappyMichaelHappyR = Rule([evaIsHappyS], michaelIsHappyS)

    evaIsHappyF = ifCoffeeEvaHappyR.eval([thereIsCoffeeF])
    michaelIsHappyF = ifEvaHappyMichaelHappyR.eval([evaIsHappyF])

    print(evaIsHappyF)
    print(michaelIsHappyF)