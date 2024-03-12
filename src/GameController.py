from ChineseCheckers import Step
from MinimaxAI import MinimaxAI
from RandomPlayer import RandomPlayer
import State
from Board import Board
from ChineseCheckers import ChineseCheckers
from Graphics import Graphics


class GameController:
    def __init__(self):
        self.problem = ChineseCheckers(triangle_size=1)
        # self.gui = Graphics(self.problem.initial_state)
        self.players = [RandomPlayer(), RandomPlayer()]

    def game_loop(self):
        state = self.problem.initial_state
        print(state)

        while not self.problem.terminal_test(state):
            action = self.players[state.player - 1].get_action(self.problem, state)
            state = self.problem.result(state, action)

            print(f'Action applied: {action}')
            print(state)

        print(f'Player {state.player} has utility: {self.problem.utility(state, state.player)}')


if __name__ == '__main__':
    GameController().game_loop()