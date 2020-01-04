from prisoners.players import Jesus, Satan, NiceTitForTat, MeanTitForTat, ForgivingTitForTat, Tester
from prisoners.generations import playForNGenerations


"""
Not only the strategies that the different players employ are relevant to the outcome. 
Also relevant is their environment!
Jesus fares really well in an overall good population, but really bad among all Satans.
If we play this game over multiple generations, cooperating agents seem to take over.
"""

players = [
    Jesus(),
    Satan(),
    NiceTitForTat(),
    MeanTitForTat(),
    ForgivingTitForTat(0.15),
    Tester()
]

players = playForNGenerations(players, 1)
