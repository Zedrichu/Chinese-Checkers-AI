from typing import Tuple, Iterable

from by_book.Board import Board


def list_adjacent_cells(board: Board, target: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
    """
    List all adjacent coordinates around a given target as if the board was a diamond.
    For the following board, 'x' represents the returned coordinates.
       0  1  2  3  4
    0  .  .  .  .  .
    1  .  .  x  x  .
    2  .  x  1  x  .
    3  .  x  x  .  .
    4  .  .  .  .  .
    """
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == -1 and j == -1 or i == 1 and j == 1:
                continue

            coordinate = target[0] + i, target[1] + j
            if board.is_bound(coordinate):
                yield coordinate
