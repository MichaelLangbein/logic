from typing import Optional, List, Any





class Fact:
    def __init__(self, statement, args = [], keys = []):
        self.statement = statement
        self.args = args
        self.keys = keys

    def eval(self, vals):
        if vals == self.args:
            return True
    
    def sk(self, *keys):
        self.keys = keys
        return self

    def __repr__(self):
        return self.statement




class Relation:
    def __init__(self, statement, size, keys = []):
        self.statement = statement
        self.size = size
        self.entries = []
        self.keys = keys

    def add(self, entry):
        if len(entry) == self.size:
            self.entries.append(entry)

    def eval(self, entryToCheck):
        for entry in self.entries:
            if entry == entryToCheck:
                return True

    def sk(self, *keys):
        self.keys = keys
        return self

    def sv(self, *vals):
        newRel = Relation(self.statement, self.size, self.keys)
        newRel.add(vals)
        return newRel



class Rule:
    def __init__(self, premises, consequence):
        self.premises = premises
        self.consequence = consequence

    def eval(self, paras = {}):
        allPremisesTrue = True
        for premise in self.premises:
            keys = premise.keys
            vals = [paras[k] for k in keys]
            isTrue = premise.eval(vals)
            allPremisesTrue = allPremisesTrue and isTrue
        keys = self.consequence.keys
        vals = [paras[k] for k in keys]
        if allPremisesTrue:
            return Fact(self.consequence.statement, vals)




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


    thereIsCoffee = Fact('There is coffee', True)
    eva = Fact('Eva', True)
    michael = Fact('Michael', True)
    
    isHappy = Relation('Is happy', 1)

    evaHappyIfCoffee = Rule([thereIsCoffee], isHappy.sv(eva))
    evaHappyF = evaHappyIfCoffee.eval()
    print(evaHappyF)

    michaelHappyIfEva = Rule([isHappy.eval(eva)], isHappy.sv(michael))
    michaelHappyF = michaelHappyIfEva.eval()

   

