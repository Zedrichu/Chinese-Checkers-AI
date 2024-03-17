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
    """
    A player that uses the Minimax algorithm with alpha-beta pruning to decide the next action
    """
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
        self.prob = problem
        self.verbose = verbose
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
        """
        Returns the average time spent on deciding the action
        :return: float number of seconds
        """
        return self._total_time_spent_on_taking_actions / self._moves_count

    def get_action(self, problem: GameProblem, state: State) -> Action:
        """
        Decides the next action to take using the Minimax algorithm with alpha-beta pruning
        :param problem: the game problem definition
        :param state: the current state of the game
        :return: decided action to take next
        """

        timer = time.perf_counter()
        # Get the action from the alpha-beta search query
        action = self.alpha_beta_search(state)

        # Measure the time spent on deciding the action
        elapsed_time = time.perf_counter() - timer
        self._total_time_spent_on_taking_actions += elapsed_time
        self._moves_count += 1
        return action

        # # Prepare thread pool
        # pool = mp.Pool(processes=16)
        # # Apply problem of getting results from thread-pool
        # results = pool.apply_async(self.minimax_alpha_beta,
        #                            args=(state, state.player))
        # pool.close()
        # pool.join()
        # score, action = results.get()

    def alpha_beta_search(self, state: State) -> Action:
        """
        The alpha-beta search algorithm
        :param state: current state of the game
        :return: decided action
        """
        self._add_state_to_history(state)
        alpha = float('-inf')
        beta = float('inf')
        best_val, best_action = self.max_value(state, 0, alpha, beta)
        if self.verbose:
            print(list(self.prob.actions(state)))
        return best_action

    def max_value(self, state: State, depth: int, alpha: float, beta: float) -> Tuple[float, Optional[Action]]:
        """
        The max-value function of the alpha-beta search algorithm
        :param state: the current state of the game
        :param depth: value of the depth of recursion
        :param alpha: alpha value - the best value (min) that the MAX player can guarantee
        :param beta: beta value - the best value (max) that the MIN player can guarantee
        :return: the evaluation and the best action
        """
        if self.cutoff_test(state, depth):
            return self.eval_state(state, self.MAX_PLAYER), None

        valid_actions = list(self.prob.actions(state))
        # Effectiveness of pruning - highly dependent of move ordering - we sort the actions by step type
        # (ends=3, then jumps=2,then crawls=1) - allows to consider the jump ending before the jump backwards (reverse)
        valid_actions.sort(key=lambda x: x.step_type, reverse=True)

        max_eval = float('-inf')
        best_action = None
        tuples = []

        # For each action, calculate the evaluation and the best action
        for action in valid_actions:
            # Get the child state as a result of the action applied
            child = self.prob.result(state, action)
            if self._state_is_in_history(child):
                continue
            # If the game does not change turn after the action - still a MAX node
            if self.prob.player(child) == self.MAX_PLAYER:
                res, sub_action = self.max_value(child, depth + 1, alpha, beta)
            # If the game changes the turn after the action - becomes a MIN node
            else:
                res, sub_action = self.min_value(child, depth + 1, alpha, beta)
            if depth == 0:
                tuples.append((action, res, sub_action))
            # Update the best evaluation and the best action
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
        """
        The min-value function of the alpha-beta search algorithm
        :param state: the current state of the game
        :param depth: depth of recursion
        :param alpha: alpha value - the best value (min) that the MAX player can guarantee
        :param beta: beta value - the best value (max) that the MIN player can guarantee
        :return:
        """
        if self.cutoff_test(state, depth):
            return self.eval_state(state, self.MAX_PLAYER), None

        min_eval = float('inf')
        best_action = None

        valid_actions = list(self.prob.actions(state))
        # Effectiveness of pruning - highly dependent of move ordering - we sort the actions by step type
        # (ends=3, then jumps=2,then crawls=1) - allows to consider the jump ending before the jump backwards (reverse)
        valid_actions.sort(key=lambda x: x.step_type, reverse=True)

        # For each action, calculate the evaluation and the best action
        for action in valid_actions:
            # Get the child state as a result of the action applied
            child = self.prob.result(state, action)
            if self._state_is_in_history(child):
                continue
            # If the game does not change turn after the action - still a MIN node
            if self.prob.player(child) == self.MAX_PLAYER:
                res, sub_action = self.max_value(child, depth + 1, alpha, beta)
            # If the game changes the turn after the action - becomes a MAX node
            else:
                res, sub_action = self.min_value(child, depth + 1, alpha, beta)
            if res < min_eval:
                min_eval = res
                best_action = action
                beta = min(beta, res)
            if min_eval <= alpha:
                break
        return min_eval, best_action

    def eval_state(self, state: State, player: int) -> float:
        """
        Evaluates the state using the heuristic
        :param state: the state to be evaluated
        :param player: the player for which the state is evaluated
        :return: float value of the heuristic evaluation
        """
        self.evaluated_states_count += 1
        if self.prob.terminal_test(state):
            return self.prob.utility(state, player)
        return self.heuristic.eval(state, player)

    def cutoff_test(self, state: State, depth: int) -> bool:
        """
        Checks if the state is terminal or the depth of recursion is reached - cutoff the search
        :param state: the state to be checked
        :param depth: the depth of recursion of the node in the game tree
        :return: flag indicating if the search should be cutoff
        """
        return self.prob.terminal_test(state) or depth == self.max_depth

    def _add_state_to_history(self, state: State):
        """
        Adds the state to the history of the last states
        :param state: the state to be added
        """
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
        """
        Checks if the state is in the history of the last states
        :param state: current state
        :return: flag indicating if the state is in the history
        """
        return hash(state) in self._state_history_set
