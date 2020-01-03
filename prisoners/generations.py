from prisoners.game import roundRobin, getRanking
import numpy as np


def draw(population):
    population.sort(key = lambda e: e.allSentences, reverse = True)
    ranking = [e.allSentences for e in population]
    minR = min(ranking)
    maxR = max(ranking)
    range = maxR - minR
    draw = np.random.random() * range + minR
    for e in population:
        if e.allSentences <= draw:
            return e


def drawNewGeneration(population):
    populationSize = len(population)
    newPopulation = [draw(population) for _ in range(populationSize)]
    return newPopulation


def playForNGenerations(population, nrGenerations):
    for _ in range(nrGenerations):
        roundRobin(*population)
        population = drawNewGeneration(population)
        print(f"+++++++++ population now consists of {population} ++++++++++++++++++++")
    return population