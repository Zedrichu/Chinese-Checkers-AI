from src.gameController import GameController
from src.board import Board
import pygame 
import sys 
  
  
# initializing the constructor 
pygame.init() 
  
# screen resolution 
res = (720,720) 
  
# opens up a window 
screen = pygame.display.set_mode(res) 
  
# white color 
color = (255,255,255) 
  
# light shade of the button 
color_light = (170,170,170) 
  
# dark shade of the button 
color_dark = (100,100,100) 
  
# stores the width of the 
# screen into a variable 
width = screen.get_width() 
  
# stores the height of the 
# screen into a variable 
height = screen.get_height() 
  
board = Board(3)
gameController = GameController(board)



clicked = False
while True: 
    
    for ev in pygame.event.get(): 
        # fill the screen with white color
        screen.fill((255,255,255))
        mouse = pygame.mouse.get_pos()     
        if ev.type == pygame.QUIT: 
            pygame.quit() 
        
        # Draw small circles for each tile
        gameController.draw_board(screen)
        gameController.draw_turn(screen)
        
        # color the outline of circles if mouse is hovering over them
        if ev.type == pygame.MOUSEMOTION:
            gameController.hover(mouse,screen)

         

        
    # superimposing the text onto our button 
    #screen.blit(text , (width/2+50,height/2)) 
      
    # updates the frames of the game 
    pygame.display.update() 