class GameProblem:

    @property
    def initial_state(self):
        raise NotImplementedError

    @staticmethod
    def player(state):
        raise NotImplementedError

    @staticmethod
    def actions(state):
        raise NotImplementedError

    @staticmethod
    def result(state, action):
        raise NotImplementedError

    @staticmethod
    def terminal_test(state):
        raise NotImplementedError

    @staticmethod
    def utility(state, player: int):
        raise NotImplementedError
