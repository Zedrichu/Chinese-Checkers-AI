from typing import Tuple, List
import numpy as np
import pygame

class Board:
    def __init__(self, triangle_size: int):
        self.triangle_size = triangle_size
        self.board_size = triangle_size * 2 + 1
        self.board = np.zeros((self.board_size, self.board_size))
        self.init_board()

    def is_cornered(self):

        for i in range(self.triangle_size):
            for j in range(self.triangle_size):
                if j + i < self.triangle_size:
                    # Translate triangular matrix bottom-left corner
                    self.board[self.board_size - 1 - i][j] = 1
                    # Translate triangular matrix top-right corner
                    self.board[i][self.board_size - 1 - j] = 2
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

    # Method to draw circles for each tile in a diamond shape
    def draw_diamond(self, screen):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, (0, 0, 255), (j * 50 + 25, i * 50 + 25), 20)
                elif self.board[i][j] == 0:
                    pygame.draw.circle(screen, (0, 0, 0), (j * 50 + 25, i * 50 + 25), 20)
                elif self.board[i][j] == 2:
                    pygame.draw.circle(screen, (255, 0, 0), (j * 50 + 25, i * 50 + 25), 20)



    def __str__(self):
        return '\n'.join('\t'.join(str(x) if x else '.' for x in row) for row in self.board)