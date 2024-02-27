class Board:
    def __init__(self, triangle_size: int = 3):
        self.triangle_size = triangle_size
        self.board_size = triangle_size * 2 + 1
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.init_board()

    def init_board(self):
        for i in range(self.triangle_size):
            for j in range(self.triangle_size):
                if j < self.board_size - self.triangle_size - i - 1:
                    self.board[self.board_size - 1 - i][j] = 1
                    self.board[i][self.board_size - 1 - j] = 2

    def print_diamond(self):
        return '\n'.join('\t'.join(str(x) for x in row) for row in self.board)

    def __str__(self):
        return '\n'.join('\t'.join(str(x) for x in row) for row in self.board)
