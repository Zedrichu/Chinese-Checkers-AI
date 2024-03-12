# Class to control the game
# TODO: Refactor the code to make it more readable, proof of concept
from typing import Tuple

from GameProblem import Step
from State import State

STARTING_PLAYER = 1

class GameController:
    def __init__(self, board):
        self.turn = STARTING_PLAYER
        self.board = board
        self.state = State(board=board, player=STARTING_PLAYER, mode=Step.CRAWL, peg=(0, 0))
        # self.players = [Player(i) for i in range(1,3)]

    def end_turn(self):
        self.turn = self.turn % 2 + 1
