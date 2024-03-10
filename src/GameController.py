import pygame
from src.ChineseCheckers import Step


# Class to control the game
# TODO: Refactor the code to make it more readable, proof of concept
class GameController:
    def __init__(self, board):
        self.turn = 1
        self.board = board
        # self.players = [Player(i) for i in range(1,3)]

    def end_turn(self):
        self.turn = self.turn % 2 + 1