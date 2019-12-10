from typing import Optional, List, Any





class Fact:
    def __init__(self, statement, truth: Optional[bool], args = []):
        self.statement = statement
        self.truth = truth
        self.args = args

    def __repr__(self):
        if self.truth is True:
            return f"'{self.statement}' holds true for {self.args}"
        elif self.truth is False:
            return f"'{self.statement}' does not hold true for {self.args}"
        else: 
            return f"It is unknown if '{self.statement}' holds true for {self.args}"





class Relation:
    def __init__(self, statement, size: int, keys = []):
        self.statement = statement
        self.size = size
        self.entries = []
        self.keys = keys

    def add(self, entry: List[Fact]):
        if len(entry) == self.size:
            self.entries.append(entry)

    def eval(self, entryToCheck):
        for entry in self.entries:
            if entry == entryToCheck:
                return Fact(self.statement, True, entryToCheck)
        return Fact(self.statement, False, entryToCheck)

    def sk(self, *keys):
        self.keys = keys
        return self



class Rule:
    def __init__(self, premises: List[Relation], consequence: Relation):
        self.premises = premises
        self.consequence = consequence

    def eval(self, paras = {}) -> Fact:
        allPremisesTrue = True
        for premise in self.premises:
            keys = premise.keys
            vals = [paras[k] for k in keys]
            isTrue = premise.eval(vals)
            allPremisesTrue = allPremisesTrue and isTrue.truth
        keys = self.consequence.keys
        vals = [paras[k] for k in keys]
        if allPremisesTrue:
            return Fact(self.consequence.statement, True, vals)
        else:
            return Fact(self.consequence.statement, None, vals)




if __name__ == "__main__":

    
    """
    Testing 1st order logic
    """
    socrates = Fact('Socrates', True)
    isHumanRel = Relation('Is human', 1)
    isHumanRel.add([socrates])
    socatesIsHumanF = isHumanRel.eval([socrates])
    print(socatesIsHumanF)

    isMortalRel = Relation('Is mortal', 1)
    allHumansMortalR = Rule([isHumanRel.sk('X')], isMortalRel.sk('X'))
    socratesIsMortalF = allHumansMortalR.eval({'X': socrates})
    print(socratesIsMortalF)



    michael = Fact('Michael', True)
    eva = Fact('Eva', True)
    coffee = Fact('There is coffee', True)

    isThereCoffee = Relation('Is there coffee', 1)
    isThereCoffee.add([coffee])

    isEvaHappy = Relation('Is Eva happy', 0)

    evaHappyIfCoffee = Rule([isThereCoffee.sk('coffee')], isEvaHappy)
    evaHappyF = evaHappyIfCoffee.eval({'coffee': coffee})
    print(evaHappyF)

   

