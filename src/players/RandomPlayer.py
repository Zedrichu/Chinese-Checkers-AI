import random

from game_problem.GameProblem import GameProblem
from game.Action import Action
from game.State import State
from players.Player import Player


class RandomPlayer(Player):

    def get_action(self, problem: GameProblem, state: State) -> Action:
        return random.choice(list(problem.actions(state)))
