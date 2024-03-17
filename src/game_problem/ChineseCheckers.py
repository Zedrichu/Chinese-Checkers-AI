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
        """
        Initial state of the Chinese Checkers game
        :return: a state object
        """
        return State(Board(self.triangle_size), 1, mode=Step.END, peg=(None, None))

    def player(self, state: State) -> int:
        """
        The player to move in the current state
        :param state: the current state of the game
        :return: the player index
        """
        return state.player

    @staticmethod
    def _peg_actions(state, src: Tuple[int, int]) -> Iterable[Action]:
        """
        Generate all possible actions for a selected peg
        :param state: current state of the game
        :param src: the selected peg coordinate pair
        :return: an iterable of valid actions
        """
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
        """
        Generate all possible actions for the current state
        :param state: current state of the game
        :return: an iterable of valid actions
        """
        board = state.board
        for i in range(board.board_size):
            for j in range(board.board_size):
                if board.matrix[i][j] == state.player:
                    yield from self._peg_actions(state, (i, j))

    def result(self, state: State, action: Action) -> State:
        """
        Apply the action to the current state and return the new state (copied version)
        :param state: current state of the game
        :param action: action to be applied
        :return: the new state obtained
        """
        new_board = copy(state.board)
        new_board.move(action.src, action.dest)

        new_state = State(new_board, state.player, action.step_type, action.dest)

        if action.step_type == Step.CRAWL or action.step_type == Step.END:
            new_state.player = 3 - state.player

        return new_state

    def terminal_test(self, state: State) -> bool:
        """
        Check if the current state is a terminal state - one of the players wins
        :param state: current state of the game
        :return: flag indicating if the state is terminal
        """
        return state.board.is_top_right_terminal() or state.board.is_bot_left_terminal()

    def utility(self, state: State, player: int) -> int:
        """
        Calculate the utility of the current state for a specific player
        :param state: current state of the game
        :param player: the player index
        :return: payoff values for each player depending on the state
        """
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
