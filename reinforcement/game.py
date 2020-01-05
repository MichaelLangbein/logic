import pygame
import numpy as np
from reinforcement.helpers import collides, elasticCollision, outside, stop, bounce, touchesEdge
from reinforcement.classes import Field, Ball, Player
from reinforcement.brains import SimpleBrain, RandomBrain
from reinforcement.globals import SCREEN_HEIGHT, SCREEN_WIDTH
import time



def ballInMiddle(ball):
    ball.x = np.array((400.0, 250.0))
    ball.v = np.array((0.0, 0.0))
    ball.a = np.array((0.0, 0.0))


def playGame(players):
    pygame.init()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    field = Field()
    ball = Ball((400, 250), 3)
    objects = [field, ball] + players
    
    running = True
    fps = 20.0
    loopTime = 1.0 / fps
    deltaTime = 0.1
    while running:
        startTime = time.perf_counter()

        # Step 1: handle events
        for event in pygame.event.get():
            pass

        # Step 2: handle logic
        for player in players:
            if collides(player, ball):
                elasticCollision(player, ball)
            if outside(player, field):
                stop(player, field)
        touchedEdge = touchesEdge(ball, field)
        if touchedEdge:
            bounce(ball, touchedEdge)
        if outside(ball, field):
            ballInMiddle(ball)
        for obj in objects:
            obj.update(deltaTime, objects)
        
        # Step 3: render
        screen.fill((0, 0, 0))
        for obj in objects:
            obj.render(screen)
        pygame.display.flip()

        endTime = time.perf_counter()
        deltaTime = endTime - startTime
        timeRemaining = loopTime - deltaTime
        time.sleep(timeRemaining)


if __name__ == '__main__':
    playGame([
        Player(np.array((750.0, 350.0)), 75, 100000, 'Andreas', 'blue', SimpleBrain()),
        Player(np.array((650.0, 150.0)), 65, 150000, 'Max', 'blue', SimpleBrain()),
        Player(np.array((50.0, 350.0)), 65, 100000, 'Michael', 'red', SimpleBrain()),
        Player(np.array((150.0, 150.0)), 75, 200000, 'Julian', 'red', SimpleBrain())
    ])
