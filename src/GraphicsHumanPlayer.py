import GameProblem
import Graphics

from Action import Action
from PlayerInterface import PlayerInterface
from State import State


class GraphicsHumanPlayer(PlayerInterface):

    def __init__(self, gui: Graphics):
        self.gui = gui

    def get_action(self, problem: GameProblem, state: State) -> Action:
        actions = list(problem.actions(state))
        self.gui.start_listening_to_actions()
        while not self.gui.is_move_ready():
            self.gui.handle_events(state, actions)
            self.gui.draw_everything(state)
        return self.gui.get_action()
