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

    @cached_property
    def initial_avg_euclidean(self):
        """
        Returns the average Euclidian distance between the two initial corner triangles
        :return: mean of Euclidian distances
        """
        diffs = self.corner_triangles[0] - [0, self.board_size - 1]
        distances = np.linalg.norm(diffs, axis=1)
        return np.mean(distances)

    def average_euclidean_to_corner(self, player) -> float:
        if player == 1:
            corner = [0, self.board_size - 1]
        else:
            corner = [self.board_size - 1, 0]

        indices = np.argwhere(self.matrix == player)
        distances = np.linalg.norm(indices - corner, axis=1)
        return np.mean(distances)

    def average_manhattan_to_corner(self, player) -> float:
        if player == 1:
            corner = [0, self.board_size - 1]
        else:
            corner = [self.board_size - 1, 0]

        indices = np.argwhere(self.matrix == player)
        distances = np.sum(np.abs(indices - corner), axis=1)
        return np.mean(distances)

    def sum_player_pegs(self, player: int) -> float:
        """
        Returns the sum of pegs in the corner triangles for a specific player.
        :param player:
        :return:
        """
        corner = self.corner_triangles[player - 1]
        return np.sum(self.matrix[corner[:, 0], corner[:, 1]] == player)

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

    def is_top_filled(self) -> bool:
        """
        Checks if the top-right corner of the board is filled with pegs.
        :return: boolean value
        """
        return all(self.matrix[pair] != 0 for pair in _top_right_corner_coords(self.triangle_size, self.board_size))

    def is_bottom_filled(self) -> bool:
        """
        Checks if the bottom-left corner of the board is filled with pegs.
        :return: boolean value
        """
        return all(self.matrix[pair] != 0 for pair in _bot_left_corner_coords(self.triangle_size, self.board_size))

    def is_top_filled_with(self, value: int) -> bool:
        """
        Checks if the top-right corner of the board is filled with pegs of a specific value.
        :param value: value of peg searching for in the top-right corner
        :return: boolean value
        """
        return all(self.matrix[pair] == value for pair in _top_right_corner_coords(self.triangle_size, self.board_size))

    def is_bottom_filled_with(self, value: int) -> bool:
        """
        Checks if the bottom-left corner of the board is filled with pegs of a specific value.
        :param value: value of peg searching for in the bottom-left corner
        :return: boolean value
        """
        return all(self.matrix[pair] == value for pair in _bot_left_corner_coords(self.triangle_size, self.board_size))

    def is_cornered(self, corner: str, value: int) -> bool:
        if corner == 'bottom':
            np_corner = _bot_left_corner_coords(self.triangle_size, self.board_size)
        else:  # corner == 'top'
            np_corner = _top_right_corner_coords(self.triangle_size, self.board_size)

        return np.all(self.matrix[np_corner[:, 0], np_corner[:, 1]] == value)

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
