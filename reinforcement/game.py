import pygame
import numpy as np
from reinforcement.helpers import collides, elasticCollision, outside, stop, bounce, touchesEdge
from reinforcement.classes import Field, Ball, Player, Goal, Counter, Timer
from reinforcement.brains import SimpleBrain, RandomBrain, PlayerBrain
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
    counter = Counter()
    timer = Timer(60)
    goalRed = Goal('red', (0, SCREEN_HEIGHT / 2))
    goalBlue = Goal('blue', (SCREEN_WIDTH, SCREEN_HEIGHT / 2))
    ball = Ball((400, 250), 1)
    objects = [field, counter, timer, ball, goalBlue, goalRed] + players
    
    running = True
    fps = 20.0
    loopTime = 1.0 / fps
    deltaTime = 0.1
    while running:
        startTime = time.time()

        # Step 1: handle events
        for event in pygame.event.get():
            playerBrain.handleEvent(event)

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
        if collides(ball, goalRed):
            counter.increaseScore('blue')
            ballInMiddle(ball)
        if collides(ball, goalBlue):
            counter.increaseScore('red')
            ballInMiddle(ball)
        for obj in objects:
            obj.update(deltaTime, objects)
        
        # Step 3: render
        screen.fill((0, 0, 0))
        for obj in objects:
            obj.render(screen)
        pygame.display.flip()

        # Step 4: sleep
        endTime = time.time()
        deltaTime = endTime - startTime
        timeRemaining = loopTime - deltaTime
        if timeRemaining > 0.00001:
            time.sleep(timeRemaining)

        # Step 5: stopcondition
        if timer.seconds < 0.0:
            running = False


if __name__ == '__main__':
    playerBrain = PlayerBrain()
    playGame([
        Player(np.array((750.0, 350.0)), 75, 500000, 400, 'Andreas', 'blue', SimpleBrain()),
        Player(np.array((650.0, 150.0)), 65, 500000, 600, 'Max', 'blue', SimpleBrain()),
        Player(np.array((50.0, 350.0)), 65, 500000, 500, 'Michael', 'red', playerBrain),
        Player(np.array((150.0, 150.0)), 75, 500000, 400, 'Julian', 'red', SimpleBrain())
    ])
