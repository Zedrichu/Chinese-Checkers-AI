import unittest

from game.Board import Board
from game_problem.Heuristic import decide_goal_corner_coordinates


class TestDecideGoalCorner(unittest.TestCase):

    def test_initial_state(self):
        """
           0  1  2  3  4  5  6
        0  .  .  .  .  2  2  2
        1  .  .  .  .  .  2  2
        2  .  .  .  .  .  .  2
        3  .  .  .  .  .  .  .
        4  1  .  .  .  .  .  .
        5  1  1  .  .  .  .  .
        6  1  1  1  .  .  .  .
        """
        board = Board(3)
        coords = decide_goal_corner_coordinates(board, 1)
        self.assertEqual((coords[0], coords[1]), (0, 6))

    def test_top_right_almost_terminal(self):
        """
           0  1  2  3  4  5  6
        0  .  .  .  .  2  2  2
        1  .  .  .  .  .  2  2
        2  .  .  .  .  .  2  .
        3  .  .  .  .  .  .  .
        4  1  .  .  .  .  .  .
        5  1  1  .  .  .  .  .
        6  1  1  1  .  .  .  .
        """
        board = Board(3)
        board.place_pegs(2, [(2, 6)])
        board.move((2, 6), (2, 5))
        coords = decide_goal_corner_coordinates(board, 1)
        self.assertEqual((coords[0], coords[1]), (2, 6))

    def test_top_right_almost_terminal2(self):
        """
           0  1  2  3  4  5  6
        0  2  .  .  .  2  2  2
        1  .  .  .  .  .  2  .
        2  .  .  .  .  .  .  2
        3  .  .  .  .  .  .  .
        4  1  .  .  .  .  .  .
        5  1  1  .  .  .  .  .
        6  1  1  1  .  .  .  .
        """
        board = Board(3)
        board.move((1, 6), (0, 0))
        coords = decide_goal_corner_coordinates(board, 1)
        self.assertEqual((coords[0], coords[1]), (1, 6))

    def test_bottom_left_almost_terminal(self):
        """
           0  1  2  3  4  5  6
        0  1  .  .  .  2  2  2
        1  .  .  .  .  .  2  2
        2  .  .  .  .  .  .  2
        3  .  .  .  .  .  .  .
        4  1  .  .  .  .  .  .
        5  1  1  .  .  .  .  .
        6  1  .  1  .  .  .  .
        """
        board = Board(3)
        board.move((6, 1), (0, 0))
        coords = decide_goal_corner_coordinates(board, 2)
        self.assertEqual((coords[0], coords[1]), (6, 1))

    def test_bottom_left_almost_terminal2(self):
        """
           0  1  2  3  4  5  6
        0  1  .  .  .  2  2  2
        1  .  .  .  .  .  2  2
        2  .  .  .  .  .  .  2
        3  .  .  .  .  .  .  .
        4  1  .  .  .  .  .  .
        5  .  1  .  .  .  .  .
        6  1  1  1  .  .  .  .
        """
        board = Board(3)
        board.move((5, 0), (0, 0))
        coords = decide_goal_corner_coordinates(board, 2)
        self.assertEqual((coords[0], coords[1]), (5, 0))