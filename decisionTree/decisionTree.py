from math import log, inf
from typing import List
import csv



class KVPair:
    def __init__(self, key, val):
        self.key = key
        self.val = val
    def __repr__(self):
        return f"[{self.key}, {self.val}]"


class Node:
    def __init__(self, splitPoint: KVPair, branch1, branch2):
        self.splitPoint = splitPoint
        self.branch1 = branch1
        self.branch2 = branch2

    def categorize(self, row):
        splitFunction = None
        if isinstance(self.splitPoint.val, int) or isinstance(self.splitPoint.val, float):
            splitFunction = lambda row: row[self.splitPoint.key] >= self.splitPoint.val
        else:
            splitFunction = lambda row: row[self.splitPoint.key] != self.splitPoint.val
        if splitFunction(row):
            # print(f"Categorized {row} by {self.splitPoint}: left")
            return self.branch1.categorize(row)
        else:
            # print(f"Categorized {row} by {self.splitPoint}: right")
            return self.branch2.categorize(row)
    def __repr__(self):
        return f"{self.splitPoint} -- branch1: {self.branch1} \n -- branch2: {self.branch2}"


class Leaf:
    def __init__(self, data, targets):
        self.data = data
        self.targets = targets

    def categorize(self, row):
        return valCounts(self.targets)
    
    def __repr__(self):
        return f"leaf with {len(self.data)} entries"


def countPrintTree(node):
    if isinstance(node, Leaf):
        l = len(node.data)
        print(f"leaf with {l} entries")
        return l
    else:
        l1 = countPrintTree(node.branch1)
        l2 = countPrintTree(node.branch2)
        print(f"node at {node.splitPoint}: {l1}, {l2}")
        return l1 + l2


def doCreateTree(splitPoints, rows, targets):
    ent = entropy(rows, targets)
    return createTree(splitPoints, rows, targets, ent)


def createTree(splitPoints: List[KVPair], rows, targets, entropy):
    if len(rows) == 1 or len(splitPoints) == 0:
        return Leaf(rows, targets)
    splitPoint, rows1, rows2, targ1, targ2, ent1, ent2 = split(splitPoints, rows, targets, entropy)
    if splitPoint is None:
        return Leaf(rows, targets)
    # print(f"splitting at {splitPoint}")
    newSplitPoints = [sp for sp in splitPoints if sp != splitPoint]
    tree1 = createTree(newSplitPoints, rows1, targ1, ent1)
    tree2 = createTree(newSplitPoints, rows2, targ2, ent2)
    return Node(splitPoint, tree1, tree2)


def split(splitPoints: List[KVPair], rows, targets, totalEnt):
    minInfoGain = - inf
    best = (None, None, None, None, None, None, None)
    for point in splitPoints:
        set1, set2, targets1, targets2 = splitRowsAt(rows, targets, point)
        if len(set1) > 0 and len(set2) > 0:
            ent1 = entropy(set1, targets1)
            ent2 = entropy(set2, targets2)
            q = len(set1)/len(rows)
            w = 1 - q
            infoGain = totalEnt - q*ent1 - w*ent2
            if infoGain > minInfoGain:
                minInfoGain = infoGain
                best = (point, set1, set2, targets1, targets2, ent1, ent2)
    return best


def splitRowsAt(rows, targets, point):
    splitFunction = None
    if isinstance(point.val, int) or isinstance(point.val, float):
        splitFunction = lambda row: row[point.key] >= point.val
    else:
        splitFunction = lambda row: row[point.key] != point.val
    set1 = []
    set2 = []
    targets1 = []
    targets2 = []
    for row, target in zip(rows, targets):
        if splitFunction(row):
            set1.append(row)
            targets1.append(target)
        else:
            set2.append(row)
            targets2.append(target)
    return (set1, set2, targets1, targets2)


def entropy(rows, targets):
    log2 = lambda x: log(x)/log(2)
    counts = valCounts(targets)
    entropy = 0.0
    for value in counts.keys():
        p = float(counts[value]) / len(rows)
        entropy = entropy - p * log2(p)
    return entropy


def valCounts(data):
    counts = {}
    for val in data:
        if not val in counts.keys():
            counts[val] = 1
        else:
            counts[val] += 1
    return counts


def unique(data):
    unique = []
    for d in data:
        if not d in unique:
            unique.append(d)
    return unique


if __name__ == '__main__':
    targetColumn = 'class'

    rows = []
    targets = []
    for row in csv.DictReader(open('data/mushrooms.csv')):
        targets.append(row.pop(targetColumn))
        rows.append(row)

    n = len(rows)
    trainingRows = rows[0: int(0.5*n)]
    trainingTargets = targets[0: int(0.5*n)]
    validationRows = rows[int(0.5*n):]
    validationTargets = targets[int(0.5*n):]

    splitPoints = []
    for key in trainingRows[0].keys():
        colVals = [row[key] for row in trainingRows]
        uniqueVals = unique(colVals)
        splitPoints += [KVPair(key, val) for val in uniqueVals]

    tree = doCreateTree(splitPoints, trainingRows, trainingTargets)
    
    for i in range(100):
        prediction = tree.categorize(validationRows[i])
        realVal = validationTargets[i]
        print(f"prediction: {prediction} -- real value: {realVal}")


