from prisoners.game import Player, SENTENCE_BOTH_KEPT_QUIET, SENTENCE_BOTH_RATTED_OUT, SENTENCE_SUCCESSFULL_RATTING, SENTENCE_VICTIM_OF_RATTING_OUT
import numpy as np



class Jesus(Player):
    def __init__(self):
        super().__init__('Jesus')

    def pickAction(self):
        return 'cooperation'


class Satan(Player):
    def __init__(self):
        super().__init__('Satan')

    def pickAction(self):
        return 'treason'


class NiceTitForTat(Player):
    def __init__(self):
        super().__init__('NiceTitForTat')
        self.lastSentence = None

    def getSentence(self, sentence):
        self.lastSentence = sentence
        super().getSentence(sentence)

    def pickAction(self):
        if self.lastSentence is None: # beginning
            return 'cooperation'
        if self.lastSentence == SENTENCE_BOTH_KEPT_QUIET  or self.lastSentence == SENTENCE_SUCCESSFULL_RATTING: # opponent cooperated
            return 'cooperation'
        if self.lastSentence == SENTENCE_BOTH_RATTED_OUT or self.lastSentence == SENTENCE_VICTIM_OF_RATTING_OUT: # opponent ratted out
            return 'treason'

    def newMatch(self):
        self.lastSentence = None


class MeanTitForTat(Player):
    def __init__(self):
        super().__init__('MeanTitForTat')
        self.lastSentence = None

    def getSentence(self, sentence):
        self.lastSentence = sentence
        super().getSentence(sentence)

    def pickAction(self):
        if self.lastSentence is None: # beginning
            return 'treason'
        if self.lastSentence == SENTENCE_BOTH_KEPT_QUIET  or self.lastSentence == SENTENCE_SUCCESSFULL_RATTING: # opponent cooperated
            return 'cooperation'
        if self.lastSentence == SENTENCE_BOTH_RATTED_OUT or self.lastSentence == SENTENCE_VICTIM_OF_RATTING_OUT: # opponent ratted out
            return 'treason'

    def newMatch(self):
        self.lastSentence = None

class ForgivingTitForTat(Player):
    def __init__(self, chanceOfForgiving):
        super().__init__('ForgivingTitForTat')
        self.lastSentence = None
        self.chanceOfForgiving = chanceOfForgiving

    def getSentence(self, sentence):
        self.lastSentence = sentence
        super().getSentence(sentence)

    def pickAction(self):
        if self.lastSentence is None: # beginning
            return 'cooperation'
        if self.lastSentence == SENTENCE_BOTH_KEPT_QUIET or self.lastSentence == SENTENCE_SUCCESSFULL_RATTING: # opponent cooperated
            return 'cooperation'
        if self.lastSentence == SENTENCE_BOTH_RATTED_OUT or self.lastSentence == SENTENCE_VICTIM_OF_RATTING_OUT: # opponent ratted out -> retalliate in 90% of cases
            if np.random.random() < self.chanceOfForgiving: 
                print(f"{self} chose to forgive!")
                return 'cooperation'
            else:
                return 'cooperation'

    def newMatch(self):
        self.lastSentence = None