from copy import copy
from functools import cached_property
from typing import Tuple, Iterable
from game_problem.GameProblem import GameProblem
from game.Step import Step
from game.Action import Action
from game.State import State
from game.Board import Board


class ChineseCheckers(GameProblem):
    def __init__(self, triangle_size: int = 3):
        self.triangle_size = triangle_size

    @cached_property
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
        player1 = state.board.is_cornered('top', 1)
        player2 = state.board.is_cornered('bottom', 2)
        if player1 or player2:
            return True
        # Extension of terminal test to account for children that are terminal - losing can't be avoided
        for a in self.actions(state):
            new_state = self.result(state, a)
            if (new_state.board.is_cornered('top', 1)
                    or new_state.board.is_cornered('bottom', 2)):
                return True
        return False

    def utility(self, state: State, player: int) -> int:
        if state.board.is_cornered('top', player):
            return 1
        return -1


if __name__ == "__main__":
    cc = ChineseCheckers()
    init = cc.initial_state
    print(init)
    for act in cc.actions(init):
        print(act)
    pass
