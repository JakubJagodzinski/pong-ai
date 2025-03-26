from ball import Ball
from board import Board
from player import Player
from racket import Racket


class HumanPlayer(Player):

    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(HumanPlayer, self).__init__(racket, ball, board)

    def move_manual(self, x: int) -> None:
        self.move(x)
