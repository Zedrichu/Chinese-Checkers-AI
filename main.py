import pygame as pg
from ChineseCheckers import Action
from Board import Board
from GameController import GameController
from Graphics import Graphics

# Initialize gameController
gameController = GameController()
# Extract gui from gameController for simple calls
gui = gameController.gui

# Pygame loop
while True:
    for ev in pg.event.get():
        # get mouse position
        mouse = pg.mouse.get_pos()

        if ev.type == pg.QUIT:
            pg.quit()

        # Method to draw all components of the game based on state
        gui.draw_everything()

        # color the outline of circles if mouse is hovering over them
        if ev.type == pg.MOUSEMOTION:
            gui.hover(mouse, gameController)
        if ev.type == pg.MOUSEBUTTONDOWN:
            gui.click(mouse, gameController)
            gui.click_button(mouse, gameController)

    # updates the frames of the game
    pg.display.update()