from ied.engine import InferenceEngine
from ied.substitution import substituteExpression
from ied.base import TestableRelation
from ied.helpers import unique


def __andTestFunction(ie: InferenceEngine, *statements):
    statement = statements[0]
    substDicts = ie.evalExpression(*statement)
    if len(statements[1:]) == 0:
        return substDicts
    
    fullSubstDicts = []
    for substDict in substDicts:
        substStatements = [substituteExpression(statement, substDict) for statement in statements[1:]]
        subSubstDicts = __andTestFunction(ie, *substStatements)
        [d.update(substDict) for d in subSubstDicts]
        fullSubstDicts += subSubstDicts
    return unique(fullSubstDicts)

And = TestableRelation('and', __andTestFunction)


def __orTestFunction(ie: InferenceEngine, *statements):
    orDictList = []
    for statement in statements:
        tDicts = ie.evalExpression(*statement)
        if tDicts == True:
            return True
        orDictList += tDicts
    return unique(orDictList)

Or = TestableRelation('or', __orTestFunction)


def __notTestFunction(ie: InferenceEngine, *statements):
    pass

Not = TestableRelation('not', __notTestFunction)

