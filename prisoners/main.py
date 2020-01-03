from prisoners.players import Jesus, Satan, NiceTitForTat, MeanTitForTat, ForgivingTitForTat
from prisoners.game import roundRobin, getRanking
from prisoners.generations import playForNGenerations


"""
Not only the strategies that the different players employ are relevant to the outcome. 
Also relevant is their environment!
Jesus fares really well in an overall good population, but really bad among all Satans.
If we play this game over multiple generations, cooperating agents seem to take over.
"""


player1 = Jesus()
player2 = Satan()
player3 = NiceTitForTat()
player4 = MeanTitForTat()
player5 = ForgivingTitForTat(0.15)
players = [player1, player2, player3, player4, player5]

players = playForNGenerations(players, 1)
ranking = getRanking(players)
for rating, player in ranking:
    print(f"sentence: {rating} --- player: {player}")