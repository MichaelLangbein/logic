import pygame
import numpy as np
from reinforcement.globals import SCREEN_HEIGHT, SCREEN_WIDTH
from reinforcement.geometry import angle, normalize, magnitude

pygame.font.init()
font = pygame.font.SysFont('chalkduster.ttf', 72)


def direction(arr):
    return normalize(arr)


class GameObject:
    def __init__(self, imageName, x, m, fc = 0.0):

        # setup newtonian
        self.x = x
        self.v = np.array((0.0, 0.0))
        self.a = np.array((0.0, 0.0))
        self.m = m
        self.fc = fc  # friction coefficient with ground

        # setup image
        self.image = pygame.image.load("reinforcement/assets/" + imageName + ".png")
        self.moveRect()

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, deltat, environment):
        self.move(deltat)
        self.moveRect()

    def move(self, deltat):
        self.a += self.getFrictionCoefficient() * (- direction(self.v))
        self.x = self.x + self.v.dot(deltat) + self.a.dot(deltat * deltat)
        self.v = self.v + self.a.dot(deltat)
        self.a = np.array((0.0, 0.0))

    def moveRect(self):
        rect = self.image.get_rect()
        newPos = (self.x[0] - rect.width / 2, self.x[1] - rect.height / 2)
        self.rect = rect.move(newPos)

    def getFrictionCoefficient(self):
        if magnitude(self.v) > 0:
            return self.fc
        return 0.0


class Ball(GameObject):
    def __init__(self, x, m):
        super().__init__('soccerball', x, m, 50.0)

    def __repr__(self):
        return 'ball'


class Field(GameObject):
    def __init__(self):
        super().__init__('field', np.array((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)), 0)

    def update(self, deltat, environment):
        pass

    def __repr__(self):
        return 'field'


class Goal(GameObject):
    def __init__(self, teamName, x):
        self.teamName = teamName
        super().__init__('goal', x, 0)

    def update(self, deltat, environment):
        pass

    def __repr__(self):
        return f"goal {self.teamName}"


class Timer(GameObject):
    def __init__(self, seconds):
        self.delta = 0.0
        self.seconds = seconds
        self.x = np.array((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1 / 8))
        self.updateText()

    def updateText(self):
        text = f"{int(self.seconds)}"
        self.image = font.render(text, True, (255, 0, 0))
        self.moveRect()

    def update(self, deltat, environment):
        self.delta += deltat
        self.seconds -= deltat
        if self.delta > 1.0:
            self.updateText()
            self.delta = 0

    def __repr__(self):
        return 'timer'


class Counter(GameObject):
    def __init__(self):
        self.score = {
            'red': 0,
            'blue': 0
        }
        self.x = np.array((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 7 / 8))
        self.updateText()

    def updateText(self):
        text = f"{self.score['red']} : {self.score['blue']}"
        self.image = font.render(text, True, (255, 0, 0))
        self.moveRect()

    def increaseScore(self, teamName):
        self.score[teamName] += 1
        self.updateText()

    def update(self, deltat, environment):
        pass

    def __repr__(self):
        return 'counter'


class Brain:
    def choseDirection(self, player, environment):
        raise Exception('Not yet implemented!')


class Player(GameObject):
    def __init__(self, x, m, F, maxV, name, team, brain: Brain):
        if team == 'red':
            imageName = 'player_red'
        else:
            imageName = 'player_blue'
        super().__init__(imageName, x, m, 30)
        self.F = F
        self.maxV = maxV
        self.name = name
        self.team = team
        self.brain = brain

    def update(self, deltat, environment):
        newDir = self.brain.choseDirection(self, environment)
        F = self.F \
            * (1.0 - magnitude(self.v) / self.maxV)
        self.a = (F / self.m) * newDir
        super().update(deltat, environment)

    def __repr__(self):
        return f"{self.name} ({self.team})"

