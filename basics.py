
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
        def evalFunc(*args):
            return self.includes(*args)
        return Evaluable(self.description, evalFunc, args)


class Evaluable:
    def __init__(self, description, evalFunc, *inputs):
        self.description = description
        self.evalFunc = evalFunc
        self.inputs = inputs

    def getInputs(self):
        return [i for i in self.inputs if isinstance(i, str)]

    def eval(self):
        return self.evalFunc(*self.inputs)


class Object(Evaluable):
    def  __init__(self, description):
        super().__init__(description, lambda: True)


class Rule:
    def __init__(self, conditions, consequences):
        self.conditions = conditions
        self.consequences = consequences


class InferenceEngine:
    def __init__(self):
        self.vrs = []
        self.rules = []

    def add(self, something):
        if isinstance(something, Rule):
            self.rules.append(something)
        elif isinstance(something, Evaluable):
            self.vrs.append(something)

    def eval(self, question: Evaluable):
        requirements = question.getInputs()
        if not requirements:
            return question.eval()
        




if __name__ == '__main__':
    engine = InferenceEngine() 
    john = Object('John')
    engine.add(john)
    print(engine.eval(john))

    jane = Object('Jane')
    engine.add(jane)
    likes = Relation('likes')
    likes.add(jane, john)
    engine.add(likes)
    print(engine.eval(likes.v(jane, john)))

    likes.add(john, jane)
    couple = Relation('couple')
    coupleIf = Rule([likes.v('X', 'Y'), likes.v('Y', 'X')], [couple.v('X', 'Y'), couple.v('Y', 'X')])
    engine.add(couple)
    engine.add(coupleIf)
    print(engine.eval(couple.v(jane, john)))
