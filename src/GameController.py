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
        self.players = [GraphicsHumanPlayer(self.gui), MinimaxAIPlayer(self.problem, 2, 6)]

    def game_loop(self):
        state = self.problem.initial_state()
        game_start_timer = time.perf_counter()

        while not self.problem.terminal_test(state):
            action = self.players[state.player - 1].get_action(self.problem, state)
            print(f'Player {state.player} | applied action: {action}')
            state = self.problem.result(state, action)

            print(state)

            time.sleep(0.01)

            self.gui.handle_quit()
            self.gui.draw_everything(state)

            time.sleep(0.01)

        game_duration = time.perf_counter() - game_start_timer
        print(f'Player {state.player} has utility: {self.problem.utility(state, state.player)}')

        print(f'Game elapsed time: {game_duration:0.8f}')
        print(f'Player 1 average time: {self.players[0].average_time_spent_on_actions:0.8f}')
        print(f'Player 2 average time: {self.players[1].average_time_spent_on_actions:0.8f}')
