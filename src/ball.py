import pygame

from board import Board
from drawable import Drawable
from pong_game import FPS

BALL_DEFAULT_RADIUS = 20
BALL_DEFAULT_COLOR = (255, 10, 0)
BALL_START_SPEED = 3


class Ball(Drawable):

    def __init__(self, x: int, y: int, radius: int = BALL_DEFAULT_RADIUS, color=BALL_DEFAULT_COLOR,
                 speed: int = BALL_START_SPEED):
        super().__init__(x, y, radius, radius, color)
        self.x_speed = speed
        self.y_speed = speed
        self.start_speed = speed
        self.start_x = x
        self.start_y = y
        self.last_collision = 0
        self.draw_rect = pygame.Rect(0, 0, self.width, self.height)
        self.draw_ball()

    def bounce_x(self) -> None:
        self.x_speed *= -1

    def bounce_y(self) -> None:
        self.y_speed *= -1

    def bounce_y_power(self) -> None:
        self.x_speed *= 1.1
        self.y_speed *= 1.1
        self.bounce_y()
        self.draw_ball()

    def reset(self) -> None:
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.x_speed = self.start_speed
        self.y_speed = self.start_speed
        self.bounce_y()

    def move(self, board: Board, *args) -> None:
        self.rect.x += round(self.x_speed)
        self.rect.y += round(self.y_speed)

        if self.rect.x < 0 or self.rect.x > (board.surface.get_width() - self.rect.width):
            self.bounce_x()

        if self.rect.y < 0 or self.rect.y > (board.surface.get_height() - self.rect.height):
            self.reset()

        timestamp = pygame.time.get_ticks()
        if (timestamp - self.last_collision) < (FPS * 4):
            return

        for racket in args:
            if self.rect.colliderect(racket.rect):
                self.last_collision = pygame.time.get_ticks()
                if ((self.rect.right < racket.rect.left + racket.rect.width // 4)
                        or (self.rect.left > racket.rect.right - racket.rect.width // 4)):
                    self.bounce_y_power()
                else:
                    self.bounce_y()

    def draw_ball(self):
        pygame.draw.ellipse(self.surface, self.color, self.draw_rect)
