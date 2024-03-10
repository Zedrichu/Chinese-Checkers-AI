import unittest

from by_book.Board import Board
from parameterized import parameterized


class BoardTests(unittest.TestCase):
    def test_filled_on_default_board(self):
        sut = Board(triangle_size=5)
        self.assertTrue(sut.bottom_is_filled())
        self.assertTrue(sut.bottom_is_filled_with(1))

        self.assertTrue(sut.top_is_filled())
        self.assertTrue(sut.top_is_filled_with(2))

    @parameterized.expand([
        (3, 0),
        (4, 0), (4, 1)
    ])
    def test_non_filled_bottom(self, i, j):
        """
           0  1  2  3  4
        0  .  .  .  2  2
        1  .  .  .  .  2
        2  .  .  .  .  .
        3  1  .  .  .  .
        4  1  1  .  .  .
        """
        sut = Board(triangle_size=2)
        sut.matrix[i, j] = 0
        self.assertFalse(sut.bottom_is_filled())

    @parameterized.expand([
        (0, 3), (0, 4),
        (1, 4)
    ])
    def test_non_filled_top(self, i, j):
        """
           0  1  2  3  4
        0  .  .  .  2  2
        1  .  .  .  .  2
        2  .  .  .  .  .
        3  1  .  .  .  .
        4  1  1  .  .  .
        """
        sut = Board(triangle_size=2)
        sut.matrix[i, j] = 0
        self.assertFalse(sut.top_is_filled())


if __name__ == '__main__':
    unittest.main()
