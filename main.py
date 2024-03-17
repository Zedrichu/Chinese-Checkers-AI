import argparse
import sys

sys.path.append("src")
from GameController import GameController

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chinese Checkers game with AI and player options.')

    parser.add_argument('--first-player', choices=['human', 'minimax'], required=False,
                        help='Type of the first player.')
    parser.add_argument('--first-minimax-depth', type=int, default=6, required=False,
                        help='Minimax depth for the first player, if applicable.')
    parser.add_argument('--second-player', choices=['random', 'nonrepeatrandom', 'minimax'], required=False,
                        help='Type of the second player.')
    parser.add_argument('--second-minimax-depth', type=int, default=6, required=False,
                        help='Minimax depth for the second player, if applicable.')

    args = parser.parse_args()

    controller = GameController(verbose=False, use_graphics=False, args=args)

    controller.game_loop()
