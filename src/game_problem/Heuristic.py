import numpy as np

from game import Board

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
    diffs = board.corner_triangles[0] - [0, board.board_size - 1]
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
    corner = board.corner_triangles[2 - player]  # 1-indexed player
    return np.sum(board.matrix[corner[:, 0], corner[:, 1]] == player)
