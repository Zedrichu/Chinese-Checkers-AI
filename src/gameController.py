from src.player import Player
import pygame

# Class to control the game
# TODO: Refactor the code to make it more readable, proof of concept
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

    # Method to handle mouse click event to select a tile of player's turn
    # TODO: Very bad code, needs to be refactored. But selecting and moving tiles is working
    def click(self, mouse, screen):
        print("Test")
        for i in range(self.board.board_size):
            for j in range(self.board.board_size):
                if (j * 50 + 25 - 20 < mouse[0] < j * 50 + 25 + 20) and (i * 50 + 25 - 20 < mouse[1] < i * 50 + 25 + 20):
                    print(str(self.players[self.turn].player_id))
                    if self.board.board[i][j] == self.turn:
                        # Player selects his own tile as first part of the move
                        self.players[self.turn].select_own_tile(i, j)
                    if self.board.board[i][j] == 0 and self.players[self.turn].selected_tile != None:
                        # Player selects an empty tile as second part of the move
                        self.players[self.turn].select_target_tile(i, j)
                        # If the move is valid, update the board and change the turn
                        selected = self.players[self.turn].selected_tile
                        target = self.players[self.turn].target_tile
                        
                        # if both selected and target tiles are not None
                        if target != None and selected != None:
                            # change the values of target and selected tiles
                            self.board.board[target[0]][target[1]] = self.turn
                            self.board.board[selected[0]][selected[1]] = 0                        



                            return

                        

        
                    
                        

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
    
    

        
    

    

