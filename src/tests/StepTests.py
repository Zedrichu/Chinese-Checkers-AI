import unittest

import numpy as np
from typing import Tuple
from src.Step import Step
from src.Board import Board
from parameterized import parameterized


class StepTests(unittest.TestCase):
    @parameterized.expand([
        (2, 3), (3, 2), (3, 4),
        (4, 3), (2, 2), (4, 4),
        (2, 4, False), (4, 2, False)
    ])
    def test_center_empty_crawls(self, i, j, expected=True):
        board = Board(3)
        board.matrix = np.array(
            [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             ]
        )
        self.assertEqual(Step.validate_crawl(board, (3, 3), (i, j)), expected)


if __name__ == '__main__':
    unittest.main()
