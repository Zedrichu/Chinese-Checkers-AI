from typing import Tuple, List, Iterable
import numpy as np
from functools import cached_property
import pygame


class Board:
    def __init__(self, triangle_size: int):
        self.triangle_size = triangle_size
        self.board_size = triangle_size * 2 + 1
        self.matrix = np.zeros((self.board_size, self.board_size), dtype=int)
        self.init_board()

    def init_board(self):
        """
        Initializes the board with the triangular matrices for each player at opposite corners.
        """
        for i in range(self.triangle_size):
            for j in range(self.triangle_size):
                # Define small triangular matrix function
                #   with dimensions triangle_size • triangle_size
                if j + i < self.triangle_size:
                    # Translate triangular matrix bottom-left corner
                    self.matrix[self.board_size - 1 - i][j] = 1
                    # Translate triangular matrix top-right corner
                    self.matrix[i][self.board_size - 1 - j] = 2

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
        return all(self.matrix[pair] != 0 for pair in self.top_right_corner_coords)

    def is_bottom_filled(self) -> bool:
        """
        Checks if the bottom-left corner of the board is filled with pegs.
        :return: boolean value
        """
        return all(self.matrix[pair] != 0 for pair in self.bottom_left_corner_coords)

    def is_top_filled_with(self, value: int) -> bool:
        """
        Checks if the top-right corner of the board is filled with pegs of a specific value.
        :param value: value of peg searching for in the top-right corner
        :return: boolean value
        """
        return all(self.matrix[pair] == value for pair in self.top_right_corner_coords)

    def is_bottom_filled_with(self, value: int) -> bool:
        """
        Checks if the bottom-left corner of the board is filled with pegs of a specific value.
        :param value: value of peg searching for in the bottom-left corner
        :return: boolean value
        """
        return all(self.matrix[pair] == value for pair in self.bottom_left_corner_coords)

    def is_cornered(self, corner: str, value: int) -> bool:
        if corner == 'top':
            check_condition = lambda i, j: self.matrix[i][self.board_size - 1 - j] != value
        else:  # corner == 'bottom'
            check_condition = lambda i, j: self.matrix[self.board_size - 1 - i][j] != value

        for i in range(self.triangle_size):
            for j in range(self.triangle_size):
                if i + j < self.triangle_size:
                    if check_condition(i, j):
                        return False
        return True

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

    def __str__(self):
        separator = '  '
        text = ' ' + separator + separator.join((str(i) for i in range(self.matrix.shape[0])))
        for i, row in enumerate(self.matrix):
            text += '\n' + str(i) + separator + separator.join(str(x) if x else '.' for x in row)
        return text

    def copy(self):
        new_board = Board(self.triangle_size)
        new_board.matrix = np.copy(self.matrix)
        return new_board