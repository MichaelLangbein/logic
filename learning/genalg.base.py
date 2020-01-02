import numpy as np



class Individuum:
    pass


def randomSelection(geneSeed) -> Individuum:
    pass


def evaluateFitness(individuum: Individuum) -> Individuum:
    pass


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
        newGeneration = [mutateIndivid(individuum) for individuum in newGeneration]
        newGeneration = [evaluateFitness(individuum) for individuum in newGeneration]
        population = keepSurvivors(nrSurvivors, population, newGeneration)
    return population