from typing import Optional, List, Any




class Statement:
    def __init__(self, description, args: List[Any] = []):
        self.description = description
        self.args = args

    def __repr__(self):
        return self.description


class Fact:
    def __init__(self, statement: Statement, truth: Optional[bool], args: List[Any] = []):
        self.statement = statement
        self.truth = truth
        self.args = args

    def __repr__(self):
        end = ""
        if len(self.args) > 0:
            end = f" for {self.args}"
        if self.truth is True:
            return f"'{self.statement}' holds true" + end
        elif self.truth is False:
            return f"'{self.statement}' does not hold true" + end
        else: 
            return f"It is unknown if '{self.statement}' holds true" + end


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
            consequenceInstances = self.__getConsequenceInstances(facts)
            return Fact(self.consequence, True, consequenceInstances)
        else: 
            return Fact(self.consequence, None)

    def __getConsequenceInstances(self, facts: List[Fact]):
        allInstances = []
        for fact in facts:
            allInstances.extend(fact.args)
        consequenceInstances = []
        for instance in allInstances:
            for C in self.consequence.args:
                if isinstance(instance, C):
                    consequenceInstances.append(instance)
        return consequenceInstances


if __name__ == "__main__":
    
    """
    Testing 0th order logic
    """

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



    """
    Testing 1st order logic
    """

    class Man:
        def __init__(self, name):
            self.name = name
        def __repr__(self):
            return self.name

    isManS = Statement('Is a man', [Man])
    isMortalS = Statement('Is mortal', [Man])

    ifIsManThenIsMortalR = Rule([isManS], isMortalS)

    pythagoras = Man('Pythagoras')
    pythagorasIsAManF = Fact(isManS, True, [pythagoras])

    pythagorasIsMortalF = ifIsManThenIsMortalR.eval([pythagorasIsAManF])

    print(pythagorasIsMortalF)