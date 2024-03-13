import GameProblem
import Graphics

from Action import Action
from State import State
from players.Player import Player


class GraphicsHumanPlayer(Player):

    def __init__(self, gui: Graphics):
        self.gui = gui

    def get_action(self, problem: GameProblem, state: State) -> Action:
        actions = list(problem.actions(state))
        self.gui.start_listening_to_actions(actions)
        while not self.gui.is_move_ready():
            self.gui.handle_events(state, actions)
        action = self.gui.get_action()
        return action
