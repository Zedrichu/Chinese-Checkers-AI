import multiprocessing as mp
import sys
import time
from typing import Tuple, Optional

from game.Action import Action
from game.State import State
from game_problem import GameProblem
from game_problem.Heuristic import *
from players.Player import Player

sys.setrecursionlimit(2000)


class MinimaxAIPlayer(Player):
    def __init__(self, problem: GameProblem, max_player: int, max_depth: int = 8, history_size: int = 10):
        # Sets up multiprocessing
        super().__init__()
        mp.freeze_support()
        self.prob = problem
        self.MAX_PLAYER = max_player
        self.max_depth = max_depth
        self.state_history = set()
        self.HISTORY = history_size

    @property
    def average_time_spent_on_actions(self) -> float:
        return self._total_time_spent_on_taking_actions / self._moves_count

    def get_action(self, problem: GameProblem, state: State) -> Action:
        # # Prepare thread pool
        # pool = mp.Pool(processes=16)
        # print(state.board.initial_avg_euclidean)
        # # Apply problem of getting results from thread-pool
        # results = pool.apply_async(self.minimax_alpha_beta,
        #                            args=(state, state.player))
        # pool.close()
        # pool.join()
        # score, action = results.get()

        timer = time.perf_counter()

        action = self.alpha_beta_search(state)
        if len(self.state_history) > self.HISTORY:
            self.state_history.pop()
        print(self.state_history)
        print(action)

        elapsed_time = time.perf_counter() - timer
        self._total_time_spent_on_taking_actions += elapsed_time
        self._moves_count += 1
        return action

    def alpha_beta_search(self, state: State) -> Action:
        self.state_history.add(state)
        alpha = float('-inf')
        beta = float('inf')
        best_val, best_action = self.max_value(state, 0, alpha, beta)
        print(list(self.prob.actions(state)))
        return best_action

    def max_value(self, state: State, depth: int, alpha: float, beta: float) -> Tuple[float, Optional[Action]]:
        if self.cutoff_test(state, depth):
            return self.eval_state(state, self.MAX_PLAYER), None

        valid_actions = list(self.prob.actions(state))
        # Effectiveness of pruning - highly dependent of move ordering - we sort the actions by step type
        # (ends=3, then jumps=2,then crawls=1) - allows to consider the jump ending before the jump backwards (reverse)
        valid_actions.sort(key=lambda x: x.step_type, reverse=True)

        max_eval = float('-inf')
        best_action = None
        tuples = []

        for action in valid_actions:
            child = self.prob.result(state, action)
            if child in self.state_history:
                continue
            if self.prob.player(child) == self.MAX_PLAYER:
                res, sub_action = self.max_value(child, depth + 1, alpha, beta)
            else:
                res, sub_action = self.min_value(child, depth + 1, alpha, beta)
            if depth == 0:
                tuples.append((action, res, sub_action))
            if res > max_eval:
                max_eval = res
                best_action = action
                alpha = max(alpha, res)
            if max_eval >= beta:
                break
        if depth == 0:
            print(tuples)
        return max_eval, best_action

    def min_value(self, state: State, depth: int, alpha: float, beta: float) -> Tuple[float,Optional[Action]]:
        if self.cutoff_test(state, depth):
            return self.eval_state(state, self.MAX_PLAYER), None

        min_eval = float('inf')
        best_action = None

        valid_actions = list(self.prob.actions(state))
        # Effectiveness of pruning - highly dependent of move ordering - we sort the actions by step type
        # (ends=3, then jumps=2,then crawls=1) - allows to consider the jump ending before the jump backwards (reverse)
        valid_actions.sort(key=lambda x: x.step_type, reverse=True)

        for action in valid_actions:
            child = self.prob.result(state, action)
            if child in self.state_history:
                continue
            if self.prob.player(child) == self.MAX_PLAYER:
                res, sub_action = self.max_value(child, depth + 1, alpha, beta)
            else:
                res, sub_action = self.min_value(child, depth + 1, alpha, beta)
            if res < min_eval:
                min_eval = res
                best_action = action
                beta = min(beta, res)
            if min_eval <= alpha:
                break
        return min_eval, best_action

    @staticmethod
    def path_cost(c, state1, action, state2):
        return c + 1

    def eval_state(self, state: State, player: int) -> float:
        if self.prob.terminal_test(state):
            return self.prob.utility(state, player)

        weights = [0.1, 0.3, 0.4, 0.2]  # Sum must be always equal ~ 1

        peg_count = (state.board.triangle_size - 1) * state.board.triangle_size / 2
        initial_euclidean = initial_avg_euclidean(state.board)

        # Consider Manhattan distance towards the goal corner of each player - normalize the distance by 2 board size
        # Subtract the normalized distance from 1 to get a heuristic that is higher when closer to the goal
        heuristic1 = (1 - average_manhattan_to_corner(state.board, player) / (2 * state.board.board_size)) * weights[1]

        # Consider the sum of pegs of the player - normalize the sum by the peg count for each player - scaled by weight
        heuristic2 = (sum_player_pegs(state.board, player) / peg_count) * weights[0]  # / peg_count

        # Consider the Euclidean distance towards the goal corner of each player - normalize the distance by the initial
        # average distance to the corner - subtract the normalized distance from 1 to get a heuristic that is higher
        # when closer to the goal
        heuristic3 = (1 - average_euclidean_to_corner(state.board, player) / initial_euclidean) * weights[2]

        heuristic4 = (1 - max_manhattan_to_corner(state.board, player) / (2 * state.board.board_size)) * weights[3]

        # print(f'Heuristic 1: {heuristic1} | Heuristic 2: {heuristic2} | Heuristic 3: {heuristic3}')
        # Compute the combined heuristic function and flip the value if the player is
        return heuristic1 + heuristic2 + heuristic3 + heuristic4

    def cutoff_test(self, state: State, depth: int) -> bool:
        return self.prob.terminal_test(state) or depth == self.max_depth

