from src.gameController import GameController
from src.Board import Board
from src.Graphics import Graphics
from src.GameProblem import Action
import pygame as pg
import sys 
  
  
# initializing the constructor 
pg.init()
  
# screen resolution 
res = (720,720) 
  
# opens up a window 
screen = pg.display.set_mode(res)
pg.display.set_caption('Chinese Checkers')
  
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

gui = Graphics(board)

#print(Action.generate_peg_actions(board, (6, 2)))

# Pygame loop
while True: 
    
    for ev in pg.event.get():
        # fill the screen with white color
        screen.fill((255,255,255))
        mouse = pg.mouse.get_pos()
        if ev.type == pg.QUIT:
            pg.quit()

        # Draw small circles for each tile
        gui.draw_diamond_board(screen)
        gui.draw_turn(gameController.turn, screen)
        
        # color the outline of circles if mouse is hovering over them
        if ev.type == pg.MOUSEMOTION:
            gui.hover(mouse, gameController.turn, screen)
        if ev.type == pg.MOUSEBUTTONDOWN:
            gui.click(mouse, gameController.turn)


         

        
    # superimposing the text onto our button 
    #screen.blit(text , (width/2+50,height/2)) 
      
    # updates the frames of the game 
    pg.display.update()