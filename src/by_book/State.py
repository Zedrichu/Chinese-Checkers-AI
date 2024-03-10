from dataclasses import dataclass

import numpy as np

from State import State
from by_book.Board import Board


@dataclass(frozen=True)
class State:
    board: Board
    player_to_move: int = 0

    def __str__(self):
        return f'Player to move: {self.player_to_move}\n{self.board}'

    def __eq__(self, other: State):
        return self.player_to_move == other.player_to_move and np.array_equal(self.board.matrix, other.board.matrix)
