import time

from game_problem.Heuristic import WeightedHeuristic, SumOfPegsInCornerHeuristic, AverageManhattanToCornerHeuristic, \
    AverageEuclideanToCornerHeuristic, MaxManhattanToCornerHeuristic, EnsuredNormalizedHeuristic
from players.GraphicsHumanPlayer import GraphicsHumanPlayer
from players.MinimaxAIPlayer import MinimaxAIPlayer
from players.RandomPlayer import RandomPlayer
from game_problem.ChineseCheckers import ChineseCheckers
from game.Graphics import Graphics


class GameController:
    def __init__(self, verbose=True, use_graphics=True):
        self.verbose = verbose  # Flag to print the state and action applied
        self.use_graphics = use_graphics  # Flag to use the GUI

        self.problem = ChineseCheckers(triangle_size=3)  # Initialize the game problem
        self.gui = Graphics() if use_graphics else None  # Initialize the GUI if the flag is set
        # self.players = [GraphicsHumanPlayer(self.gui), RandomPlayer()]

        heuristic1 = WeightedHeuristic([
            (EnsuredNormalizedHeuristic(SumOfPegsInCornerHeuristic()), 0.1),
            (EnsuredNormalizedHeuristic(AverageManhattanToCornerHeuristic()), 0.3),
            (EnsuredNormalizedHeuristic(AverageEuclideanToCornerHeuristic()), 0.4),
            (EnsuredNormalizedHeuristic(MaxManhattanToCornerHeuristic()), 0.2),
        ])
        # self.players = [GraphicsHumanPlayer(self.gui),
        #                 MinimaxAIPlayer(self.problem, 2, 6, heuristic1, verbose=verbose)]
        self.players = [
            MinimaxAIPlayer(self.problem, 1, 4, heuristic1, verbose=verbose),
            MinimaxAIPlayer(self.problem, 2, 7, heuristic1, verbose=verbose)
        ]

    def game_loop(self):
        """
        Main game loop - takes care of the game state and the players' turns.
        """
        # Initialize the game state with the game problem definition
        state = self.problem.initial_state()
        # Start the game timer to measure the game duration and other performance metrics
        game_start_timer = time.perf_counter()

        turn = 0
        # Loop until the game is over - state becomes terminal
        while not self.problem.terminal_test(state):
            # Retrieve the action from the player currently taking the turn
            action = self.players[state.player - 1].get_action(self.problem, state)
            # Update the state according to the action applied
            state = self.problem.result(state, action)

            # Print the state and action applied once every 10 turns
            if self.verbose or turn % 10 == 0:
                print(f'Player {state.player} | applied action: {action} | turn = {turn}')
                print(state)
                print('\n\n')

            # Connection to the GUI
            if self.gui:
                self.gui.handle_quit()
                self.gui.draw_everything(state)

            turn += 1

        # Print the final state and the utility of the final state
        print(f'Final state:\n{state}')

        game_duration = time.perf_counter() - game_start_timer
        print(f'Player {state.player} has utility: {self.problem.utility(state, state.player)}')

        # Print the game duration and the performance metrics of the players
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
