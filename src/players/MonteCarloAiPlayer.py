import math
import random
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from threading import Event, Thread
from typing import Dict, List

from game.Action import Action
from game.State import State
from game_problem.GameProblem import GameProblem
from game_problem.Heuristic import Heuristic
from players.Player import Player


class ThreadExitException(Exception):
    """Exception to be raised when a thread should exit."""
    pass


@dataclass
class MonteCarloTreeNode:
    state: State
    parent: 'MonteCarloTreeNode' = None
    total_utility_of_playouts: float = 0
    playouts_count: int = 1
    children: List['MonteCarloTreeNode'] = field(default_factory=list)
    action: Action = None
    actions = None


# noinspection PyMethodMayBeStatic
class MonteCarloAiPlayer(Player):
    def __init__(
            self,
            player_id: int,
            utility_heuristic: Heuristic,
            exploitation_vs_exploration_rate: float = math.sqrt(2),
            time_limit_per_move: int = 1,
            title: str = None,
            verbose=False,
    ):
        super().__init__()
        self._player_type = 'MCTS' + f' {title}' if title is not None else ''

        self.player_id = player_id
        self.utility_heuristic = utility_heuristic
        self.exploitation_vs_exploration_rate = exploitation_vs_exploration_rate
        self.time_limit_per_move = time_limit_per_move
        self.verbose = verbose

    def _ucb(self, node: MonteCarloTreeNode) -> float:
        if node.playouts_count == 0:
            return 0

        sqrt_part = math.sqrt(math.log(node.parent.playouts_count) / node.playouts_count)
        return node.total_utility_of_playouts / node.playouts_count + self.exploitation_vs_exploration_rate * sqrt_part

    def _select(self, node: MonteCarloTreeNode) -> MonteCarloTreeNode:
        """select a leaf node in the tree"""
        if node.children:
            unexplored_children = [x for x in node.children if x.playouts_count == 0]
            if len(unexplored_children) > 0:
                return self._select(random.choice(unexplored_children))

            weights = [self._ucb(x) for x in node.children]
            min_value = min(weights)
            if min_value < 0:
                print(f'min ucb = {min_value}')
                sys.stdout.flush()
                weights = [x - min_value for x in weights]
            if sum(weights) == 0:
                selected_child = random.choice(node.children)
            else:
                selected_child = random.choices(node.children, weights, k=1)[0]
            print(f'weights = {weights}')
            sys.stdout.flush()
            return self._select(selected_child)
        else:
            return node

    def _expand(self, problem: GameProblem, node: MonteCarloTreeNode, e: Event = None) -> MonteCarloTreeNode:
        """expand the leaf node by adding all its children states"""
        if not problem.terminal_test(node.state):
            for action in problem.actions(node.state):
                if e and e.is_set():
                    raise ThreadExitException()

                new_state = problem.result(node.state, action)
                child_node = MonteCarloTreeNode(state=new_state, parent=node, action=action)
                node.children.append(child_node)

        return self._select(node)

    def _playout_policy(self, problem: GameProblem, state: State, player: int, actions: List[Action]) -> Action:
        return random.choice(actions)
        # max_score = float('-inf')
        # chosen_action = None
        #
        # for action in actions:
        #     new_state = problem.result(state, action)
        #     score = self.utility_heuristic.eval(new_state, player)
        #     if score > max_score:
        #         max_score = score
        #         chosen_action = action
        #
        # return chosen_action

    def _simulate(self, problem: GameProblem, state: State, e: Event = None):
        simulations = 0
        while not problem.terminal_test(state):
            if e and e.is_set():
                raise ThreadExitException()

            actions = list(problem.actions(state))
            action = self._playout_policy(problem, state, self.player_id, actions)
            state = problem.result(state, action)
            simulations += 1

        utility = problem.utility(state, self.player_id)
        if utility == 0:
            utility = self.utility_heuristic.eval(state, self.player_id)
        return -utility

    def _back_propagate(self, node: MonteCarloTreeNode, utility: float, e: Event = None):
        if e and e.is_set():
            raise ThreadExitException()

        node.total_utility_of_playouts += utility
        node.playouts_count += 1
        if node.parent:
            self._back_propagate(node.parent, -utility, e)

    def _run_thread_task(self, problem: GameProblem, root: MonteCarloTreeNode, e: Event = None):
        simulation_count = 0
        try:
            # Stop when the time limit is exceeded
            while not (e and e.is_set()):
                leaf = self._select(root)
                child_node = self._expand(problem, leaf, e)
                result = self._simulate(problem, child_node.state, e)
                self._back_propagate(child_node, result, e)

                simulation_count += 1
                print(f'Simulation {simulation_count}')
                sys.stdout.flush()
        except ThreadExitException:
            pass

    def get_action(self, problem: GameProblem, state: State) -> Action:
        self._moves_count += 1

        root = MonteCarloTreeNode(state=state)

        e = Event()
        thread = Thread(target=self._run_thread_task, args=(problem, root, e))
        thread.daemon = True

        thread.start()

        # Stop after time limit is exceeded
        thread.join(timeout=self.time_limit_per_move)
        e.set()

        # Extra time for the thread to stop
        thread.join(timeout=0.01)

        best_child = max(root.children, key=lambda x: x.playouts_count)
        return best_child.action
