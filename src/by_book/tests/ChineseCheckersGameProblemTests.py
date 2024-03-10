import unittest

from by_book.Action import Action
from by_book.Board import Board
from by_book.GameProblem import ChineseCheckersGameProblem
from by_book.State import State


class ChineseCheckersGameProblemTests(unittest.TestCase):
    def test_terminal_test_on_initial_state(self):
        board = Board(triangle_size=3)
        state = State(board)
        sut = ChineseCheckersGameProblem(initial_state=state)

        self.assertFalse(sut.terminal_test(state))

    def test_terminal_test_on_initial_state_with_one_cell_moved(self):
        """
           0  1  2  3  4  5  6
        0  .  .  .  .  2  2  2
        1  .  .  .  .  .  2  2
        2  .  .  .  .  .  .  2
        3  1  .  .  .  .  .  .
        4  .  .  .  .  .  .  .
        5  1  1  .  .  .  .  .
        6  1  1  1  .  .  .  .
        """
        board = Board(triangle_size=3)
        board.move((4, 0), (3, 0))
        state = State(board)
        sut = ChineseCheckersGameProblem(initial_state=state)

        self.assertFalse(sut.terminal_test(state))

    def test_terminal_test_on_bottom_corner_filled_with_only_one_opponent(self):
        """
           0  1  2  3  4  5  6
        0  1  .  .  .  .  2  2
        1  .  .  .  .  .  2  2
        2  .  .  .  .  .  .  2
        3  .  .  .  .  .  .  .
        4  2  .  .  .  .  .  .
        5  1  1  .  .  .  .  .
        6  1  1  1  .  .  .  .
        """
        board = Board(triangle_size=3)
        board.move((4, 0), (0, 0))
        board.move((0, 4), (4, 0))
        state = State(board)
        sut = ChineseCheckersGameProblem(initial_state=state)

        self.assertTrue(sut.terminal_test(state))

    def test_terminal_test_on_top_corner_filled_with_only_one_opponent(self):
        """
           0  1  2  3  4  5  6
        0  2  .  .  .  1  2  2
        1  .  .  .  .  .  2  2
        2  .  .  .  .  .  .  2
        3  .  .  .  .  .  .  .
        4  .  .  .  .  .  .  .
        5  1  1  .  .  .  .  .
        6  1  1  1  .  .  .  .
        """
        board = Board(triangle_size=3)
        board.move((0, 4), (0, 0))
        board.move((4, 0), (0, 4))
        state = State(board)
        sut = ChineseCheckersGameProblem(initial_state=state)

        self.assertTrue(sut.terminal_test(state))

    def test_result_should_apply_move(self):
        board = Board(triangle_size=3)
        state = State(board)
        sut = ChineseCheckersGameProblem(initial_state=state)

        new_state = sut.result(state, Action([(4, 0), (3, 0), (2, 1)]))

        self.assertEqual(new_state.player_to_move, 1)

        self.assertEqual(new_state.board.matrix[4, 0], 0)
        self.assertEqual(new_state.board.matrix[3, 0], 0)
        self.assertEqual(new_state.board.matrix[2, 1], 1)


if __name__ == '__main__':
    unittest.main()
