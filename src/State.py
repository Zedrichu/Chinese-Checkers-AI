from dataclasses import dataclass
from Board import Board


@dataclass
class State:
    board: Board
    player: int
    mode: int
