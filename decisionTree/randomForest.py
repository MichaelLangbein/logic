from math import log, inf
from random import random
import csv
from decisionTree import unique, KVPair, doCreateTree


def randPredArr(count, prob):
    out = []
    for i in range(count):
        if random() < prob:
            out.append(True)
        else:
            out.append(False)
    return out


def draw(arr, doDraw):
    out = []
    for i in range(len(arr)):
        pred = doDraw[i]
        if pred:
            out.append(arr[i])
    return out

def addDicts(d1, d2):
    keys1 = list(d1.keys())
    keys2 = list(d2.keys())
    keys = unique(keys1 + keys2)
    out = {}
    for key in keys:
        out[key] = 0
        if key in d1:
            out[key] += d1[key]
        if key in d2:
            out[key] += d2[key]
    return out



class RandomForest:
    def __init__(self, nrTrees, trainingRows, trainingTargets):
        n = len(trainingRows)
        trees = []
        for _ in range(nrTrees):
            indices = randPredArr(n, 0.5)
            subTrainingRows = draw(trainingRows, indices)
            subTrainingTargets = draw(trainingTargets, indices)

            splitPoints = []
            for key in subTrainingRows[0].keys():
                colVals = [row[key] for row in subTrainingRows]
                uniqueVals = unique(colVals)
                splitPoints += [KVPair(key, val) for val in uniqueVals]

            tree = doCreateTree(splitPoints, subTrainingRows, subTrainingTargets)
            trees.append(tree)

        self.trees = trees

    def predict(self, row):
        prediction = {}
        for i, tree in enumerate(self.trees):
            print(f"... predicting {i} of {len(self.trees)} ...")
            treeClassification = tree.categorize(row)
            prediction = addDicts(treeClassification, prediction)
        return prediction




if __name__ == "__main__":

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

    forrest = RandomForest(10, trainingRows, trainingTargets)

    for i in range(10):
        row = validationRows[i]
        target = validationTargets[i]
        pred = forrest.predict(row)
        print(f"prediction: {pred} -- real value: {target}")