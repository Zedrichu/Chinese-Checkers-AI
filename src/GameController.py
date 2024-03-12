import time

from players.GraphicsHumanPlayer import GraphicsHumanPlayer
from players.RandomPlayer import RandomPlayer
from ChineseCheckers import ChineseCheckers
from Graphics import Graphics


class GameController:
    def __init__(self):
        self.problem = ChineseCheckers(triangle_size=3)
        self.gui = Graphics()
        self.players = [GraphicsHumanPlayer(self.gui), RandomPlayer()]

    def game_loop(self):
        state = self.problem.initial_state
        print(state)

        while not self.problem.terminal_test(state):
            action = self.players[state.player - 1].get_action(self.problem, state)
            state = self.problem.result(state, action)

            print(f'Action applied: {action}')
            print(state)

            self.gui.handle_quit()
            self.gui.draw_everything(state)

            time.sleep(0.01)

        print(f'Player {state.player} has utility: {self.problem.utility(state, state.player)}')
