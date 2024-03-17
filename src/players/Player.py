from game_problem.GameProblem import GameProblem
from abc import ABC, abstractmethod
from game.State import State
from game.Action import Action


class Player(ABC):
    """
    Interface class for a player in a game
    """

    def __init__(self):
        self._total_time_spent_on_taking_actions = 0.0
        self._moves_count = 0
        self._player_type = 'minimax'

    @abstractmethod
    def get_action(self, problem: GameProblem, state: State) -> Action:
        raise NotImplementedError

    @property
    def average_time_spent_on_actions(self) -> float:
        return self._total_time_spent_on_taking_actions / self._moves_count

    @property
    def moves_count(self):
        return int(self._moves_count)

    def to_dict(self) -> dict:
        return {
            'player_type': self._player_type,
            'average_time_per_action': self.average_time_spent_on_actions,
            'move_count': self.moves_count,
            'expanded_states': getattr(self, 'evaluated_states_count', 'Non applicable'),
            'max_depth': getattr(self, 'max_depth', 'Non applicable')
        }
