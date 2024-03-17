import numpy as np

from dataclasses import dataclass
from typing import Optional, Tuple

from game.Step import Step
from game.Board import Board


@dataclass
class State:
    """
    Class that represents the state of the game
    """
    board: Board  # the current board object
    player: int = 1  # the player index to move
    mode: int = Step.END  # the mode of the last action applied
    peg: Tuple[Optional[int], Optional[int]] = (None, None)  # the peg that was moved in the last action

    def __str__(self):
        return f"board:\n{self.board}\nplayer: {self.player} mode: {self.mode} peg: {self.peg}"

    def __eq__(self, other):
        return (self.player == other.player and self.mode == other.mode
                and self.peg == other.peg and np.array_equal(self.board.matrix, other.board.matrix))

    def __hash__(self):
        return hash((bytes(self.board.matrix), self.player, self.mode, self.peg))
