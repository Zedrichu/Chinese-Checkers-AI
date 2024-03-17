import unittest
import numpy as np
from parameterized import parameterized

from game.Board import Board
from game.State import State
from game_problem.ChineseCheckers import ChineseCheckers
from game_problem.Heuristic import average_manhattan_to_corner, AverageManhattanToCornerHeuristic, Heuristic, \
    SumOfPegsInCornerHeuristic, AverageEuclideanToCornerHeuristic, MaxManhattanToCornerHeuristic, NoneHeuristic
from players.MinimaxAIPlayer import MinimaxAIPlayer


class TestEvaluationFunction(unittest.TestCase):
    def test_utility_on_terminal(self):
        sut = ChineseCheckers(2)
        ai = MinimaxAIPlayer(sut, 2, 1, heuristic=NoneHeuristic())
        state = sut.initial_state()
        state.board.matrix = np.array([
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [2, 0, 0, 0, 0],
            [2, 2, 0, 0, 0],
        ])

        self.assertTrue(sut.utility(state, player=2) == 1)  # Player 2 wins
        self.assertTrue(sut.utility(state, player=1) == -1)  # Player 1 loses

        # Situation is better for player 2
        self.assertTrue(ai.eval_state(state, player=1) < ai.eval_state(state, player=2))

    @parameterized.expand([
        AverageManhattanToCornerHeuristic(),
        AverageEuclideanToCornerHeuristic(),
        MaxManhattanToCornerHeuristic(),
    ])
    def test_payoff_on_random_states(self, heuristic: Heuristic):
        state1 = State(Board(2, matrix=np.array([
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [2, 0, 0, 2, 0],
            [2, 0, 0, 0, 0],
        ])))
        state2 = State(Board(2, matrix=np.array([
            [0, 0, 0, 0, 1],
            [0, 0, 0, 2, 1],
            [0, 0, 0, 1, 0],
            [2, 0, 0, 0, 0],
            [2, 0, 0, 0, 0],
        ])))

        eval1 = heuristic.eval(state1, player=2)
        eval2 = heuristic.eval(state2, player=2)

        self.assertGreater(eval1, eval2)

    @parameterized.expand([
        AverageManhattanToCornerHeuristic(),
        AverageEuclideanToCornerHeuristic(),
    ])
    def test_payoff_on_random_states2(self, heuristic: Heuristic):
        state1 = State(Board(3, matrix=np.array([
            [0, 0, 0, 2, 2, 0, 2],
            [0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
        ])))
        state2 = State(Board(3, matrix=np.array([
            [0, 0, 0, 0, 2, 2, 2],
            [0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
        ])))

        eval1 = heuristic.eval(state1, player=2)
        eval2 = heuristic.eval(state2, player=2)
        self.assertGreater(eval1, eval2)

    def test_avg_manhattan_on_state(self):
        state = State(Board(2, matrix=np.array([
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [2, 0, 0, 0, 0],
            [2, 2, 0, 0, 0],
        ])))

        avg_manhattan = average_manhattan_to_corner(state.board, 1)
        avg_manhattan2 = average_manhattan_to_corner(state.board, 2)

        self.assertTrue(avg_manhattan > avg_manhattan2)

    def test_avg_manhattan_on_random_state(self):
        state1 = State(Board(2, matrix=np.array([
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [2, 0, 0, 2, 0],
            [2, 0, 0, 0, 0],
        ])))
        state2 = State(Board(2, matrix=np.array([
            [0, 0, 0, 0, 1],
            [0, 0, 0, 2, 1],
            [0, 0, 0, 1, 0],
            [2, 0, 0, 0, 0],
            [2, 0, 0, 0, 0],
        ])))

        avg_manhattan1 = average_manhattan_to_corner(state1.board, 2)
        avg_manhattan2 = average_manhattan_to_corner(state2.board, 2)
        self.assertTrue(avg_manhattan1 < avg_manhattan2)
