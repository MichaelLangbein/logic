from ie.substitution import listUnion, substituteExpressionWithDict, getTranslationDict
from ie.engine import InferenceEngine
from ie.base import TestableRelation


def __andFunction(ie: InferenceEngine, *statements):
    statement = statements[0]
    results = ie.evalExpression(*statement)
    
    if not statements[1:]:
        return [[r] for r in results]
    
    truthList = []
    for result in results:
        translationDict = getTranslationDict(statement, result)
        substatements = [substituteExpressionWithDict(s, translationDict) for s in statements[1:]]
        subresults = __andFunction(ie, *substatements)
        mergedResults = [[result] + subresult for subresult in subresults]
        truthList += mergedResults
    
    return truthList

def __andTestFunction(ie: InferenceEngine, *statements):
    allTuples = __andFunction(ie, *statements)
    return [tuple([And] + tupl) for tupl in allTuples]

And = TestableRelation('and', __andTestFunction)


def __orTestFunction(ie: InferenceEngine, *statements):
    truthList = []
    for statement in statements:
        truthList = listUnion(truthList, ie.evalExpression(*statement))
    return truthList

Or = TestableRelation('or', __orTestFunction)


def __notTestFunction(ie: InferenceEngine, *statements):
    pass

Not = TestableRelation('not', __notTestFunction)

