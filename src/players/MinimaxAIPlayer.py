import multiprocessing as mp
import sys
import time
from collections import deque
from typing import Tuple, Optional

from game.Action import Action
from game.State import State
from game_problem import GameProblem
from game_problem.Heuristic import *
from players.Player import Player

sys.setrecursionlimit(2000)


class MinimaxAIPlayer(Player):
    def __init__(
            self,
            problem: GameProblem,
            max_player: int,
            max_depth: int,
            heuristic: Heuristic,
            history_size: int = 10,
            verbose=True
    ):
        # Sets up multiprocessing
        super().__init__()
        mp.freeze_support()
        self.verbose = verbose
        self.prob = problem
        self.MAX_PLAYER = max_player
        self.heuristic = heuristic
        self.max_depth = max_depth

        # Counter for the evaluated states
        self.evaluated_states_count = 0

        # set.pop() - removes a random element from the set
        # Therefore, an additional queue is used to remember which element is the oldest
        self.history_size = history_size
        self._state_history_set = set()
        self._state_history_queue = deque()

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

        elapsed_time = time.perf_counter() - timer
        self._total_time_spent_on_taking_actions += elapsed_time
        self._moves_count += 1
        return action

    def alpha_beta_search(self, state: State) -> Action:
        self._add_state_to_history(state)
        alpha = float('-inf')
        beta = float('inf')
        best_val, best_action = self.max_value(state, 0, alpha, beta)
        if self.verbose:
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
            if self._state_is_in_history(child):
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
        if self.verbose and depth == 0:
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
            if self._state_is_in_history(child):
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
        self.evaluated_states_count += 1
        if self.prob.terminal_test(state):
            return self.prob.utility(state, player)
        return self.heuristic.eval(state, player)

    def cutoff_test(self, state: State, depth: int) -> bool:
        return self.prob.terminal_test(state) or depth == self.max_depth

    def _add_state_to_history(self, state: State):
        # state_value = state
        state_value = hash(state)

        if state_value in self._state_history_set:
            return

        self._state_history_set.add(state_value)
        self._state_history_queue.append(state_value)
        if len(self._state_history_set) > self.history_size:
            removed_value = self._state_history_queue.popleft()
            self._state_history_set.remove(removed_value)

    def _state_is_in_history(self, state: State):
        return hash(state) in self._state_history_set
