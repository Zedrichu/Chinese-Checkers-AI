from game import Graphics
from game.Action import Action
from game.State import State
from game_problem import GameProblem
from players.Player import Player


class GraphicsHumanPlayer(Player):
    """
    A player that gets the action from the GUI - human interacting with GUI by clicks
    """

    def __init__(self, gui: Graphics):
        super().__init__()
        self._player_type = 'human'
        self.gui = gui

    def get_action(self, problem: GameProblem, state: State) -> Action:
        """
        Decides the action by listening to the GUI
        :param problem: game problem definition
        :param state: the current state of the game
        :return: decided action to take next
        """
        actions = list(problem.actions(state))
        # Start listening to the GUI for the actions
        self.gui.start_listening_to_actions(actions)
        # Wait for the action to be ready
        while not self.gui.is_move_ready():
            # Handle the events on the GUI
            self.gui.handle_events(state, actions)
        # Retrieve the action from the GUI and return it
        action = self.gui.get_action()
        return action
