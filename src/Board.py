from typing import Tuple, List
import numpy as np
import pygame


class Board:
    def __init__(self, triangle_size: int):
        self.triangle_size = triangle_size
        self.board_size = triangle_size * 2 + 1
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.init_board()

    def is_cornered(self, corner: str, value: int) -> bool:
        if corner == 'top':
            check_condition = lambda i, j: self.board[i][self.board_size - 1 - j] != value
        else: # corner == 'bottom'
            check_condition = lambda i, j: self.board[self.board_size - 1 - i][j] != value

        for i in range(self.triangle_size):
            for j in range(self.triangle_size):
                if j + i < self.triangle_size:
                    if check_condition(i, j):
                        return False
        return True

    def init_board(self):
        for i in range(self.triangle_size):
            for j in range(self.triangle_size):
                # Define small triangular matrix function
                #   with dimensions triangle_size • triangle_size
                if j + i < self.triangle_size:
                    # Translate triangular matrix bottom-left corner
                    self.board[self.board_size - 1 - i][j] = 1
                    # Translate triangular matrix top-right corner
                    self.board[i][self.board_size - 1 - j] = 2

    def move(self, initial_pos: Tuple[int, int], path: List[Tuple[int, int]]):
        current_x, current_y = initial_pos
        for coordinates in path:
            x, y = coordinates

            if x < 0 or x > self.board_size - 1 or y < 0 or y > self.board_size:
                raise Exception(f'Coordinates out of bound: {coordinates}')

            self.board[x][y] = self.board[current_x][current_y]
            self.board[current_x][current_y] = 0
            current_x, current_y = x, y

    def __str__(self):
        return '\n'.join('\t'.join(str(x) if x else '.' for x in row) for row in self.board)