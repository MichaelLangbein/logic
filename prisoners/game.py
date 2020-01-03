class Player:
    def __init__(self, name):
        self.name = name
        self.allSentences = 0

    def newMatch(self):
        pass

    def pickAction(self):
        raise Exception('Not implemented!')

    def getSentence(self, sentence):
        self.allSentences += sentence

    def __repr__(self):
        return self.name


NR_ROUNDS = 100
SENTENCE_VICTIM_OF_RATTING_OUT = 10
SENTENCE_BOTH_RATTED_OUT = 8
SENTENCE_BOTH_KEPT_QUIET = 0.5
SENTENCE_SUCCESSFULL_RATTING = 0



def getRanking(players):
    players.sort(key = lambda el: el.allSentences)
    sentences = [el.allSentences for el in players]
    return zip(sentences, players)


def roundRobin(player, *opponents):
    print(f"********* {player} now faces {len(opponents)} opponents ************")
    for opponent in opponents:
        playGame(player, opponent)
    if len(opponents) > 1:
        roundRobin(*opponents)


def playGame(player1, player2):
    print(f"-------- match {player1} vs. {player2} -----------------")
    player1.newMatch()
    player2.newMatch()
    for _ in range(NR_ROUNDS):
        playRound(player1, player2)


def playRound(player1, player2):
    action1 = player1.pickAction()
    action2 = player2.pickAction()
    sentence1, sentence2 = calculateSentence(action1, action2)
    player1.getSentence(sentence1)
    player2.getSentence(sentence2)
    print(f"{player1} -> {action1}, {player2} -> {action2}")
    print(f"{player1} <- {sentence1} years, {player2} <- {sentence2} years")


def calculateSentence(action1, action2):
    if action1 == 'treason' and action2 == 'cooperation':
        sentence1 = SENTENCE_SUCCESSFULL_RATTING
        sentence2 = SENTENCE_VICTIM_OF_RATTING_OUT
    elif action1 == 'cooperation' and action2 == 'treason':
        sentence1 = SENTENCE_VICTIM_OF_RATTING_OUT
        sentence2 = SENTENCE_SUCCESSFULL_RATTING
    elif action1 == 'cooperation' and action2 == 'cooperation':
        sentence1 = SENTENCE_BOTH_KEPT_QUIET
        sentence2 = SENTENCE_BOTH_KEPT_QUIET
    elif action1 == 'treason' and action2 == 'treason':
        sentence1 = SENTENCE_BOTH_RATTED_OUT
        sentence2 = SENTENCE_BOTH_RATTED_OUT
    return sentence1, sentence2
