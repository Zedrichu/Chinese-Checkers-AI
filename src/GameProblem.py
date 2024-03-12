from functools import cached_property

from State import State


class GameProblem:
    @cached_property
    def initial_state(self):
        raise NotImplementedError

    def player(self, state):
        raise NotImplementedError

    def actions(self, state: State):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def terminal_test(self, state):
        raise NotImplementedError

    def utility(self, state, player):
        raise NotImplementedError
