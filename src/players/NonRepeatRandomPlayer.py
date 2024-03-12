import random
import GameProblem

from typing import Optional
from Action import Action
from State import State
from players.Player import Player


class NonRepeatingRandomPlayer(Player):
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