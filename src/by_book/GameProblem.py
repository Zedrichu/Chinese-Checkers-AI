from abc import ABC, abstractmethod
from copy import copy
from functools import cached_property
from typing import Iterable, List, Tuple

from by_book.Action import Action
from by_book.State import State


class GameProblem(ABC):
    @property
    @abstractmethod
    def initial_state(self) -> State:
        pass

    @abstractmethod
    def player(self, state: State) -> int:
        """Who has to move in state"""
        pass

    @abstractmethod
    def actions(self, state: State) -> Iterable[Action]:
        """Legal moves in state"""
        pass

    @abstractmethod
    def result(self, state: State, move: Action) -> State:
        """Transition model"""
        pass

    @abstractmethod
    def terminal_test(self, state: State) -> bool:
        """Is the game over?"""
        pass

    @abstractmethod
    def utility(self, state: State, player_id: int) -> int:
        """
        Numerical value for the given player in the given terminal state.
        Example: +1 for win and −1 for loose (zero-sum).
        """
        pass


class ChineseCheckersGameProblem(GameProblem):
    def __init__(self, initial_state: State, players_count: int = 2):
        self._initial_state = initial_state
        self._players_count = players_count

    @cached_property
    def initial_state(self) -> State:
        return self._initial_state

    def player(self, state: State) -> int:
        return state.player_to_move

    @staticmethod
    def _find_all_moves_for_position(state: State, src: Tuple[int, int]) -> Iterable[Action]:
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_position = (src[0] + i, src[1] + j)
                y_is_out_of_bounds = new_position[0] < 0 or new_position[0] >= state.board.board_size
                x_is_out_of_bounds = new_position[1] < 0 or new_position[1] >= state.board.board_size
                if y_is_out_of_bounds or x_is_out_of_bounds:
                    continue

                position_is_occupied = state.board.matrix[new_position] != 0
                if position_is_occupied:
                    continue

                yield Action(steps=[src, new_position])

    def actions(self, state: State) -> Iterable[Action]:
        for i in range(state.board.board_size):
            for j in range(state.board.board_size):
                if state.board.matrix[i][j] == state.player_to_move + 1:
                    yield from self._find_all_moves_for_position(state, (i, j))

    def result(self, state: State, move: Action) -> State:
        initial_position = move.steps[0]
        final_position = move.steps[-1]

        new_board = copy(state.board)
        new_board.move(initial_position, final_position)
        player_to_move = (state.player_to_move + 1) % self._players_count
        return State(board=new_board, player_to_move=player_to_move)

    def terminal_test(self, state: State) -> bool:
        if state.board.bottom_is_filled() or state.board.top_is_filled():
            return not state.board.bottom_is_filled_with(1) and not state.board.top_is_filled_with(2)
        else:
            return False

    def utility(self, state: State, player_id: int) -> int:
        """
        Given that it is a terminal state, return +1 if the opposing corner of the board is filled
        """
        if player_id == 0:
            return 1 if state.board.top_is_filled() else -1
        else:
            return 1 if state.board.bottom_is_filled() else -1


