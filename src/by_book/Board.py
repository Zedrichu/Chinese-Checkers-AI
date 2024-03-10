from functools import cached_property
from typing import Iterable, Tuple, List

import numpy as np


class Board:
    def __init__(self, triangle_size: int, initialised=True):
        self.triangle_size = triangle_size
        self.board_size = triangle_size * 2 + 1
        self.matrix = np.zeros((self.board_size, self.board_size), dtype=int)

        if initialised:
            self.init_board()

    def init_board(self):
        for i in range(self.triangle_size):
            for j in range(self.triangle_size):
                if j + i < self.triangle_size:
                    # Translate triangular matrix bottom-left corner
                    self.place_peg(0, (self.board_size - 1 - i, j))
                    # Translate triangular matrix top-right corner
                    self.place_peg(1, (i, self.board_size - 1 - j))

    def move(self, src: Tuple[int, int], dest: Tuple[int, int]):
        tmp = self.matrix[src]
        self.matrix[src] = 0
        self.matrix[dest] = tmp

    def place_peg(self, player_id: int, dest: Tuple[int, int]):
        self.matrix[dest] = player_id + 1

    def place_pegs(self, player_id: int, destinations: Iterable[Tuple[int, int]]):
        for dest in destinations:
            self.place_peg(player_id, dest)

    def is_bound(self, coordinate: Tuple[int, int]) -> bool:
        """
        Verify if the coordinate is within the limits of the board.
        """
        if coordinate[0] < 0 or coordinate[0] >= self.board_size:
            return False
        if coordinate[1] < 0 or coordinate[1] >= self.board_size:
            return False
        return True

    @cached_property
    def _top_corner_coordinates(self) -> Iterable[Tuple[int, int]]:
        result = []
        for i in range(self.triangle_size):
            for j in range(self.triangle_size):
                if j + i < self.triangle_size:
                    result.append((i, self.board_size - 1 - j))
        return result

    @cached_property
    def _bottom_corner_coordinates(self) -> List[Tuple[int, int]]:
        result = []
        for i in range(self.triangle_size):
            for j in range(self.triangle_size):
                if j + i < self.triangle_size:
                    result.append((self.board_size - 1 - i, j))
        return result

    def top_is_filled(self) -> bool:
        return all(self.matrix[ij] != 0 for ij in self._top_corner_coordinates)

    def bottom_is_filled(self) -> bool:
        return all(self.matrix[ij] != 0 for ij in self._bottom_corner_coordinates)

    def top_is_filled_with(self, value: int) -> bool:
        return all(self.matrix[ij] == value for ij in self._top_corner_coordinates)

    def bottom_is_filled_with(self, value: int) -> bool:
        return all(self.matrix[ij] == value for ij in self._bottom_corner_coordinates)

    def __str__(self):
        separator = '  '
        text = ' ' + separator + separator.join((str(i) for i in range(self.matrix.shape[0])))
        for i, row in enumerate(self.matrix):
            text += '\n' + str(i) + separator + separator.join(str(x) if x else '.' for x in row)
        return text
