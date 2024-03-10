import time

from by_book.Board import Board
from by_book.GameProblem import ChineseCheckersGameProblem
from by_book.Player import RandomPlayer, NonRepeatingRandomPlayer, KeyboardHumanPlayer
from by_book.State import State


def main():
    players = [KeyboardHumanPlayer(), NonRepeatingRandomPlayer()]

    board = Board(triangle_size=1)
    initial_state = State(board=board, player_to_move=0)
    problem = ChineseCheckersGameProblem(initial_state=initial_state, players_count=len(players))

    print(initial_state)

    state = initial_state
    while not problem.terminal_test(state):
        player_to_move = players[problem.player(state)]
        move = player_to_move.get_next_move(problem, state)
        if move is None:
            print(f'Player {state.player_to_move} was unable to find a move')
            break

        state = problem.result(state, move)
        print(f'Applied move: {move}')
        print(state)
        time.sleep(1)

    print(f'Utility for player 0: {problem.utility(state, 0)}')
    print(f'Utility for player 1: {problem.utility(state, 1)}')


if __name__ == '__main__':
    main()
