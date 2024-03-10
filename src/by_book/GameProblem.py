from abc import ABC, abstractmethod
from copy import copy
from functools import cached_property
from typing import Iterable, List, Tuple

from by_book.Action import Action
from by_book.State import State
from by_book.chinese_toolbox import list_adjacent_cells


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
    def _find_crawl_moves(state: State, src: Tuple[int, int]) -> Iterable[Action]:
        """
        Find the moves to adjacent non-occupied cells.
        """
        for position in list_adjacent_cells(state.board, src):
            if state.board.matrix[position] == 0:
                yield Action(steps=[src, position])

    @staticmethod
    def _find_jump_moves(state: State, path: List[Tuple[int, int]]) -> Iterable[Action]:
        """
        For a given path of positions, recursively find all possible jumps, stopping when a jump lands inside the path.
        To start, use path=[initial_position].
        """
        src = path[-1]
        for pos in list_adjacent_cells(state.board, src):
            if state.board.matrix[pos] == 0:
                continue

            landing = None
            if src[0] - 1 == pos[0] and src[1] - 1 == pos[1]:
                # Diagonal up jump
                landing = src[0] - 2, src[0] - 2
            elif src[0] - 1 == pos[0] and src[1] == pos[1]:
                # Up jump
                landing = src[0] - 2, src[1]
            elif src[0] == pos[0] and src[1] + 1 == pos[1]:
                # Right jump
                landing = src[0], src[1] + 2
            elif src[0] + 1 == pos[0] and src[1] + 1 == pos[1]:
                # Diagonal down jump
                landing = src[0] + 2, src[1] + 2
            elif src[0] + 1 == pos[0] and src[1] == pos[1]:
                # Down jump
                landing = src[0] + 2, src[1]
            elif src[0] == pos[0] and src[1] - 1 == pos[1]:
                # Left jump
                landing = src[0], src[1] - 2

            if landing is None:
                continue

            if not state.board.is_bound(landing) or state.board.matrix[landing] != 0:
                continue

            # Invalidate if it enters a loop
            if landing in path:
                continue

            new_path = [*path, landing]
            yield Action(new_path)
            yield from ChineseCheckersGameProblem._find_jump_moves(state, new_path)

    def actions(self, state: State) -> Iterable[Action]:
        for i in range(state.board.board_size):
            for j in range(state.board.board_size):
                if state.board.matrix[i][j] == state.player_to_move + 1:
                    yield from self._find_crawl_moves(state, (i, j))
                    yield from self._find_jump_moves(state, [(i, j)])

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


