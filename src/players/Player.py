from game_problem.GameProblem import GameProblem
from abc import ABC, abstractmethod
from game.State import State
from game.Action import Action


class Player(ABC):

    @abstractmethod
    def get_action(self, problem: GameProblem, state: State) -> Action:
        raise NotImplementedError

    