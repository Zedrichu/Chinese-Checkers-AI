from functools import cache, cached_property
from typing import Tuple, List, Iterable

import numpy as np


@cache
def _top_right_corner_coords(triangle_size: int, board_size: int) -> np.ndarray:
    """
    Returns the coordinates of the top-right corner of the board.
    :return: list of coordinate pairs
    """
    res = []
    for i in range(triangle_size):
        for j in range(triangle_size):
            if i + j < triangle_size:
                res.append((i, board_size - 1 - j))
    corner = (0, board_size - 1)
    res.sort(key=lambda p: (p[0] - corner[0]) ** 2 + (p[1] - corner[1]) ** 2)
    return np.array(res)


@cache
def _bot_left_corner_coords(triangle_size: int, board_size: int) -> np.ndarray:
    """
    Returns the coordinates of the bottom-left corner of the board.
    :return: list of coordinate pairs
    """
    res = []
    for i in range(triangle_size):
        for j in range(triangle_size):
            if i + j < triangle_size:
                res.append((board_size - 1 - i, j))
    corner = (board_size - 1, 0)
    res.sort(key=lambda p: (p[0] - corner[0]) ** 2 + (p[1] - corner[1]) ** 2)
    return np.array(res)


class Board:
    def __init__(self, triangle_size: int, initialised=True):
        self.triangle_size = triangle_size
        self.board_size = triangle_size * 2 + 1
        self.matrix = np.zeros((self.board_size, self.board_size), dtype=int)
        self.corner_triangles = [_bot_left_corner_coords(self.triangle_size, self.board_size),
                                 _top_right_corner_coords(self.triangle_size, self.board_size)]
        if initialised:
            self.init_board()

    def init_board(self):
        """
        Initializes the board with the triangular matrices for each player at opposite corners.
        """
        # for i in range(self.triangle_size):
        #     for j in range(self.triangle_size):
        #         # Define small triangular matrix function
        #         #   with dimensions triangle_size • triangle_size
        #         if j + i < self.triangle_size:
        #             # Translate triangular matrix bottom-left corner
        #             self.place_pegs(1, [(self.board_size - 1 - i, j)])
        #             # Translate triangular matrix top-right corner
        #             self.place_pegs(2, [(i, self.board_size - 1 - j)])
        self.matrix[self.corner_triangles[0][:, 0], self.corner_triangles[0][:, 1]] = 1
        self.matrix[self.corner_triangles[1][:, 0], self.corner_triangles[1][:, 1]] = 2

    def adjacent_cells(self, src: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns a list of diamond-adjacent cells to the specific cell.
        :param src: the coordinate pair of the source cell
        :return: list of diamond-adjacent cell coordinate pairs
        """
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == -1 and j == 1 or i == 1 and j == -1:
                    continue
                dest = src[0] + i, src[1] + j
                if self.within_bounds(dest):
                    yield dest

    def is_cornered_pegs(self, corner: str) -> bool:
        """
        Checks if the corner is filled with pegs of any type.
        :param corner: string indicating the corner to be checked ('bottom' or 'top')
        :return: boolean value
        """
        if corner == 'bottom':
            np_corner = _bot_left_corner_coords(self.triangle_size, self.board_size)
        else:  # corner == 'top'
            np_corner = _top_right_corner_coords(self.triangle_size, self.board_size)
        return np.all(self.matrix[np_corner[:, 0], np_corner[:, 1]] != 0)

    def is_cornered_with(self, corner: str, value: int) -> bool:
        """
        Checks if the corner is filled with pegs of a specific value.
        :param corner: string indicating the corner to be checked ('bottom' or 'top')
        :param value: specific value to be checked for in the matrix
        :return: boolean value
        """
        if corner == 'bottom':
            np_corner = _bot_left_corner_coords(self.triangle_size, self.board_size)
        else:  # corner == 'top'
            np_corner = _top_right_corner_coords(self.triangle_size, self.board_size)

        return np.all(self.matrix[np_corner[:, 0], np_corner[:, 1]] == value)

    def is_top_right_terminal(self) -> bool:
        """
        Checks if the top-right corner is terminal for player 1.
        :return:
        """
        return (self.is_cornered_pegs('top') and  # Initial config has TOP with 2's
                not self.is_cornered_with('top', 2))

    def is_bot_left_terminal(self) -> bool:
        """
        Checks if the bottom-left corner is terminal for player 2.
        :return: boolean value
        """
        return (self.is_cornered_pegs('bottom') and  # Initial config has BOTTOM with 1's
                not self.is_cornered_with('bottom', 1))

    def move(self, initial_pos: Tuple[int, int], path: Tuple[int, int]):
        current_x, current_y = initial_pos
        x, y = path

        if not self.within_bounds(path):
            raise Exception(f'Coordinates out of bound: {path}')

        tmp = self.matrix[x][y]
        self.matrix[x][y] = self.matrix[current_x][current_y]
        self.matrix[current_x][current_y] = tmp

    def within_bounds(self, coords: Tuple[int, int]) -> bool:
        """
        Checks if the coordinates are within the bounds of the board.
        :param coords: the coordinate pair to be checked
        :return: boolean value indicating if the coordinates are within the bounds of the board
        """
        return 0 <= coords[0] < self.board_size and 0 <= coords[1] < self.board_size

    def place_pegs(self, player_id: int, destinations: Iterable[Tuple[int, int]]):
        for dest in destinations:
            self.matrix[dest] = player_id

    def __str__(self):
        separator = '  '
        text = ' ' + separator + separator.join((str(i) for i in range(self.matrix.shape[0])))
        for i, row in enumerate(self.matrix):
            text += '\n' + str(i) + separator + separator.join(str(x) if x else '.' for x in row)
        return text

    def __copy__(self):
        new_board = Board(self.triangle_size)
        new_board.matrix = np.copy(self.matrix)
        return new_board
