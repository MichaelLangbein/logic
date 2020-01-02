from learning.genalg import evolve
from learning.scraping import getRandomPaths



populationSize = 1000
nrGenerations = 1000
nrSurvivors = 100
geneSeed = getRandomPaths(1000)
lastGeneration = evolve(geneSeed, populationSize, nrGenerations, nrSurvivors)