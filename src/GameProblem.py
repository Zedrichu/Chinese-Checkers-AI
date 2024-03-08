from dataclasses import dataclass
from typing import Tuple, List

from State import State
from Board import Board


class Step:
    CRAWL = 1
    JUMP = 2

    # Validate move based on available moves in 2D space.
    @staticmethod
    def validate_crawl(board: Board, src: Tuple[int, int], dest: Tuple[int, int]):
        x1, y1 = src
        x2, y2 = dest
        print(f"dest: {x2} {y2} src: {x1} {y1}")
        if (((abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or
             (abs(x1 - x2) == 0 and abs(y1 - y2) == 1) or
             abs(x2 + y2 - (x1 + y1)) == 2 and abs(x2 - x1) == 1)
                and board.matrix[x2][y2] == 0):
            return True
        return False

    @staticmethod
    def validate_jump(board: Board, src: Tuple[int, int], dest: Tuple[int, int]):
        x1, y1 = src
        x2, y2 = dest
        print(f"dest: {x2} {y2} src: {x1} {y1}")
        if (((abs(x2 + y2 - (x1 + y1)) == 4 and abs(x2 - x1) == 2) or
             (abs(x1 - x2) == 2 and abs(y1 - y2) == 0) or
             (abs(x1 - x2) == 0 and abs(y1 - y2) == 2)) and
                board.matrix[(x1 + x2) // 2][(y1 + y2) // 2] != 0):
            return True
        pass

    @staticmethod
    def validate_step(board: Board, src: Tuple[int, int], dest: Tuple[int, int]):
        if (abs(src[0] - dest[0]) <= 1 and abs(src[1] - dest[1]) <= 1
                and Step.validate_crawl(board, src, dest)):
            return Step.CRAWL
        elif Step.validate_jump(board, src, dest):
            return Step.JUMP
        return None


@dataclass
class Action:
    src: Tuple[int, int]
    dest: Tuple[int, int]
    step_type: int

    @staticmethod
    def generate_peg_actions(board: Board, src: Tuple[int, int]):
        actions = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (src[0] + i >= 0 or src[0] + i < board.board_size
                        or src[1] + j >= 0 or src[1] + j < board.board_size):
                    res = Step.validate_step(board, src, (src[0] + i, src[1] + j))
                    if res is not None:
                        actions.append(Action(src, (src[0] + i, src[1] + j), res))
        return actions

    def __str__(self):
        return f"src: {self.src} dest: {self.dest} step_type: {self.step_type}"


class GameProblem:
    def __init__(self):
        board = Board(3)
        board.init_board()
        self.state = State(board, 1)

    def player(self):
        return self.state.player

    def actions(self):
        board = self.state.board
        actions = []
        for i in range(board.board_size):
            for j in range(board.board_size):
                if board.matrix[i][j] == self.state.player:
                    actions.extend(Action.generate_peg_actions(board, (i, j)))
        return actions

    def result(self, state, action):
        raise NotImplementedError

    def terminal_test(self):
        player1 = self.state.board.is_cornered('top', 1)
        player2 = self.state.board.is_cornered('bottom', 2)
        return player1 or player2

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def cutoff_test(self, state):
        raise NotImplementedError

    def utility(self, player):
        if self.state.board.is_cornered('top', player):
            return 1
        return -1
