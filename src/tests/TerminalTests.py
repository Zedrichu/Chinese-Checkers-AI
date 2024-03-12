import unittest

import numpy as np

from ChineseCheckers import ChineseCheckers


class TerminalTests(unittest.TestCase):
    def test_terminal_test_on_initial_state(self):
        sut = ChineseCheckers()
        state = sut.initial_state

        self.assertFalse(sut.terminal_test(state))

        self.assertFalse(sut.terminal_test(state))

    def test_terminal_test_on_initial_state_with_one_cell_moved(self):
        """
           0  1  2  3  4
        0  .  .  .  2  2
        1  .  .  .  .  2
        2  1  .  .  .  .
        3  .  .  .  .  .
        4  1  1  .  .  .
        """
        sut = ChineseCheckers(triangle_size=2)
        state = sut.initial_state
        state.board.move((3, 0), (2, 0))

        self.assertFalse(sut.terminal_test(state))

    def test_terminal_test_on_bottom_corner_filled_with_all_opponents(self):
        sut = ChineseCheckers(triangle_size=2)
        state = sut.initial_state
        state.board.matrix = np.array([
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [2, 0, 0, 0, 0],
            [2, 2, 0, 0, 0],
        ])
        self.assertTrue(sut.terminal_test(state))
        self.assertEqual(sut.utility(state, player=1), -1)

    def test_terminal_test_on_top_corner_filled_with_all_opponents(self):
        sut = ChineseCheckers(triangle_size=2)
        state = sut.initial_state
        state.board.matrix = np.array([
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1],
            [2, 0, 0, 0, 0],
            [2, 0, 0, 0, 0],
            [2, 0, 0, 0, 0],
        ])
        self.assertTrue(sut.terminal_test(state))
        self.assertEqual(sut.utility(state, player=1), 1)
