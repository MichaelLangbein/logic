from ied.base import Variable, Rule



def variableMatches(w1: Variable, w2):
    if isinstance(w2, Variable):
        return w1.cls == w2.cls
    return isinstance(w2, w1.cls)


def matchLeftToRight(expression1, expression2):
    '''
        returns a dict such that expression1 matches expression2. 
        The order is important!
    '''

    if len(expression1) != len(expression2):
        return False
    
    translationDict = {}
    for w1, w2 in zip(expression1, expression2):
        if isinstance(w1, Variable):
            if variableMatches(w1, w2):
                translationDict[w1] = w2
            else:
                return False
        elif w1 != w2:
            return False
    return translationDict


def matchRightToLeft(expression1, expression2):
    return matchLeftToRight(expression2, expression1)
        

def substituteExpression(expression, tDict):
    newExpression = []
    for word in expression:
        if isinstance(word, Variable) and word in tDict:
            newWord = tDict[word]
        elif isinstance(word, tuple):
            newWord = substituteExpression(word, tDict)
        else: 
            newWord = word
        newExpression.append(newWord)
    return tuple(newExpression)


def substituteRule(rule: Rule, tDict):
    return Rule(
        substituteExpression(rule.condition, tDict), 
        substituteExpression(rule.consequence, tDict))