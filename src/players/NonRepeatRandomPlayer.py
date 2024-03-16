import random
import time

from game_problem import GameProblem

from typing import Optional
from game.Action import Action
from game.State import State
from players.Player import Player


class NonRepeatingRandomPlayer(Player):
    """
    A player that will not repeat an action for a given state
    """

    def __init__(self):
        super().__init__()
        self.previous_actions_and_states = []

    def get_action(self, problem: GameProblem, state: State) -> Optional[Action]:
        timer = time.perf_counter()

        state_hash = hash(state)
        possible_actions = []
        for action in problem.actions(state):
            action_and_state_hash = hash(action) ^ state_hash
            if action_and_state_hash not in self.previous_actions_and_states:
                possible_actions.append(action)

        if len(possible_actions) == 0:
            return None

        elapsed_time = time.perf_counter() - timer
        self._total_time_spent_on_taking_actions += elapsed_time
        self._moves_count += 1
        return random.choice(possible_actions)
