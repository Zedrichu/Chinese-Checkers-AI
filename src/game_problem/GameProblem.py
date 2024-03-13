from functools import cached_property
from game.State import State
from abc import ABC, abstractmethod


class GameProblem(ABC):
    """
    Abstract class that represents a problem to be solved by an AI.
    """
    @cached_property
    def initial_state(self):
        raise NotImplementedError

    @abstractmethod
    def player(self, state):
        raise NotImplementedError

    @abstractmethod
    def actions(self, state: State):
        raise NotImplementedError

    @abstractmethod
    def result(self, state, action):
        raise NotImplementedError

    @abstractmethod
    def terminal_test(self, state):
        raise NotImplementedError

    @abstractmethod
    def utility(self, state, player):
        raise NotImplementedError
