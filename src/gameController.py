
import pygame
from State import State
from GameProblem import Step


# Class to control the game
# TODO: Refactor the code to make it more readable, proof of concept
class GameController:
    def __init__(self, board):
        self.turn = 1
        self.board = board
        # self.players = [Player(i) for i in range(1,3)]