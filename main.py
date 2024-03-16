import argparse

from src.GameController import GameController

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chinese Checkers game with MinMax based AI')

    strategy_group_first_player = parser.add_mutually_exclusive_group()
    strategy_group_first_player.add_argument('--first-minmax', dest='first_minmax', action='store', nargs='?', type=int,
                                             default=6,
                                             help='First player: AI that uses the moves evaluated by MinMax based AI with specified depth.')
    strategy_group_first_player.add_argument('--first-human', dest='first_human', action='store_true',
                                             help='First player: Human player with GUI.')

    strategy_group_second_player = parser.add_mutually_exclusive_group()
    strategy_group_second_player.add_argument('--second-minmax', dest='second_minmax', action='store', nargs='?',
                                              type=int, default=6,
                                              help='Second player: AI that uses the moves evaluated by MinMax based AI with specified depth.')
    strategy_group_second_player.add_argument('--second-rand', dest='second_rand', action='store_true',
                                              help='Second player: AI that uses randomly generated moves.')
    strategy_group_second_player.add_argument('--second-noreprand', dest='second_noreprand', action='store_true',
                                              help='Second player: AI that uses randomly generated moves, but with no repetitions.')

    args = parser.parse_args()

    controller = GameController(verbose=False, use_graphics=False, args=args)
    controller.game_loop()
