from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np

from game import Board
from game.Board import bot_left_corner_coords, top_right_corner_coords
from game.State import State

"""
Utility functions for evaluation of board states.
Primarily different Heuristics functions
"""


def average_euclidean_to_corner(board: Board, player: int) -> float:
    corner = decide_goal_corner_coordinates(board, player)
    indices = np.argwhere(board.matrix == player)
    distances = np.linalg.norm(indices - corner, axis=1)
    return np.mean(distances)


def initial_avg_euclidean(board: Board):
    """
    Returns the average Euclidian distance between the two initial corner triangles
    :return: mean of Euclidian distances
    """
    bottom_corner = bot_left_corner_coords(board.triangle_size, board.board_size)
    diffs = bottom_corner - [0, board.board_size - 1]
    distances = np.linalg.norm(diffs, axis=1)
    return np.mean(distances)


def average_manhattan_to_corner(board: Board, player: int) -> float:
    corner = decide_goal_corner_coordinates(board, player)
    indices = np.argwhere(board.matrix == player)
    distances = np.sum(np.abs(indices - corner), axis=1)
    return np.mean(distances)


def max_manhattan_to_corner(board: Board, player: int) -> float:
    corner = decide_goal_corner_coordinates(board, player)
    indices = np.argwhere(board.matrix == player)
    distances = np.sum(np.abs(indices - corner), axis=1)
    return np.max(distances)


def decide_goal_corner_coordinates(board: Board, player: int):
    if player == 1:
        corner = top_right_corner_coords(board.triangle_size, board.board_size)
    else:
        corner = bot_left_corner_coords(board.triangle_size, board.board_size)
    for pair in corner:
        if board.matrix[pair[0], pair[1]] == 0:
            return pair

    # Base case
    if player == 1:
        corner = [0, board.board_size - 1]
    else:
        corner = [board.board_size - 1, 0]
    return corner


def sum_player_pegs(board: Board, player: int) -> float:
    """
    Returns the sum of pegs in the corner triangles for a specific player.
    :param board:
    :param player: int
    :return:
    """
    if player == 1:
        corner = top_right_corner_coords(board.triangle_size, board.board_size)
    else:
        corner = bot_left_corner_coords(board.triangle_size, board.board_size)
    return np.sum(board.matrix[corner[:, 0], corner[:, 1]] == player)


class Heuristic(ABC):
    @abstractmethod
    def eval(self, state: State, player: int) -> float:
        raise NotImplemented


class NoneHeuristic(Heuristic):
    """
    A heuristic that always returns 0
    """
    def eval(self, state: State, player: int) -> float:
        return 0


class EnsuredNormalizedHeuristic(Heuristic):
    """
    Utility to verify that the inner heuristic is normalized.
    Usage: EnsuredNormalizedHeuristic(SomeOtherHeuristic()).eval(state, player)
    """
    def __init__(self, inner_heuristic: Heuristic):
        self.inner_heuristic = inner_heuristic

    def eval(self, state: State, player: int) -> float:
        value = self.inner_heuristic.eval(state, player)
        assert -0.001 <= value <= 1, f'{type(self.inner_heuristic).__name__}: Assertion -0.001 <= {value} <= 1 Failed'
        return value


class WeightedHeuristic(Heuristic):
    """
    Utility to combine multiple heuristics with different weights.
    """
    def __init__(self, weighted_heuristics: List[Tuple[Heuristic, float]]):
        self.weighted_heuristics = weighted_heuristics
        total_weights = sum(weight for _, weight in weighted_heuristics)
        if total_weights != 1:
            raise ValueError(f'Total weights must be 1')

    def eval(self, state: State, player: int) -> float:
        """
        Combine the weighted heuristics
        :param state: the current state of the game
        :param player: the player for which the heuristic is evaluated
        :return: value of the combined heuristic
        """
        total = 0
        for heuristic, weight in self.weighted_heuristics:
            total += heuristic.eval(state, player) * weight
        return total


class AverageManhattanToCornerHeuristic(Heuristic):
    def eval(self, state: State, player: int) -> float:
        """
        Consider Manhattan distance towards the goal corner of each player - normalize the distance by 2 board size
        Subtract the normalized distance from 1 to get a heuristic that is higher when closer to the goal
        """
        return 1 - average_manhattan_to_corner(state.board, player) / (2 * state.board.board_size)


class SumOfPegsInCornerHeuristic(Heuristic):
    def eval(self, state: State, player: int) -> float:
        """
        Consider the sum of pegs of the player - normalize the sum by the peg count for each player
        """
        peg_count = (state.board.triangle_size + 1) * state.board.triangle_size / 2
        return sum_player_pegs(state.board, player) / peg_count


class AverageEuclideanToCornerHeuristic(Heuristic):
    def eval(self, state: State, player: int) -> float:
        """
        Consider the Euclidean distance towards the goal corner of each player - normalize the distance by the initial
        average distance to the corner - subtract the normalized distance from 1 to get a heuristic that is higher
        when closer to the goal
        """
        initial_euclidean = initial_avg_euclidean(state.board)
        return 1 - average_euclidean_to_corner(state.board, player) / initial_euclidean


class AverageEuclideanToEachCornerHeuristic(Heuristic):
    def eval(self, state: State, player: int) -> float:
        """
        AverageEuclideanToCornerHeuristic but does a mean of the distance to each corner.
        """
        initial_euclidean = initial_avg_euclidean(state.board)

        if player == 1:
            corners = top_right_corner_coords(state.board.triangle_size, state.board.board_size)
        else:
            corners = bot_left_corner_coords(state.board.triangle_size, state.board.board_size)
        indices = np.argwhere(state.board.matrix == player)

        means = 0
        for corner in corners:
            distances = np.linalg.norm(indices - corner, axis=1)
            means += np.mean(distances)
        final_mean = means / len(corners)
        return 1 - final_mean / initial_euclidean


class MaxManhattanToCornerHeuristic(Heuristic):
    """
    Consider the maximal Manhattan distance towards the goal corner of each player - normalize the distance by 2
    board size - helps to avoid the player from leaving pegs behind and carry them together towards the goal
    """
    def eval(self, state: State, player: int) -> float:
        return 1 - max_manhattan_to_corner(state.board, player) / (2 * state.board.board_size)
