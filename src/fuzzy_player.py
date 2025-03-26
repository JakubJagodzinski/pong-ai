import numpy as np
import skfuzzy as fuzz
from matplotlib import pyplot as plt
from skfuzzy import control as fuzzcontrol

from ball import Ball
from board import Board
from player import Player
from pong_game import BOARD_WIDTH, BOARD_HEIGHT
from racket import Racket

MAMDAMI_RULES = 'mamdami'
TSK_RULES = 'tsk'
RULES_TYPE = MAMDAMI_RULES

X_DIST = 'x_dist'
X_LEFT_FAR = 'x_left_far'
X_LEFT_NEAR = 'x_left_near'
X_LEFT_SIDE = 'x_left_side'
X_MIDDLE = 'x_middle'
X_RIGHT_SIDE = 'x_right_side'
X_RIGHT_NEAR = 'x_right_near'
X_RIGHT_FAR = 'x_right_far'
Y_DIST = 'y_dist'
Y_LOW = 'y_low'
Y_MEDIUM = 'y_medium'
Y_HIGH = 'y_high'
VELOCITY = 'velocity'
VELOCITY_FAST_LEFT = 'velocity_fast_left'
VELOCITY_SLOW_LEFT = 'velocity_slow_left'
VELOCITY_STOP = 'velocity_stop'
VELOCITY_SLOW_RIGHT = 'velocity_slow_right'
VELOCITY_FAST_RIGHT = 'velocity_fast_right'


class FuzzyPlayer(Player):

    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(FuzzyPlayer, self).__init__(racket, ball, board)

        self.x_universe = np.arange(-BOARD_WIDTH, BOARD_WIDTH + 1, 1)

        self.x_membership_functions = {
            X_LEFT_FAR: fuzz.trapmf(self.x_universe, [45, 50, 800, 800]),
            X_LEFT_NEAR: fuzz.trimf(self.x_universe, [39, 45, 50]),
            X_LEFT_SIDE: fuzz.trimf(self.x_universe, [19, 30, 40]),
            X_MIDDLE: fuzz.trimf(self.x_universe, [-20, 0, 20]),
            X_RIGHT_SIDE: fuzz.trimf(self.x_universe, [-40, -30, -19]),
            X_RIGHT_NEAR: fuzz.trimf(self.x_universe, [-50, -45, -39]),
            X_RIGHT_FAR: fuzz.trapmf(self.x_universe, [-800, -800, -50, -45])
        }

        x_membership_functions = fuzzcontrol.Antecedent(self.x_universe, X_DIST)
        for membership_function_name, membership_function in self.x_membership_functions.items():
            x_membership_functions[membership_function_name] = membership_function

        y_membership_functions = fuzzcontrol.Antecedent(np.arange(0, BOARD_HEIGHT + 1, 1), Y_DIST)
        y_membership_functions[Y_LOW] = fuzz.trimf(y_membership_functions.universe, [0, 0, 150])
        y_membership_functions[Y_MEDIUM] = fuzz.trimf(y_membership_functions.universe, [100, 175, 250])
        y_membership_functions[Y_HIGH] = fuzz.trimf(y_membership_functions.universe, [175, 400, 400])

        if RULES_TYPE == MAMDAMI_RULES:
            velocity_universe = np.arange(-10, 11, 1)
            velocity_membership_functions = fuzzcontrol.Consequent(velocity_universe, VELOCITY)

            velocity_membership_functions[VELOCITY_FAST_LEFT] = fuzz.trapmf(
                velocity_membership_functions.universe,
                [-10, -10, -10, -9]
            )
            velocity_membership_functions[VELOCITY_SLOW_LEFT] = fuzz.trimf(
                velocity_membership_functions.universe,
                [-9.1, -5, -2]
            )
            velocity_membership_functions[VELOCITY_STOP] = fuzz.trimf(
                velocity_membership_functions.universe,
                [-2.1, 0, 2.1]
            )
            velocity_membership_functions[VELOCITY_SLOW_RIGHT] = fuzz.trimf(
                velocity_membership_functions.universe,
                [2, 5, 9.1]
            )
            velocity_membership_functions[VELOCITY_FAST_RIGHT] = fuzz.trapmf(
                velocity_membership_functions.universe,
                [9, 10, 10, 10]
            )

            self.rules = [
                # -------------------------------- LEFT FAR --------------------------------
                fuzzcontrol.Rule(
                    x_membership_functions[X_LEFT_FAR] & y_membership_functions[Y_LOW],
                    velocity_membership_functions[VELOCITY_FAST_LEFT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_LEFT_FAR] & y_membership_functions[Y_MEDIUM],
                    velocity_membership_functions[VELOCITY_FAST_LEFT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_LEFT_FAR] & y_membership_functions[Y_HIGH],
                    velocity_membership_functions[VELOCITY_FAST_LEFT]
                ),

                # -------------------------------- LEFT NEAR --------------------------------
                fuzzcontrol.Rule(
                    x_membership_functions[X_LEFT_NEAR] & y_membership_functions[Y_LOW],
                    velocity_membership_functions[VELOCITY_FAST_LEFT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_LEFT_NEAR] & y_membership_functions[Y_MEDIUM],
                    velocity_membership_functions[VELOCITY_FAST_LEFT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_LEFT_NEAR] & y_membership_functions[Y_HIGH],
                    velocity_membership_functions[VELOCITY_FAST_LEFT]
                ),

                # -------------------------------- LEFT SIDE --------------------------------
                fuzzcontrol.Rule(
                    x_membership_functions[X_LEFT_SIDE] & y_membership_functions[Y_LOW],
                    velocity_membership_functions[VELOCITY_SLOW_LEFT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_LEFT_SIDE] & y_membership_functions[Y_MEDIUM],
                    velocity_membership_functions[VELOCITY_SLOW_LEFT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_LEFT_SIDE] & y_membership_functions[Y_HIGH],
                    velocity_membership_functions[VELOCITY_FAST_LEFT]
                ),

                # -------------------------------- MIDDLE --------------------------------
                fuzzcontrol.Rule(
                    x_membership_functions[X_MIDDLE] & y_membership_functions[Y_LOW],
                    velocity_membership_functions[VELOCITY_STOP]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_MIDDLE] & y_membership_functions[Y_MEDIUM],
                    velocity_membership_functions[VELOCITY_STOP]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_MIDDLE] & y_membership_functions[Y_HIGH],
                    velocity_membership_functions[VELOCITY_STOP]
                ),

                # -------------------------------- RIGHT SIDE --------------------------------
                fuzzcontrol.Rule(
                    x_membership_functions[X_RIGHT_SIDE] & y_membership_functions[Y_LOW],
                    velocity_membership_functions[VELOCITY_SLOW_RIGHT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_RIGHT_SIDE] & y_membership_functions[Y_MEDIUM],
                    velocity_membership_functions[VELOCITY_SLOW_RIGHT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_RIGHT_SIDE] & y_membership_functions[Y_HIGH],
                    velocity_membership_functions[VELOCITY_FAST_RIGHT]
                ),

                # -------------------------------- RIGHT NEAR --------------------------------
                fuzzcontrol.Rule(
                    x_membership_functions[X_RIGHT_NEAR] & y_membership_functions[Y_LOW],
                    velocity_membership_functions[VELOCITY_FAST_RIGHT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_RIGHT_NEAR] & y_membership_functions[Y_MEDIUM],
                    velocity_membership_functions[VELOCITY_FAST_RIGHT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_RIGHT_NEAR] & y_membership_functions[Y_HIGH],
                    velocity_membership_functions[VELOCITY_FAST_RIGHT]
                ),

                # -------------------------------- RIGHT FAR --------------------------------
                fuzzcontrol.Rule(
                    x_membership_functions[X_RIGHT_FAR] & y_membership_functions[Y_LOW],
                    velocity_membership_functions[VELOCITY_FAST_RIGHT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_RIGHT_FAR] & y_membership_functions[Y_MEDIUM],
                    velocity_membership_functions[VELOCITY_FAST_RIGHT]
                ),
                fuzzcontrol.Rule(
                    x_membership_functions[X_RIGHT_FAR] & y_membership_functions[Y_HIGH],
                    velocity_membership_functions[VELOCITY_FAST_RIGHT]
                )
            ]

            x_membership_functions.view()
            y_membership_functions.view()
            velocity_membership_functions.view()

            self.racket_controller = fuzzcontrol.ControlSystem(self.rules)
            self.racket_simulator = fuzzcontrol.ControlSystemSimulation(self.racket_controller)
        else:
            self.velocity_functions = {
                VELOCITY_FAST_LEFT: lambda x_diff, y_diff: -10 * (abs(x_diff) + y_diff),
                VELOCITY_SLOW_LEFT: lambda x_diff, y_diff: -5 * (abs(x_diff) + y_diff),
                VELOCITY_STOP: lambda x_diff, y_diff: 0,
                VELOCITY_SLOW_RIGHT: lambda x_diff, y_diff: 5 * (abs(x_diff) + y_diff),
                VELOCITY_FAST_RIGHT: lambda x_diff, y_diff: 10 * (abs(x_diff) + y_diff)
            }

            plt.figure()
            for name, membership_function in self.x_membership_functions.items():
                plt.plot(self.x_universe, membership_function, label=name)
            plt.legend()
            plt.show()

            self.racket_controller = None
            self.racket_simulator = None

    def act(self, x_diff: int, y_diff: int) -> None:
        velocity = self.make_decision(x_diff, y_diff)
        self.move(self.racket.rect.x + velocity)

    def make_decision(self, x_diff: int, y_diff: int) -> float:
        if RULES_TYPE == MAMDAMI_RULES:
            self.racket_simulator.input[X_DIST] = x_diff
            self.racket_simulator.input[Y_DIST] = y_diff
            self.racket_simulator.compute()
            velocity = self.racket_simulator.output[VELOCITY]
            return velocity
        else:
            x_membership_degrees = {}
            for membership_function_name, membership_function in self.x_membership_functions.items():
                x_membership_degrees[membership_function_name] = fuzz.interp_membership(
                    self.x_universe,
                    membership_function,
                    x_diff
                )

            velocity_weights = {
                VELOCITY_FAST_LEFT: min(x_membership_degrees[X_LEFT_FAR], 1),
                VELOCITY_SLOW_LEFT: min(x_membership_degrees[X_LEFT_NEAR], 1),
                VELOCITY_STOP: min(x_membership_degrees[X_MIDDLE], 1),
                VELOCITY_SLOW_RIGHT: min(x_membership_degrees[X_RIGHT_NEAR], 1),
                VELOCITY_FAST_RIGHT: min(x_membership_degrees[X_RIGHT_FAR], 1)
            }

            velocity = 0
            weights_sum = 0
            for velocity_name, weight in velocity_weights.items():
                velocity += self.velocity_functions[velocity_name](x_diff, y_diff) * weight
                weights_sum += weight

            if weights_sum == 0:
                return 0

            return velocity / weights_sum
