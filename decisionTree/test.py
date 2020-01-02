import csv
from decisionTree.decisionTree import doCreateTree, KVPair, unique


targetColumn = 'class'

rows = []
targets = []
for row in csv.DictReader(open('../data/mushrooms.csv')):
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

for i in range(1):
    prediction = tree.categorize(validationRows[i])
    realVal = validationTargets[i]
    print(f"prediction: {prediction} -- real value: {realVal}")

