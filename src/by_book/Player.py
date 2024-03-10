import random
from abc import ABC, abstractmethod
from typing import Optional

from by_book.GameProblem import GameProblem
from by_book.State import State
from by_book.Action import Action


class Player(ABC):
    @abstractmethod
    def get_next_move(self, problem: GameProblem, state: State) -> Optional[Action]:
        pass


class RandomPlayer(Player):
    def get_next_move(self, problem: GameProblem, state: State) -> Optional[Action]:
        return random.choice(list(problem.actions(state)))


class NonRepeatingRandomPlayer(Player):
    """
    A player that will not repeat an action for a given state
    """

    def __init__(self):
        self.previous_actions_and_states = []

    def get_next_move(self, problem: GameProblem, state: State) -> Optional[Action]:
        state_hash = hash(state)
        possible_actions = []
        for action in problem.actions(state):
            action_and_state_hash = hash(action) ^ state_hash
            if action_and_state_hash not in self.previous_actions_and_states:
                possible_actions.append(action)

        if len(possible_actions) == 0:
            return None

        return random.choice(possible_actions)


class KeyboardHumanPlayer(Player):
    def get_next_move(self, problem: GameProblem, state: State) -> Optional[Action]:
        possible_actions = list(problem.actions(state))
        print('\n'.join(f'{i}:\t{action}' for i, action in enumerate(possible_actions)))
        user_input = int(input("Enter which action to take: "))
        return possible_actions[user_input]


