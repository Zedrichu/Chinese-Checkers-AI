from dataclasses import dataclass
from src.Board import Board


@dataclass
class State:
    board: Board
    player: int
    mode: int
    peg: tuple
