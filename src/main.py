# Based on https://python101.readthedocs.io/pl/latest/pygame/pong/#

from fuzzy_player import FuzzyPlayer
from naive_opponent import NaiveOpponent
from pong_game import PongGame


def main():
    # game = PongGame(NaiveOpponent, HumanPlayer)
    game = PongGame(NaiveOpponent, FuzzyPlayer)
    game.run()


if __name__ == "__main__":
    main()
