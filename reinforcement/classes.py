import pygame
import numpy as np


def normalize(arr):
    if arr[0] == 0 and arr[1] == 0:
        return arr
    return arr / arr.sum()


class GameObject:
    def __init__(self, imageName, x, m):

        # setup newtonian
        self.x = x
        self.v = np.array((0, 0))
        self.a = np.array((0, 0))
        self.m = m

        # setup image
        self.image = pygame.image.load("reinforcement/assets/" + imageName + ".png")
        self.moveRect()

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, deltat, environment):
        self.move(deltat)
        self.moveRect()

    def move(self, deltat):
        friction = -0.1 * normalize(self.a)
        self.x = self.x + self.v.dot(deltat) + self.a.dot(deltat * deltat) - friction.dot(deltat * deltat)
        self.v = self.v + self.a.dot(deltat)
        self.a = np.array((0, 0))

    def moveRect(self):
        rect = self.image.get_rect()
        newPos = (self.x[0] - rect.width / 2, self.x[1] - rect.height / 2)
        self.rect = rect.move(newPos)



class Ball(GameObject):
    def __init__(self, x, m):
        super().__init__('soccerball', x, m)

    def __repr__(self):
        return 'ball'


class Field(GameObject):
    def __init__(self):
        super().__init__('field', np.array((400, 250)), 0)

    def __repr__(self):
        return 'field'


class Brain:
    def choseDirection(self, player, environment):
        raise Exception('Not yet implemented!')


class Player(GameObject):
    def __init__(self, x, m, F, name, team, brain: Brain):
        if team == 'red':
            imageName = 'player_red'
        else:
            imageName = 'player_blue'
        super().__init__(imageName, x, m)
        self.F = F
        self.name = name
        self.team = team
        self.brain = brain

    def update(self, deltat, environment):
        newDir = self.brain.choseDirection(self, environment)
        self.a = (self.F / self.m) * newDir
        super().update(deltat, environment)

    def __repr__(self):
        return f"{self.name} ({self.team})"

