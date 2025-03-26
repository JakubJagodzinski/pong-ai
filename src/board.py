import pygame

BACKGROUND_COLOR = (0, 0, 0)


class Board:

    def __init__(self, width: int, height: int):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("AI Fundamentals - PongGame")

    def draw(self, *args):
        self.surface.fill(BACKGROUND_COLOR)

        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()
