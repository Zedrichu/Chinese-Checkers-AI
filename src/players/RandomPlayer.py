import random
import time

from game_problem.GameProblem import GameProblem
from game.Action import Action
from game.State import State
from players.Player import Player


class RandomPlayer(Player):
    def get_action(self, problem: GameProblem, state: State) -> Action:
        timer = time.perf_counter()

        action = random.choice(list(problem.actions(state)))

        elapsed_time = time.perf_counter() - timer
        self._total_time_spent_on_taking_actions += elapsed_time
        self._moves_count += 1
        return action

