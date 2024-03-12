import sys

import pygame as pg

from Action import Action
from Step import Step
from typing import List
from Board import Board
from State import State

CIRCLE_RADIUS = 20
TILE_SIZE = 50
OFFSET = TILE_SIZE // 2
RESOLUTION = 720

# Rectangles in which the game is split
# 1. Game
game_rect = pg.Rect(0, 0, RESOLUTION, RESOLUTION - 50)
# 2. Turn
turn_rect = pg.Rect((0, RESOLUTION - 50, 720, 50))
# 3. End-turn button
end_turn_rect = pg.Rect(RESOLUTION - 150, RESOLUTION - 150, 120, 50)


# Method to find the circle that the mouse is hovering over
def find_circle(mouse):
    # Compute the tile position - swap mouse coordinates
    # x and y are swapped because of the way the board is drawn, and board is to be fixed
    x = mouse[1] // TILE_SIZE
    y = mouse[0] // TILE_SIZE

    # Verify if the mouse is inside the circle
    if ((x * TILE_SIZE - CIRCLE_RADIUS < mouse[1] - OFFSET < x * TILE_SIZE + CIRCLE_RADIUS) and
            (y * TILE_SIZE - CIRCLE_RADIUS < mouse[0] - OFFSET < y * TILE_SIZE + CIRCLE_RADIUS)):
        return x, y

    return None


# Method to find if the mouse is hovering over the end-turn button
def find_button(mouse):
    x = mouse[0]
    y = mouse[1]

    # Verify that mouse is inside end-turn button
    if (end_turn_rect.left < x < end_turn_rect.right) and (end_turn_rect.top < y < end_turn_rect.bottom):
        return True

    return None


class Graphics:

    def __init__(self):
        self.pg = pg
        pg.init()
        self.img = pg.image.load('img/wood.jpg')
        self.screen = pg.display.set_mode((RESOLUTION, RESOLUTION))
        self.colors = ['blue', 'red']
        self.start_tile = None
        self.target_tile = None
        self.selected_action = None
        pg.display.set_caption('Chinese Checkers')

    # Method to draw every aspect of the game
    def draw_everything(self, state: State):
        self.screen.blit(self.img, (0, 0))
        self.draw_diamond_board(state.board)
        self.draw_current_player_turn(state.player)
        self.draw_end_turn_button()
        self.pg.display.update()

    def start_listening_to_actions(self):
        self.target_tile = None
        self.selected_action = None

    def handle_events(self, state: State, actions: List[Action]):
        for ev in self.pg.event.get():

            if ev.type == self.pg.QUIT:
                self.pg.quit()
                sys.exit(0)

            # Method to draw all components of the game based on state
            self.draw_everything(state)

            # color the outline of circles if mouse is hovering over them
            # if ev.type == pg.MOUSEMOTION: #TODO: Fix hover effect
                # self.hover()
            if ev.type == pg.MOUSEBUTTONDOWN:
                self.click(state, actions)
                self.click_button(state)

    def handle_quit(self):
        for ev in self.pg.event.get():
            if ev.type == self.pg.QUIT:
                self.pg.quit()
                sys.exit()

    # Method to draw circles for each tile in a diamond shape
    def draw_diamond_board(self, board: Board):
        blue = pg.Color(0, 0, 255)
        black = pg.Color(0, 0, 0)
        red = pg.Color(255, 0, 0)
    
        for i in range(board.board_size):
            for j in range(board.board_size):
                if board.matrix[i][j] == 1:
                    pg.draw.circle(self.screen, blue, (j * TILE_SIZE + OFFSET, i * TILE_SIZE + OFFSET), CIRCLE_RADIUS)

                elif board.matrix[i][j] == 0:
                    pg.draw.circle(self.screen, black, (j * TILE_SIZE + OFFSET, i * TILE_SIZE + OFFSET),
                                   CIRCLE_RADIUS, width=4)

                elif board.matrix[i][j] == 2:
                    pg.draw.circle(self.screen, red, (j * TILE_SIZE + OFFSET, i * TILE_SIZE + OFFSET), CIRCLE_RADIUS)

        # peg = self.start_tile
        # if peg is not None:
        #    self.highlight_peg(peg, game.turn)
        #    self.highlight_possible_moves(game.state)

    def draw_current_player_turn(self, turn: int):
        '''
        Draw the turn rectangle with text
        '''
        pg.draw.rect(self.screen, (245, 245, 220), turn_rect)
        font = pg.font.Font(None, 36)
        text = font.render(f"Player {turn}'s turn", True, pg.Color(self.colors[turn - 1]))
        self.screen.blit(text, (270, self.screen.get_height() - 40))

    def draw_end_turn_button(self):
        # TODO: Do hover effect in the same way as for the circles, even hiding it in same method
        mouse = self.pg.mouse.get_pos()
        button_color = (171, 148, 126)
        if end_turn_rect.collidepoint(mouse):  # Check if mouse is hovering
            button_color = (111, 94, 83)
        pg.draw.rect(self.screen, button_color, end_turn_rect, border_radius=100)
        font = pg.font.Font(None, 36)
        text = font.render(f"End turn", True, pg.Color(89, 61, 59))
        text_rect = text.get_rect(center=end_turn_rect.center)
        self.screen.blit(text, text_rect)

    def highlight_peg(self, peg: tuple, turn: int):
        x, y = peg[0], peg[1]
        pg.draw.circle(self.screen, pg.Color(self.colors[turn - 1]),
                       (y * 50 + 25, x * 50 + 25), CIRCLE_RADIUS, 5)
        pg.draw.circle(self.screen, pg.Color('green'),
                       (self.start_tile[1] * 50 + 25, self.start_tile[0] * 50 + 25), 22, 5)

    def highlight_possible_moves(self, src: State):
        return None
        # x, y = src[0], src[1]
        # for move_coords in np.ndindex(self.board.matrix.shape):
        #     if ChineseCheckers.actions(self.board, state=src):
        #         pg.draw.circle(self.screen, pg.Color('white'),
        #                        (move_coords[1] * 50 + 25, move_coords[0] * 50 + 25),CIRCLE_RADIUS, 5)

    def is_move_ready(self):
        return self.selected_action is not None

    # Method is not used in the current version of the game
    def click(self, state: State, actions: List[Action]):
        mouse = self.pg.mouse.get_pos()
        pair = find_circle(mouse)

        if pair is None or not state.board.within_bounds((pair[0], pair[1])):
            return

        i, j = pair

        print(f'Clicked on tile: {i, j}')
        if state.board.matrix[i][j] == state.player:
            self.start_tile = (i, j)
            print(f'Start tile: {self.start_tile}')

        if state.board.matrix[i][j] == 0 and self.start_tile is not None:
            self.target_tile = (i, j)
            print(f'Target tile: {self.target_tile}')

            start = self.start_tile
            target = self.target_tile
            if target is not None and start is not None:
                for action in actions:
                    if action.src == start and action.dest == target and action.step_type != Step.END:
                        # self.selected_pair = (start, target, action.step_type)
                        self.selected_action = action
                        break

    def get_action(self):
        return self.selected_action

    # if button is clicked change turn in GameController
    def click_button(self, state):
        mouse = self.pg.mouse.get_pos()
        res = find_button(mouse)

        if res is None or not state.mode == Step.JUMP:
            return

        self.selected_action = Action(state.peg, state.peg, Step.END)

    def hover(self, mouse, state: State):
        pair = find_circle(mouse)

        if pair is None or not state.board.within_bounds((pair[0], pair[1])):
            return

        i, j = pair

        # color the outline of circles of the circle of current player's turn
        if state.board.matrix[i][j] == state.player and (i, j) is not self.start_tile:
            pg.draw.circle(self.screen, pg.Color(self.colors[state.player - 1]),
                           (j * 50 + 25, i * 50 + 25), CIRCLE_RADIUS, 5)
            pg.draw.circle(self.screen, pg.Color('yellow'),
                           (j * 50 + 25, i * 50 + 25), 22, 5)
        # don't do anything if tile is not owned by any player, if it is then highlight possible moves
        elif state.board.matrix[i][j] == 0 and self.start_tile is not None:
            pg.draw.circle(self.screen, pg.Color(255, 255, 255),
                           (j * TILE_SIZE + OFFSET, i * TILE_SIZE + OFFSET), CIRCLE_RADIUS)
