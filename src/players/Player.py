import GameProblem

from abc import ABC, abstractmethod
from State import State
from Action import Action


class Player(ABC):

    @abstractmethod
    def get_action(self, problem: GameProblem, state: State) -> Action:
        raise NotImplementedError
