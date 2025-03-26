import pygame

DRAWABLE_DEFAULT_COLOR = (255, 255, 255)


class Drawable:

    def __init__(self, x: int, y: int, width: int, height: int, color=DRAWABLE_DEFAULT_COLOR):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw_on(self, surface: pygame.Surface) -> None:
        surface.blit(self.surface, self.rect)
