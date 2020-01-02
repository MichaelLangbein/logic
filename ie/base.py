

class Fact:
    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return self.description


class Relation(Fact):
    def __init__(self, description):
        super().__init__(description)


class TestableRelation(Relation):
    def __init__(self, description, relationTestFunction):
        super().__init__(description)
        self.relationTestFunction = relationTestFunction
    
    def testRelation(self, *args):
        return self.relationTestFunction(*args)


class SimpleTestableRelation(TestableRelation):
    """
        Contrary to ``TestableRelation``s, a ``SimpleTestableRelation`` gives to the ``relationTestFunction`` only fully evaluated and substituted arguments.
        This way, the user does not need to evaluate any subexpressions. Also, the user only needs to return ``True`` or ``False`` instead of a TruthSet.
        However, this can have a performance impact: in a ``TestableRelation`` like ``And``, we don't need to evaluate all subexpressions if the first one already turns out to be false.
    """

    def __init__(self, description, relationTestFunction):
        super().__init__(self, description, relationTestFunction)

    def testRelation(self, ie, *args):
        substitutedArgs = []
        for arg in args:
            results = ie.evalExpression(*arg)
            substitutedArgs.append(results)

        truthSet = []
        for i in range(len(substitutedArgs[0])):
            newArgs = [row[i] for row in substitutedArgs]
            holds = self.relationTestFunction(newArgs)
            if holds:
                truthSet.append((self, *newArgs))

        return truthSet



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

