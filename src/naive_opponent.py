from ball import Ball
from board import Board
from player import Player
from racket import Racket


class NaiveOpponent(Player):

    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(NaiveOpponent, self).__init__(racket, ball, board)

    def act(self, x_diff: int, y_diff: int) -> None:
        x_cent = self.ball.rect.centerx
        self.move(x_cent)
