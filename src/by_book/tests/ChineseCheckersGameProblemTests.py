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

    def test_result_should_apply_move_and_return_new_state(self):
        board = Board(triangle_size=3)
        state = State(board)
        sut = ChineseCheckersGameProblem(initial_state=state)

        new_state = sut.result(state, Action([(4, 0), (3, 0), (2, 1)]))

        self.assertEqual(new_state.player_to_move, 1)

        self.assertEqual(new_state.board.matrix[4, 0], 0)
        self.assertEqual(new_state.board.matrix[3, 0], 0)
        self.assertEqual(new_state.board.matrix[2, 1], 1)

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
        board.place_peg(player_id=0, dest=(2, 2))
        state = State(board)
        sut = ChineseCheckersGameProblem(initial_state=state)

        actions = list(sut.actions(state))

        self.assertIn(Action([(2, 2), (1, 1)]), actions)
        self.assertIn(Action([(2, 2), (1, 2)]), actions)
        self.assertIn(Action([(2, 2), (2, 1)]), actions)
        self.assertIn(Action([(2, 2), (2, 3)]), actions)
        self.assertIn(Action([(2, 2), (3, 2)]), actions)
        self.assertIn(Action([(2, 2), (3, 3)]), actions)
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
        board.place_peg(player_id=0, dest=(2, 2))
        board.place_peg(player_id=0, dest=(1, 1))
        state = State(board)
        sut = ChineseCheckersGameProblem(initial_state=state)

        actions = list(sut.actions(state))

        # Verify that there is no move into an occupied cell
        self.assertNotIn(Action([(2, 2), (1, 1)]), actions)

    def test_actions_should_detect_small_jumps(self):
        """
           0  1  2  3  4
        0  x  .  x  .  .
        1  .  2  2  .  .
        2  x  2  1  2  x
        3  .  .  2  2  .
        4  .  .  x  .  x
        """
        board = Board(triangle_size=2, initialised=False)
        board.place_peg(0, (2, 2))
        board.place_pegs(1, [(1, 1), (1, 2), (2, 1), (2, 3), (3, 2), (3, 3)])
        state = State(board)
        sut = ChineseCheckersGameProblem(initial_state=state)

        actions = list(sut.actions(state))

        self.assertIn(Action([(2, 2), (0, 0)]), actions)
        self.assertIn(Action([(2, 2), (0, 2)]), actions)
        self.assertIn(Action([(2, 2), (2, 0)]), actions)
        self.assertIn(Action([(2, 2), (2, 4)]), actions)
        self.assertIn(Action([(2, 2), (4, 2)]), actions)
        self.assertIn(Action([(2, 2), (4, 4)]), actions)
        self.assertEqual(len(actions), 6)

    def test_actions_should_detect_non_looping_jumps(self):
        """
           0  1  2  3  4  5  6
        0  .  .  .  .  .  .  .
        1  .  x  2  x  2  x  .
        2  .  2  .  2  .  2  .
        3  .  x  .  1  .  x  .
        4  .  2  .  .  .  2  .
        5  .  x  2  x  2  x  .
        6  .  .  .  .  .  .  .
        """
        board = Board(triangle_size=3, initialised=False)
        board.place_peg(0, (3, 3))
        board.place_pegs(1, [(1, 2), (1, 4), (2, 1), (2, 3), (2, 5), (4, 1), (4, 5), (5, 2), (5, 4)])
        state = State(board)
        sut = ChineseCheckersGameProblem(initial_state=state)

        actions = list(sut.actions(state))

        self.assertIn(Action([(3, 3), (1, 3)]), actions)

        # Clockwise starting at (1, 3)
        self.assertIn(Action([(3, 3), (1, 3), (1, 5)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 5), (3, 5)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 5), (3, 5), (5, 5)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 5), (3, 5), (5, 5), (5, 3)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 5), (3, 5), (5, 5), (5, 3), (5, 1)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 5), (3, 5), (5, 5), (5, 3), (5, 1), (3, 1)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 5), (3, 5), (5, 5), (5, 3), (5, 1), (3, 1), (1, 1)]), actions)

        # Anticlockwise starting at (1, 3)
        self.assertIn(Action([(3, 3), (1, 3), (1, 1)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 1), (3, 1)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 1), (3, 1), (5, 1)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 1), (3, 1), (5, 1), (5, 3)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 1), (3, 1), (5, 1), (5, 3), (5, 5)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 1), (3, 1), (5, 1), (5, 3), (5, 5), (3, 5)]), actions)
        self.assertIn(Action([(3, 3), (1, 3), (1, 1), (3, 1), (5, 1), (5, 3), (5, 5), (3, 5), (1, 5)]), actions)

        # 15 jumps and 5 crawls
        self.assertEqual(len(actions), 15 + 5)


if __name__ == '__main__':
    unittest.main()
