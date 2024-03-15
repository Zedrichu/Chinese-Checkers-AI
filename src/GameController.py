import time

from players.GraphicsHumanPlayer import GraphicsHumanPlayer
from players.MinimaxAIPlayer import MinimaxAIPlayer
from players.RandomPlayer import RandomPlayer
from game_problem.ChineseCheckers import ChineseCheckers
from game.Graphics import Graphics


class GameController:
    def __init__(self):
        self.problem = ChineseCheckers(triangle_size=3)
        self.gui = Graphics()
        # self.players = [GraphicsHumanPlayer(self.gui), RandomPlayer()]
        self.players = [GraphicsHumanPlayer(self.gui), MinimaxAIPlayer(self.problem, 2, 8)]

    def game_loop(self):
        state = self.problem.initial_state()

        while not self.problem.terminal_test(state):
            action = self.players[state.player - 1].get_action(self.problem, state)
            print(f'Player {state.player} | applied action: {action}')
            state = self.problem.result(state, action)

            print(state)

            self.gui.handle_quit()
            self.gui.draw_everything(state)

            time.sleep(0.01)

        print(f'Player {state.player} has utility: {self.problem.utility(state, state.player)}')
        #TODO: Proper winning graphics
