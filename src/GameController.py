import time

from game_problem.Heuristic import WeightedHeuristic, SumOfPegsInCornerHeuristic, AverageManhattanToCornerHeuristic, \
    AverageEuclideanToCornerHeuristic, MaxManhattanToCornerHeuristic
from players.GraphicsHumanPlayer import GraphicsHumanPlayer
from players.MinimaxAIPlayer import MinimaxAIPlayer
from players.RandomPlayer import RandomPlayer
from game_problem.ChineseCheckers import ChineseCheckers
from game.Graphics import Graphics


class GameController:
    def __init__(self, verbose=True, use_graphics=True):
        self.verbose = verbose
        self.use_graphics = use_graphics

        self.problem = ChineseCheckers(triangle_size=3)
        self.gui = Graphics() if use_graphics else None
        # self.players = [GraphicsHumanPlayer(self.gui), RandomPlayer()]
        # self.players = [GraphicsHumanPlayer(self.gui), MinimaxAIPlayer(self.problem, 2, 6, verbose=verbose)]

        heuristic1 = WeightedHeuristic([
            (SumOfPegsInCornerHeuristic(), 0.1),
            (AverageManhattanToCornerHeuristic(), 0.3),
            (AverageEuclideanToCornerHeuristic(), 0.4),
            (MaxManhattanToCornerHeuristic(), 0.2),
        ])
        self.players = [
            MinimaxAIPlayer(self.problem, 1, 4, heuristic1, verbose=verbose),
            MinimaxAIPlayer(self.problem, 2, 4, heuristic1, verbose=verbose)
        ]

    def game_loop(self):
        state = self.problem.initial_state()
        game_start_timer = time.perf_counter()

        turn = 0
        while not self.problem.terminal_test(state):
            action = self.players[state.player - 1].get_action(self.problem, state)
            state = self.problem.result(state, action)

            if self.verbose or turn % 10 == 0:
                print(f'Player {state.player} | applied action: {action} | turn = {turn}')
                print(state)
                print('\n\n')

            if self.gui:
                self.gui.handle_quit()
                self.gui.draw_everything(state)

            turn += 1

        print(f'Final state:\n{state}')

        game_duration = time.perf_counter() - game_start_timer
        print(f'Player {state.player} has utility: {self.problem.utility(state, state.player)}')

        print(f'Game elapsed time: {game_duration:0.8f} | Turns = {turn}')
        for i, player in enumerate(self.players):
            print('-----')
            print(f'Player {i + 1} average time: {player.average_time_spent_on_actions:0.8f}')
            print(f'Player {i + 1} move count: {player.moves_count:0.8f}')
            if hasattr(player, 'evaluated_states_count'):
                print(f'Player {i + 1} expanded states: {player.evaluated_states_count}')

        # Wait until quit is pressed
        if self.gui:
            while True:
                self.gui.handle_quit()
