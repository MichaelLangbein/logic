

class Node:
    def __init__(self):
        pass


def divideSet(rows, columnName, value):
    splitFunction = None
    if isinstance(value, int) or isinstance(value, float):
        splitFunction = lambda row: row['columnName'] >= value
    else:
        splitFunction = lambda row: row['columnName'] != value
    set1 = []
    set2 = []
    for row in rows:
        if splitFunction(row):
            set1.append(row)
        else:
            set2.append(row)
    return (set1, set2)


def entropy(rows):
    from math import log
    log2 = lambda x: log(x)/log(2)
    colCounts = uniqueColCounts(rows)
    entropy = 0.0
    for colName in colCounts.keys():
        p = float(colCounts[colName]) / len(rows)
        entropy = entropy - p * log2(p)
    return entropy


def uniqueColCounts(rows):
    for colName in rows[0].keys():
        colVals = [row[colName] for row in rows]
        uniqueCount = len(unique())
    



