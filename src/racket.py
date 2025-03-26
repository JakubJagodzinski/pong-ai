from board import Board
from drawable import Drawable

RACKET_WIDTH = 80
RACKET_HEIGHT = 20
RACKET_DEFAULT_COLOR = (255, 255, 255)
RACKET_DEFAULT_MAX_SPEED = 10


class Racket(Drawable):

    def __init__(self, x: int, y: int, width: int = RACKET_WIDTH, height: int = RACKET_HEIGHT,
                 color=RACKET_DEFAULT_COLOR, max_speed: int = RACKET_DEFAULT_MAX_SPEED):
        super(Racket, self).__init__(x, y, width, height, color)
        self.max_speed = max_speed
        self.surface.fill(color)

    def move(self, x: int, board: Board) -> None:
        delta = x - self.rect.x
        delta = self.max_speed if delta > self.max_speed else delta
        delta = -self.max_speed if delta < -self.max_speed else delta
        delta = 0 if (self.rect.x + delta) < 0 else delta
        delta = (0 if (self.rect.x + self.width + delta) > board.surface.get_width() else delta)
        self.rect.x += delta
