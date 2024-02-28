from src.player import Player
import pygame

class GameController:
    def __init__(self, board):
        self.turn = 1
        self.board = board
        self.players = [Player(i) for i in range(1,3)]

    def draw_board(self, screen):
        self.board.draw_diamond(screen)
    
    # Method to draw the current player's turn inside a rectangle filling bottom half of the screen
    def draw_turn(self, screen):
        pygame.draw.rect(screen, (60,60,60), (0, screen.get_height()-50, 720, 50))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Player {self.turn}'s turn", True, self.players[self.turn].color)
        screen.blit(text, (270, screen.get_height()-40))

    def hover(self, mouse,screen):
        for i in range(self.board.board_size):
            for j in range(self.board.board_size):
                if (j * 50 + 25 - 20 < mouse[0] < j * 50 + 25 + 20) and (i * 50 + 25 - 20 < mouse[1] < i * 50 + 25 + 20):
                    
                    # color the outline of circles of the circle of current player's turn
                    if self.board.board[i][j] == self.turn:
                        pygame.draw.circle(screen, self.players[self.turn].color, (j * 50 + 25, i * 50 + 25), 15, 5)
                        pygame.draw.circle(screen, pygame.Color('green'), (j * 50 + 25, i * 50 + 25), 20, 5)
                    elif self.board.board[i][j] == 0:
                        #draw cross if tile is not owned by any player
                        pygame.draw.line(screen, pygame.Color('white'), (j * 50 + 5, i * 50 + 5), (j * 50 + 45, i * 50 + 45), 5)
                        pygame.draw.line(screen, pygame.Color('white'), (j * 50 + 45, i * 50 + 5), (j * 50 + 5, i * 50 + 45), 5)
    
    

        
    

    

