from dataclasses import dataclass
from typing import Tuple

from State import State
from Board import Board


class GameProblem:
    def __init__(self):
        board = Board(3)
        board.init_board()
        self.state = State(board, 1)

    def player(self):
        return self.player

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def terminal_test(self, state):
        player1 = state.board.is_cornered('top', 1)
        player2 = state.board.is_cornered('bottom', 2)
        return player1 or player2

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def cutoff_test(self, state):
        raise NotImplementedError

    def utility(self, player, state):
        raise NotImplementedError


class Step:
    MOVE = 1
    JUMP = 2

    # Validate move based on available moves in 2D space.
    @staticmethod
    def validate_move(state: State, src: Tuple[int, int], dest: Tuple[int, int]):
        x1, y1 = src
        x2, y2 = dest
        print(f"dest: {x2} {y2} src: {x1} {y1}")
        if (((abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or
             (abs(x1 - x2) == 0 and abs(y1 - y2) == 1) or
             abs(x2 + y2 - (x1 + y1)) == 2 and abs(x2 - x1) == 1)
                and state.board[x2][y2] == 0):
            return True
        return False

    @staticmethod
    def validate_jump(state: State, src: Tuple[int, int], dest: Tuple[int, int]):
        x1, y1 = src
        x2, y2 = dest
        print(f"dest: {x2} {y2} src: {x1} {y1}")
        if (((abs(x2 + y2 - (x1 + y1)) == 4 and abs(x2 - x1) == 2) or
             (abs(x1 - x2) == 2 and abs(y1 - y2) == 0) or
             (abs(x1 - x2) == 0 and abs(y1 - y2) == 2)) and
                state.board[(x1 + x2) // 2][(y1 + y2) // 2] != 0):
            return True
        pass

    @staticmethod
    def validate_step(state: State):
        raise NotImplementedError
