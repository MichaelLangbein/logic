import pygame





class Player:
    def __init__(self, name, number, weight):
        self.name = name
        self.number = number
        self.weight = weight

    def __repr__(self):
        return f"{self.name} - {self.number}"


class Renderable:
    def render(self, field):
        raise Exception('Not yet implemented!')

    def update(self):
        raise Exception('Not yet implemented!')


class Ball(Renderable):
    def __init__(self, weight):
        self.weight = weight
        self.field = pygame.image.load('reinforcement/assets/soccerball.png')

    def render(self, screen):
        screen.blit(self.field, self.field.get_rect())

    def update(self):
        pass

    def __repr__(self):
        return 'ball'


class Field(Renderable):
    def __init__(self):
        self.field = pygame.image.load('reinforcement/assets/field.png')

    def render(self, screen):
        screen.blit(self.field, self.field.get_rect())

    def update(self):
        pass

    def __repr__(self):
        return 'field'


def playGame(players):
    pygame.init()
    screen = pygame.display.set_mode([800, 500])
    objects = [Field(), Ball(1)] + players

    while True:

        # Step 1: handle events
        for event in pygame.event.get():
            pass

        # Step 2: handle logic
        for obj in objects:
            obj.update()

        # Step 3: render
        screen.fill((0, 0, 0))
        for obj in objects:
            obj.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    playGame([])
