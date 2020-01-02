import numpy as np
from learning.analysis import findRules, evaluateQuality


"""
Wiki-data is a huge knowledge base.
The objective here is to learn rules from that kb to be used in an inference engine.

How does one find rules frome a knowledge base?
Well, I often move from link to link through wikipedia. 
Sometimes i find topic x on a site that seems to be related to topic y from a completely other site.
Our geneseed could be a list of random walks through wikimedias links.
We could try to recombine some points in these walks.

This at first sight seems less deep than just evolving ideas themself. 
But is it really? Think of it this way:
Wikidata is our knowledge base. 
One part of creativity is finding rules based on facts, (thats handled with random forrest, better than genalg),
but another part of creativity is deciding on what part of your knowledge-base you want to work on.
"""


class Individuum:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = None

    def queryData(self):
        pass


def randomSelection(geneSeed) -> Individuum:
    pass


def evaluateFitness(individuum: Individuum) -> Individuum:
    data = individuum.queryData()
    rules = findRules(data)
    quality = [evaluateQuality(rule, data) for rule in rules]


def recombineIndivids(individuum1: Individuum, individuum2: Individuum):
    pass


def mutateIndivid(individuum: Individuum):
    pass


def drawByFitness(population):
    population.sort(key = lambda i: i.fitness)
    maxFitness = population[0].fitness
    randVal = maxFitness * np.random.random()
    lowestCandidate = population[0]
    for individuum in population:
        if individuum.fitness > randVal and individuum.fitness < lowestCandidate.fitness:
            lowestCandidate = individuum
    return lowestCandidate 


def keepSurvivors(nrSurvivors, oldGen, newGen):
    oldGen.sort(key = lambda i: i.fitness)
    newGen.sort(key = lambda i: i.fitness)
    return oldGen[:nrSurvivors] + newGen[:-nrSurvivors]


def evolve(geneSeed, populationSize, nrGenerations, nrSurvivors):
    population = [Individuum(randomSelection(geneSeed)) for i in range(populationSize)]
    population = [evaluateFitness(individuum) for individuum in population]
    for g in range(nrGenerations):
        couples = [(drawByFitness(population), drawByFitness(population)) for i in range(populationSize)]
        recombinations = [recombineIndivids(individuum1, individuum2) for individuum1, individuum2 in couples]
        newGeneration = [mutateIndivid(individuum) for individuum in recombinations]
        newGeneration = [evaluateFitness(individuum) for individuum in newGeneration]
        population = keepSurvivors(nrSurvivors, population, newGeneration)
    return population