from copy import copy
from typing import Tuple, Iterable

from game.Action import Action
from game.Board import Board
from game.State import State
from game.Step import Step
from game_problem.GameProblem import GameProblem


class ChineseCheckers(GameProblem):
    def __init__(self, triangle_size: int = 3):
        self.triangle_size = triangle_size

    def initial_state(self) -> State:
        return State(Board(self.triangle_size), 1, mode=Step.END, peg=(None, None))

    def player(self, state: State) -> int:
        return state.player

    @staticmethod
    def _peg_actions(state, src: Tuple[int, int]) -> Iterable[Action]:
        board = state.board

        for i in range(-2, 3):
            for j in range(-2, 3):
                if board.within_bounds((src[0] + i, src[1] + j)):
                    res = None

                    if state.mode == Step.JUMP and src == state.peg:
                        res = Step.validate_tail(board, src, (src[0] + i, src[1] + j))

                    if state.mode == Step.END or state.mode == Step.CRAWL:
                        res = Step.validate_head(board, src, (src[0] + i, src[1] + j))

                    if res is not None:
                        yield Action(src, (src[0] + i, src[1] + j), res)

    def actions(self, state: State) -> Iterable[Action]:
        board = state.board
        for i in range(board.board_size):
            for j in range(board.board_size):
                if board.matrix[i][j] == state.player:
                    yield from self._peg_actions(state, (i, j))

    def result(self, state: State, action: Action) -> State:
        new_board = copy(state.board)
        new_board.move(action.src, action.dest)

        new_state = State(new_board, state.player, action.step_type, action.dest)

        if action.step_type == Step.CRAWL or action.step_type == Step.END:
            new_state.player = 3 - state.player

        return new_state

    def terminal_test(self, state: State) -> bool:
        """
        :param state:
        :return: True or False depending on
        """
        return state.board.is_top_right_terminal() or state.board.is_bot_left_terminal()

    def utility(self, state: State, player: int) -> int:
        if state.board.is_top_right_terminal():
            return (-1) ** (player == 2)
        elif state.board.is_bot_left_terminal():
            return (-1) ** (player == 1)
        else:
            return 0


if __name__ == "__main__":
    cc = ChineseCheckers()
    init = cc.initial_state
    print(init)
    for act in cc.actions(init):
        print(act)
    pass
