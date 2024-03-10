from dataclasses import dataclass
from typing import Tuple, List, Iterable
from src.GameProblem import GameProblem
from src.Step import Step
from src.Action import Action
from src.State import State
from src.Board import Board


class ChineseCheckers(GameProblem):
    initial_state: State = State(Board(3), 1, mode=0, peg=(None, None))

    @staticmethod
    def player(state: State) -> int:
        return state.player

    @staticmethod
    def peg_actions(state, src: Tuple[int, int]) -> Iterable[Action]:
        board = state.board

        for i in range(-2, 3):
            for j in range(-2, 3):
                if board.within_bounds((src[0] + i, src[1] + j)):
                    res = None

                    if state.mode == Step.JUMP and src == state.peg:
                        res = Step.validate_jump(board, src, (src[0] + i, src[1] + j))

                    if state.mode == Step.END or state.mode == Step.CRAWL:
                        res = Step.validate_step(board, src, (src[0] + i, src[1] + j))

                    if res is not None:
                        yield Action(src, (src[0] + i, src[1] + j), res)

    @staticmethod
    def actions(state: State) -> Iterable[Action]:
        board = state.board
        for i in range(board.board_size):
            for j in range(board.board_size):
                if board.matrix[i][j] == state.player:
                    yield from ChineseCheckers.peg_actions(state, (i, j))

    @staticmethod
    def result(state: State, action: Action) -> State:
        new_board = state.board.copy()
        new_board.move(action.src, action.dest)

        new_state = State(new_board, state.player, action.step_type, action.dest)

        if action.step_type == Step.CRAWL or action.step_type == Step.END:
            new_state.player = 3 - state.player

        return new_state

    @staticmethod
    def terminal_test(state: State) -> bool:
        player1 = state.board.is_cornered('top', 1)
        player2 = state.board.is_cornered('bottom', 2)
        return player1 or player2

    @staticmethod
    def path_cost(c, state1, action, state2):
        return c + 1

    @staticmethod
    def cutoff_test(state: State):
        raise NotImplementedError

    @staticmethod
    def utility(state, player):
        if state.board.is_cornered('top', player):
            return 1
        return -1


if __name__ == "__main__":
    new = ChineseCheckers.initial_state
    print(new)
    for action in ChineseCheckers.actions(new):
        print(action)
    pass
