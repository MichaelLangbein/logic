from reinforcement.classes import Brain, Ball
from reinforcement.helpers import normalize, findInstance
import numpy as np


class RandomBrain(Brain):
    def choseDirection(self, player, environment):
        # move player in the direction of the ball
        return normalize(np.random.random(2) - np.array((0.5, 0.5)))



class SimpleBrain(Brain):
    def choseDirection(self, player, environment):
        ball = findInstance(Ball, environment)
        return normalize(player.x - ball.x)