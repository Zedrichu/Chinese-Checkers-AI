import pygame as pg
from GameProblem import Step
from State import State


class Graphics:
    def __init__(self, board):
        self.board = board
        # self.screen = pg.display.set_mode((self.board.board_size * 50, self.board.board_size * 50))
        self.colors = ['blue', 'red']
        self.start_tile = None
        self.target_tile = None

    # Method to draw circles for each tile in a diamond shape
    def draw_diamond_board(self, screen):
        screen.fill((255, 255, 255))
        for i in range(self.board.board_size):
            for j in range(self.board.board_size):
                if self.board.board[i][j] == 1:
                    pg.draw.circle(screen, (0, 0, 255), (j * 50 + 25, i * 50 + 25), 20)
                elif self.board.board[i][j] == 0:
                    pg.draw.circle(screen, (0, 0, 0), (j * 50 + 25, i * 50 + 25), 20)
                elif self.board.board[i][j] == 2:
                    pg.draw.circle(screen, (255, 0, 0), (j * 50 + 25, i * 50 + 25), 20)

    def draw_turn(self, turn: int, screen):
        pg.draw.rect(screen, (245, 245, 220), (0, screen.get_height() - 50, 720, 50))
        font = pg.font.Font(None, 36)
        text = font.render(f"Player {turn}'s turn", True, pg.Color(self.colors[turn - 1]))
        screen.blit(text, (270, screen.get_height() - 40))

    def click(self, mouse, turn):
        for i in range(self.board.board_size):
            for j in range(self.board.board_size):
                if ((j * 50 + 25 - 20 < mouse[0] < j * 50 + 25 + 20) and
                        (i * 50 + 25 - 20 < mouse[1] < i * 50 + 25 + 20)):
                    print(f'Clicked on tile: {i, j}')
                    if self.board.board[i][j] == turn:
                        self.start_tile = (i, j)

                        print(f'Start tile: {self.start_tile}')

                    print(self.board.board[i][j])
                    print(self.start_tile)
                    if self.board.board[i][j] == 0 and self.start_tile is not None:
                        self.target_tile = (i, j)
                        print(f'Target tile: {self.target_tile}')

                        start = self.start_tile
                        target = self.target_tile
                        if target is not None and start is not None:
                            x1, y1 = start
                            x2, y2 = target
                            if abs(x1 - x2) > 1 or abs(y1 - y2) > 1:
                                valid = Step.validate_jump(
                                    State(self.board.board, turn),
                                    (start[0], start[1]),
                                    (target[0], target[1])
                                )
                            else:
                                valid = Step.validate_move(
                                    State(self.board.board, turn),
                                    (start[0], start[1]),
                                    (target[0], target[1])
                                )
                            if valid:
                                self.board.board[target[0]][target[1]] = turn
                                self.board.board[start[0]][start[1]] = 0
                                self.start_tile = None
                                self.target_tile = None
                                return

    def hover(self, mouse, turn, screen):
        for i in range(self.board.board_size):
            for j in range(self.board.board_size):
                if ((j * 50 + 25 - 20 < mouse[0] < j * 50 + 25 + 20)
                        and (i * 50 + 25 - 20 < mouse[1] < i * 50 + 25 + 20)):

                    # color the outline of circles of the circle of current player's turn
                    if self.board.board[i][j] == turn:
                        pg.draw.circle(screen, pg.Color(self.colors[turn-1]), (j * 50 + 25, i * 50 + 25), 15, 5)
                        pg.draw.circle(screen, pg.Color('green'), (j * 50 + 25, i * 50 + 25), 20, 5)
                    elif self.board.board[i][j] == 0:
                        # draw cross if tile is not owned by any player
                        pg.draw.line(screen, pg.Color('white'), (j * 50 + 5, i * 50 + 5), (j * 50 + 45, i * 50 + 45), 5)
                        pg.draw.line(screen, pg.Color('white'), (j * 50 + 45, i * 50 + 5), (j * 50 + 5, i * 50 + 45), 5)
