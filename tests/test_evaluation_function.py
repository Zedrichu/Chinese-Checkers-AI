import unittest
import numpy as np

from game_problem.ChineseCheckers import ChineseCheckers
from players.MinimaxAIPlayer import MinimaxAIPlayer


class TestEvaluationFunction(unittest.TestCase):
    def test_utility_on_terminal(self):
        sut = ChineseCheckers(2)
        ai = MinimaxAIPlayer(sut, 2, 1)
        state = sut.initial_state
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
