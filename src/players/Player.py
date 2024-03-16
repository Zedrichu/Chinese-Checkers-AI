from game_problem.GameProblem import GameProblem
from abc import ABC, abstractmethod
from game.State import State
from game.Action import Action


class Player(ABC):

    def __init__(self):
        self._total_time_spent_on_taking_actions = 0.0
        self._moves_count = 0

    @abstractmethod
    def get_action(self, problem: GameProblem, state: State) -> Action:
        raise NotImplementedError

    @property
    def average_time_spent_on_actions(self) -> float:
        return self._total_time_spent_on_taking_actions / self._moves_count
