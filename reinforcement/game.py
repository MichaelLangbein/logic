import pygame
import numpy as np
from reinforcement.helpers import intersects, elasticCollision, outside, stop, bounce
from reinforcement.classes import Field, Ball, Player
from reinforcement.brains import SimpleBrain



def playGame(players):
    pygame.init()

    screen = pygame.display.set_mode([800, 500])
    field = Field()
    ball = Ball((400, 250), 1)
    objects = [field, ball] + players

    running = True
    while running:

        # Step 1: handle events
        for event in pygame.event.get():
            pass

        # Step 2: handle logic
        for player in players:
            if intersects(player, ball):
                elasticCollision(player, ball)
            if outside(player, field):
                stop(player, field)
        if outside(ball, field):
            bounce(ball, field)
        for obj in objects:
            obj.update(0.05, objects)

        # Step 3: render
        screen.fill((0, 0, 0))
        for obj in objects:
            obj.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    playGame([
        Player(np.array((700, 250)), 85, 100, 'Andreas', 'blue', SimpleBrain()),
        Player(np.array((100, 250)), 65, 100, 'Michael', 'red', SimpleBrain())
    ])
