import random

import GameProblem
from Action import Action
from PlayerInterface import PlayerInterface
from State import State


class RandomPlayer(PlayerInterface):

    def get_action(self, problem: GameProblem, state: State) -> Action:
        return random.choice(list(problem.actions(state)))
