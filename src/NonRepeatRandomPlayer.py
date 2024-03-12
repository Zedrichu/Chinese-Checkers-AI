import random
from typing import Optional

import GameProblem
from Action import Action
from PlayerInterface import PlayerInterface
from State import State


class NonRepeatingRandomPlayer(PlayerInterface):
    """
    A player that will not repeat an action for a given state
    """

    def __init__(self):
        self.previous_actions_and_states = []

    def get_action(self, problem: GameProblem, state: State) -> Optional[Action]:
        state_hash = hash(state)
        possible_actions = []
        for action in problem.actions(state):
            action_and_state_hash = hash(action) ^ state_hash
            if action_and_state_hash not in self.previous_actions_and_states:
                possible_actions.append(action)

        if len(possible_actions) == 0:
            return None

        return random.choice(possible_actions)