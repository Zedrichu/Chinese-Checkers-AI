import unittest

import numpy as np
from typing import Optional
from game.Step import Step
from game.Board import Board
from parameterized import parameterized


class TestStep(unittest.TestCase):
    @parameterized.expand([
        (2, 3), (3, 2), (3, 4),
        (4, 3), (2, 2), (4, 4),
        (2, 4, None), (4, 2, None)
    ])
    def test_center_empty_crawls(self, i, j, expected: Optional[int] = Step.CRAWL):
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
        self.assertEqual(Step.validate_head(board, (3, 3), (i, j)), expected)

