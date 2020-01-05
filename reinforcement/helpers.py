import numpy as np
from reinforcement.classes import GameObject, Field, Player, Ball
import time
import sys


def inDebugMode():
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace is None:
        return False
    else:
        return True


def stop(player: Player, field: Field):
    # stop movement
    player.v = np.array((0, 0))
    player.a = np.array((0, 0))


def bounce(ball: Ball, direction):
    if direction == 'L' or direction == 'R':
        ball.v[0] = - ball.v[0]
    if direction == 'T' or direction == 'B':
        ball.v[1] = - ball.v[1]


def normalize(arr):
    return arr / magnitude(arr)


def findInstance(cls, lst):
    for entry in lst:
        if isinstance(entry, cls):
            return entry


def touchesEdge(obj1, obj2):
    l1 = obj1.rect.left
    r1 = obj1.rect.right
    t1 = obj1.rect.top
    b1 = obj1.rect.bottom

    l2 = obj2.rect.left
    r2 = obj2.rect.right
    t2 = obj2.rect.top
    b2 = obj2.rect.bottom

    if l1 < l2 < r2:
        return 'L'
    if b1 > b2 > t1:
        return 'B'
    if l1 < r2 < r1:
        return 'R'
    if t1 < t2 < b1:
        return 'T'
    return None


def intersects(obj1: GameObject, obj2: GameObject):
    if obj1.rect.colliderect(obj2.rect):
        return True
    return False


def angle(arr1, arr2):
    d = innerProd(arr1, arr2)
    n = magnitude(arr1) * magnitude(arr2)
    return np.arccos((d/n))


def facing(obj1: GameObject, obj2: GameObject):
    directionMovement = obj1.v
    directionOther = obj2.x - obj1.x
    angleToOther = angle(directionMovement, directionOther)
    return angleToOther < np.pi / 2


collideHistory = []
def inCollideHistory(obj1, obj2, deltat):
    currentTime = time.perf_counter()
    for o1, o2, t in collideHistory:
        if o1 == obj1 and o2 == obj2 and (currentTime - t < deltat):
            return True
    return False

def withCollideHistory(func):
    def wrapped(obj1, obj2):
        if inCollideHistory(obj1, obj2, 0.2):
            return False
        elif func(obj1, obj2):
            collideHistory.append((obj1, obj2, time.perf_counter()))
            return True
    return wrapped      

# @withCollideHistory
def collides(obj1: GameObject, obj2: GameObject):
    if intersects(obj1, obj2) and (facing(obj1, obj2) or facing(obj2, obj1)):
        return True
    return False


def outside(obj1, obj2):
    return not intersects(obj1, obj2)


def innerProd(arr1, arr2):
    return np.inner(arr1, arr2)


def magnitude(arr):
    return np.sqrt(arr[0]**2 + arr[1]**2)


def elasticCollision(obj1: GameObject, obj2: GameObject):
    deltaPos = obj1.x - obj2.x
    speedFactor = innerProd(obj1.v - obj2.v, obj1.x - obj2.x) / magnitude(obj1.x - obj2.x) ** 2
    massFactor = 2 * obj2.m / (obj1.m + obj2.m)
    obj1.v = obj1.v - massFactor * speedFactor * deltaPos
    
    deltaPos = obj2.x - obj1.x
    speedFactor = innerProd(obj2.v - obj1.v, obj2.x - obj1.x) / magnitude(obj2.x - obj1.x) ** 2
    massFactor = 2 * obj1.m / (obj1.m + obj2.m)
    obj2.v = obj2.v - massFactor * speedFactor * deltaPos