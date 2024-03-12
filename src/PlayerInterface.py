from abc import ABC, abstractmethod

import GameProblem
from src.State import State
from src.Action import Action


class PlayerInterface(ABC):

    @abstractmethod
    def get_action(self, problem: GameProblem, state: State) -> Action:
        raise NotImplementedError
