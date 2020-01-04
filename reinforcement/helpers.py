from reinforcement.classes import GameObject
import numpy as np


def stop(player, field):
    player.v = np.array((0, 0))
    player.a = np.array((0, 0))


def bounce(ball, field):
    ball.v = - ball.v


def normalize(arr):
    return arr / arr.sum()


def findInstance(cls, lst):
    for entry in lst:
        if isinstance(entry, cls):
            return entry


def intersects(obj1: GameObject, obj2: GameObject):
    if obj1.rect.colliderect(obj2.rect):
        return True
    return False


def outside(obj1: GameObject, obj2: GameObject):
    return not intersects(obj1, obj2)


def elasticCollision(obj1: GameObject, obj2: GameObject):
    deltaPos = obj1.x - obj2.x
    speedFactor = 1 # TODO
    massFactor = 2 * obj2.m / (obj1.m + obj2.m)
    obj1.v = obj1.v - massFactor * speedFactor * deltaPos
    
    deltaPos = obj2.x - obj1.x
    speedFactor = 1 # TODO
    massFactor = 2 * obj1.m / (obj1.m + obj2.m)
    obj2.v = obj2.v - massFactor * speedFactor * deltaPos