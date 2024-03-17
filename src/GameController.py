import time

from players.NonRepeatRandomPlayer import NonRepeatingRandomPlayer
from players.GraphicsHumanPlayer import GraphicsHumanPlayer
from players.MinimaxAIPlayer import MinimaxAIPlayer
from players.RandomPlayer import RandomPlayer
from game_problem.ChineseCheckers import ChineseCheckers
from game.Graphics import Graphics


def create_player(player_type, depth=6, gui=None, problem=None, max_player=None):
    if player_type == 'human':
        return GraphicsHumanPlayer(gui)
    elif player_type == 'random':
        return RandomPlayer()
    elif player_type == 'nonrepeatrandom':
        return NonRepeatingRandomPlayer()
    elif player_type == 'minimax':
        return MinimaxAIPlayer(problem, max_player, max_depth=depth, verbose=True)
    else:
        raise ValueError("Unsupported player type")


class GameController:
    def __init__(self, verbose=True, use_graphics=True, args=None):
        self.verbose = verbose
        self.use_graphics = use_graphics
        self.problem = ChineseCheckers(triangle_size=3)
        self.gui = Graphics() if use_graphics else None
        self.players = []
        self.handle_game_setup(args)

    def handle_game_setup(self, args):
        if args.first_player or args.second_player is None:
            self.players = [
                MinimaxAIPlayer(self.problem, 1, 6, verbose=self.verbose),
                MinimaxAIPlayer(self.problem, 2, 6, verbose=self.verbose)
            ]
        else:
            player1_depth = args.first_minimax_depth if args.first_player == 'minimax' else None
            player2_depth = args.second_minimax_depth if args.second_player == 'minimax' else None
            player1 = create_player(args.first_player, depth=player1_depth, gui=self.gui,
                                    problem=self.problem, max_player=1)
            player2 = create_player(args.second_player, depth=player2_depth, gui=self.gui,
                                    problem=self.problem, max_player=2)
            self.players.append(player1)
            self.players.append(player2)

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

            if self.gui:
                self.gui.handle_quit()
                self.gui.draw_everything(state)

            turn += 1

        game_duration = time.perf_counter() - game_start_timer
        print(f'Player {state.player} has utility: {self.problem.utility(state, state.player)}')

        print(f'Game elapsed time: {game_duration:0.8f} | Turns = {turn}')
        for i, player in enumerate(self.players):
            print('-----')
            print(f'Player {i + 1} average time: {player.average_time_spent_on_actions:0.8f}')
            print(f'Player {i + 1} move count: {player.moves_count:0.8f}')
            if hasattr(player, 'evaluated_states_count'):
                print(f'Player {i + 1} expanded states: {player.evaluated_states_count}')
