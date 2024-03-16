import numpy as np

from game import Board
from game.Board import bot_left_corner_coords, top_right_corner_coords

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
