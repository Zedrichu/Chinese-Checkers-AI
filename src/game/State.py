import numpy as np

from dataclasses import dataclass
from typing import Optional, Tuple

from game.Step import Step
from game.Board import Board


@dataclass
class State:
    board: Board
    player: int = 1
    mode: int = Step.END
    peg: Tuple[Optional[int], Optional[int]] = (None, None)

    def __str__(self):
        return f"board:\n{self.board}\nplayer: {self.player} mode: {self.mode} peg: {self.peg}"

    def __eq__(self, other):
        return (self.player == other.player and self.mode == other.mode
                and self.peg == other.peg and np.array_equal(self.board.matrix, other.board.matrix))