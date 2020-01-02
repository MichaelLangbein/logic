class Fact:
    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return self.description


class Relation(Fact):
    def __init__(self, description):
        super().__init__(description)

    def __repr__(self):
        return self.description


class TestableRelation(Relation):
    def __init__(self, description, relationTestFunction):
        super().__init__(description)
        self.relationTestFunction = relationTestFunction
    
    def testRelation(self, ie, *args):
        return self.relationTestFunction(ie, *args)


class Object(Fact):
    def __init__(self, description):
        super().__init__(description)


class Variable(Fact):
    def __init__(self, description, cls = Fact):
        super().__init__(description)
        self.cls = cls


class Rule:
    def __init__(self, condition: Fact, consequence: Fact):
        self.condition = condition
        self.consequence = consequence

    def __repr__(self):
        return f"if {self.condition} then {self.consequence}"

