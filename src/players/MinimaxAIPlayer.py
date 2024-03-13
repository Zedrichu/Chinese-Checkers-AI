import multiprocessing as mp
import time
import sys
from functools import cached_property
from typing import Tuple, Optional

import numpy as np

from game.State import State
from game.Action import Action
from game_problem import GameProblem
from players.Player import Player

sys.setrecursionlimit(1000)


class MinimaxAIPlayer(Player):
    def __init__(self, problem: GameProblem, max_depth: int = 8):
        # Sets up multiprocessing
        mp.freeze_support()
        self.prob = problem
        self.max_depth = max_depth

    def get_action(self, problem: GameProblem, state: State) -> Action:
        # Prepare thread pool
        # pool = mp.Pool(processes=16)
        # print(state.board.initial_avg_euclidean)
        # # Apply problem of getting results from thread-pool
        # results = pool.apply_async(self.minimax_alpha_beta,
        #                            args=(state, state.player))
        # pool.close()
        # pool.join()
        # score, action = results.get()
        score, action = self.minimax_alpha_beta(state, state.player)
        return action

        # self.minimax_alpha_beta, args=(self.prob, state, depth=8, -inf, +inf, self.state.player)

    def minimax_alpha_beta(self, state: State, depth: int = 0, alpha: float = float('-inf'),
                           beta: float = float('+inf'), max_player: bool = True) -> Tuple[float, Optional[Action]]:
        """
        Minimax algorithm with alpha-beta pruning
        :param prob: formal definition of a Game Problem
        :param state:
        :param depth:
        :param alpha:
        :param beta:
        :param max_player:
        :return:
        """
        # TODO: Terminal_test and utility needs fix
        if self.cutoff_test(state, depth):
            return self.eval_state(state, max_player + 1), None

        if max_player:
            max_eval = float('-inf')
            best_action = None
            for action in self.prob.actions(state):
                child = self.prob.result(state, action)
                res, _ = self.minimax_alpha_beta(child, depth + 1, alpha, beta, False)
                if res > max_eval:
                    max_eval = res
                    best_action = action
                alpha = max(alpha, res)
                if max_eval >= beta:
                    break
            print(f'Depth {depth} -> {best_action}')
            return max_eval, best_action

        else:
            min_eval = float('inf')
            best_action = None
            for action in self.prob.actions(state):
                child = self.prob.result(state, action)
                res, _ = self.minimax_alpha_beta(child, depth + 1, alpha, beta, True)
                if res < min_eval:
                    min_eval = res
                    best_action = action
                beta = min(beta, res)
                if min_eval <= alpha:
                    break
            print(f'Depth {depth} -> {best_action}')
            return min_eval, best_action

    @staticmethod
    def path_cost(c, state1, action, state2):
        return c + 1

    def eval_state(self, state: State, player: int) -> float:
        if self.prob.terminal_test(state):
            return self.prob.utility(state, player)

        weights = [0.2, 0.4, 0.4]  # Sum must be always equal ~ 1

        peg_count = (state.board.triangle_size - 1) * state.board.triangle_size / 2
        initial_avg_euclidean = state.board.initial_avg_euclidean

        if player == 1:
            coef = 1
        else:
            coef = -1

        return coef * (state.board.sum_player_pegs(player) / peg_count * weights[0]
                    + state.board.average_euclidean_to_corner(player) / initial_avg_euclidean * weights[1]
                    + state.board.average_manhattan_to_corner(player) / (2 * state.board.board_size) * weights[2])

    def cutoff_test(self, state: State, depth: int) -> bool:
        if self.prob.terminal_test(state) or depth == self.max_depth:
            return True
        return False
