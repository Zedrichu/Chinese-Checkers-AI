import random
import GameProblem

from Action import Action
from State import State
from players.Player import Player


class RandomPlayer(Player):

    def get_action(self, problem: GameProblem, state: State) -> Action:
        return random.choice(list(problem.actions(state)))
