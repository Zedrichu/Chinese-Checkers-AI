import unittest

from Action import Action
from Board import Board
from ChineseCheckers import ChineseCheckers
from Step import Step


class TestTerminalState(unittest.TestCase):
    def test_actions_should_detect_moves_to_adjacent_cells(self):
        """
           0  1  2  3  4
        0  .  .  .  .  .
        1  .  x  x  .  .
        2  .  x  1  x  .
        3  .  .  x  x  .
        4  .  .  .  .  .
        """
        board = Board(triangle_size=2, initialised=False)
        board.place_pegs(player_id=1, destinations=[(2, 2)])
        sut = ChineseCheckers()
        state = sut.initial_state
        state.board = board

        actions = list(sut.actions(state))

        self.assertIn(Action((2, 2), (1, 1), Step.CRAWL), actions)
        self.assertIn(Action((2, 2), (1, 2), Step.CRAWL), actions)
        self.assertIn(Action((2, 2), (2, 1), Step.CRAWL), actions)
        self.assertIn(Action((2, 2), (2, 3), Step.CRAWL), actions)
        self.assertIn(Action((2, 2), (3, 2), Step.CRAWL), actions)
        self.assertIn(Action((2, 2), (3, 3), Step.CRAWL), actions)
        self.assertEqual(len(actions), 6)

    def test_actions_should_detect_moves_to_adjacent_cells_when_the_cells_are_empty(self):
        """
           0  1  2  3  4
        0  .  .  .  .  .
        1  .  1  x  .  .
        2  .  x  1  x  .
        3  .  .  x  x  .
        4  .  .  .  .  .
        """
        board = Board(triangle_size=2, initialised=False)
        board.place_pegs(player_id=1, destinations=[(1, 1), (2, 2)])
        sut = ChineseCheckers()
        state = sut.initial_state
        state.board = board

        actions = list(sut.actions(state))

        # Verify that there is no move into an occupied cell
        self.assertNotIn(Action((2, 2), (1, 1), Step.CRAWL), actions)

    def test_actions_should_detect_jumps(self):
        """
           0  1  2  3  4
        0  x  .  x  .  .
        1  .  2  2  .  .
        2  x  2  1  2  x
        3  .  .  2  2  .
        4  .  .  x  .  x
        """
        board = Board(triangle_size=2, initialised=False)
        board.place_pegs(1, [(2, 2)])
        board.place_pegs(2, [(1, 1), (1, 2), (2, 1), (2, 3), (3, 2), (3, 3)])
        sut = ChineseCheckers()
        state = sut.initial_state
        state.board = board

        actions = list(sut.actions(state))

        self.assertIn(Action((2, 2), (0, 0), Step.JUMP), actions)
        self.assertIn(Action((2, 2), (0, 2), Step.JUMP), actions)
        self.assertIn(Action((2, 2), (2, 0), Step.JUMP), actions)
        self.assertIn(Action((2, 2), (2, 4), Step.JUMP), actions)
        self.assertIn(Action((2, 2), (4, 2), Step.JUMP), actions)
        self.assertIn(Action((2, 2), (4, 4), Step.JUMP), actions)
        self.assertEqual(len(actions), 6)
