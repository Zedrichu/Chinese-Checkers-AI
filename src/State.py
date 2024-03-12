from dataclasses import dataclass
import numpy as np
from Board import Board


@dataclass
class State:
    board: Board
    player: int
    mode: int
    peg: tuple

    def __str__(self):
        return f"board:\n {self.board} player: {self.player} mode: {self.mode} peg: {self.peg}"

    def __eq__(self, other):
        return (self.player == other.player and self.mode == other.mode
                and self.peg == other.peg and np.array_equal(self.board.matrix, other.board.matrix))