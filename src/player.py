from ball import Ball
from board import Board
from racket import Racket


class Player:

    def __init__(self, racket: Racket, ball: Ball, board: Board):
        self.ball = ball
        self.racket = racket
        self.board = board

    def move(self, x: int) -> None:
        self.racket.move(x, self.board)

    def move_manual(self, x: int) -> None:
        """
        Do nothing, control is defined in derived classes
        """
        pass

    def act(self, x_diff: int, y_diff: int) -> None:
        """
        Do nothing, control is defined in derived classes
        """
        pass
