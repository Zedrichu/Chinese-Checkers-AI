from dataclasses import dataclass
from board import Board


@dataclass
class State:
    board: Board
    player: int
