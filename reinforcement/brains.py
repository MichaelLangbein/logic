from reinforcement.classes import Brain, Ball
from reinforcement.helpers import normalize, findInstance
import numpy as np
import pygame


class RandomBrain(Brain):
    def choseDirection(self, player, environment):
        return normalize(np.random.random(2) - np.array((0.5, 0.5)))


class SimpleBrain(Brain):
    def choseDirection(self, player, environment):
        ball = findInstance(Ball, environment)
        return normalize(ball.x - player.x)


class PlayerBrain(Brain):
    def __init__(self):
        self.direction = np.array((0.0, 0.0))

    def handleEvent(self, event):
        if event.type == pygame.constants.KEYDOWN:
            if event.dict['key'] == pygame.constants.K_RIGHT:
                self.direction[0] = 1
            elif event.dict['key'] == pygame.constants.K_LEFT:
                self.direction[0] = -1
            elif event.dict['key'] == pygame.constants.K_DOWN:
                self.direction[1] = 1
            elif event.dict['key'] == pygame.constants.K_UP:
                self.direction[1] = -1
        elif event.type == pygame.constants.KEYUP:
            self.direction = np.array((0.0, 0.0))

    def choseDirection(self, player, environment):
        out = normalize(self.direction)
        return out