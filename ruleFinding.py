import numpy as np


"""
    Basic idea: evolve new rules using genetic algorithm.
    Gene-seed might be taken from existing inference engine.

    Instead of a popuplation of rules, 
    we take a popuplation of query parameters.
    Once we have queried useful data, a random forrest will help us find a good, outformulated rule.
    So, in reality, we're not evolving good rules, but useful queries.

    This at first sight seems less deep than just evolving ideas themself. 
    But is it really? Think of it this way:
    Wikidata is our knowledge base. 
    One part of creativity is finding rules based on facts, (thats handled with random forrest, better than genalg),
    but another part of creativity is deciding on what part of your knowledge-base you want to work on.
"""


def queryData(paras):
    pass


def randomForrest(data, paras):
    pass


class Fitness:
    def __init__(self, testSize, successes):
        self.testSize = testSize
        self.successes = successes


class Idea:
    def __init__(self, paras):
        self.paras = paras

    def createHypothesis(self):
        data = queryData(self.paras)
        return randomForrest(data, self.paras)


def evaluateFitness(idea: Idea) -> Idea:
    pass


def drawByFitness(ideas):
    ideas.sort(key = lambda i: i.fitness)
    maxFitness = ideas[0].fitness
    randVal = maxFitness * np.random.random()
    lowestCandidate = ideas[0]
    for idea in ideas:
        if idea.fitness > randVal and idea.fitness < lowestCandidate.fitness:
            lowestCandidate = idea
    return lowestCandidate 


def keepSurvivors(nrSurvivors, oldGen, newGen):
    oldGen.sort(key = lambda i: i.fitness)
    newGen.sort(key = lambda i: i.fitness)
    return oldGen[:nrSurvivors] + newGen[:-nrSurvivors]


def recombineIdeas(idea1, idea2):
    


def evolveIdeas(geneSeed, populationSize, generationsNr, survivorsNr):
    ideas = [Idea(randomSelection(geneSeed)) for i in range(populationSize)]
    ideas = [evaluateFitness(idea) for idea in ideas]
    for g in range(generationsNr):
        couples = [(drawByFitness(ideas), drawByFitness(ideas)) for i in range(populationSize)]
        recombinations = [recombineIdeas(idea1, idea2) for idea1, idea2 in couples]
        newGeneration = [mutateIdea(idea) for idea in newGeneration]
        newGeneration = [evaluateFitness(idea) for idea in ideas]
        ideas = keepSurvivors(survivorsNr, ideas, newGeneration)
    return ideas
