import sys
import pygame as pg
from typing import List, Optional

from game.Action import Action
from game.Step import Step
from game.Board import Board
from game.State import State

CIRCLE_RADIUS = 25
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
def find_circle(self, mouse, board_size: int):
    # Compute the tile position - swap mouse coordinates
    # x and y are swapped because of the way the board is drawn, and board is to be fixed
    for i in range(board_size):
        for j in range(board_size):
            # Calculate the center of each circle
            center_position = self.get_center_position(i, j)

            # Calculate the distance between the mouse and the center of the circle
            distance = ((mouse[0] - center_position[0]) ** 2 + (mouse[1] - center_position[1]) ** 2) ** 0.5

            # If the distance is less than or equal to the radius of the circle, return the coordinates of the circle
            if distance <= CIRCLE_RADIUS:
                return i, j
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
    """
    Class that represents the graphics of the game
    """
    def __init__(self):
        self.pg = pg
        pg.init()
        self.img = pg.image.load('img/wood.jpg')
        self.screen = pg.display.set_mode((RESOLUTION, RESOLUTION))
        self.colors = ['blue', 'red']
        self.start_tile = None
        self.target_tile = None
        self.selected_action: Optional[Action] = None
        pg.display.set_caption('Chinese Checkers')

    # Method to draw every aspect of the game
    def draw_everything(self, state: State):
        self.screen.blit(self.img, (0, 0))
        self.draw_diamond_board(state.board)
        self.draw_current_player_turn(state.player)
        self.draw_end_turn_button()
        self.pg.display.update()

    def start_listening_to_actions(self, actions: List[Action]):
        self.target_tile = None
        self.selected_action = None

    def handle_events(self, state: State, actions: List[Action]):
        for ev in self.pg.event.get():

            if ev.type == self.pg.QUIT:
                self.pg.quit()
                sys.exit(0)

            # Method to draw all components of the game based on state
            self.draw_everything(state)
            self.highlight_possible_moves(actions)

            # color the outline of circles if mouse is hovering over them
            if ev.type == pg.MOUSEMOTION:
                self.hover(state)
            if ev.type == pg.MOUSEBUTTONDOWN:
                self.click(state, actions)
                self.click_button(state)
            self.pg.display.update()

    def handle_quit(self):
        for ev in self.pg.event.get():
            if ev.type == self.pg.QUIT:
                self.pg.quit()
                sys.exit(0)

    # Method get circle center position
    def get_center_position(self, i, j):
        x = ((RESOLUTION // 2 + (i + j) * TILE_SIZE + OFFSET * 2) - RESOLUTION // 2)
        y = (RESOLUTION // 2 + (i - j) * TILE_SIZE) - OFFSET
        return x, y

    # Method to draw circles for each tile in a diamond shape
    def draw_diamond_board(self, board: Board):
        blue = pg.Color(0, 0, 255)
        black = pg.Color(0, 0, 0)
        red = pg.Color(255, 0, 0)

        for i in range(board.board_size):
            for j in range(board.board_size):

                # Defining center for each circle, to gain a diamond shape
                center_position = self.get_center_position(i, j)

                if board.matrix[i][j] == 1:
                    pg.draw.circle(surface=self.screen,
                                   color=blue,
                                   center=center_position,
                                   radius=CIRCLE_RADIUS)

                elif board.matrix[i][j] == 0:

                    # TODO: draw outline of the starting tiles of each player, in their respective color
                    pg.draw.circle(surface=self.screen,
                                   color=black,
                                   center=center_position,
                                   radius=CIRCLE_RADIUS,
                                   width=4)

                elif board.matrix[i][j] == 2:
                    pg.draw.circle(surface=self.screen,
                                   color=red,
                                   center=center_position,
                                   radius=CIRCLE_RADIUS)

                if self.start_tile is not None:
                    self.highlight_selected_peg()

    def draw_current_player_turn(self, turn: int):
        """
        Draw the turn rectangle with text
        """
        rectangle_color = (245, 245, 220)
        rectangle_text = f"Player {turn}'s turn"
        player_color = pg.Color(self.colors[turn - 1])

        pg.draw.rect(self.screen, rectangle_color, turn_rect)
        font = pg.font.Font(None, 36)
        text = font.render(rectangle_text, True, player_color)
        self.screen.blit(text, (270, self.screen.get_height() - 40))

    def draw_end_turn_button(self):
        """
        Draw the end turn button with text
        """
        button_color_normal = (171, 148, 126)
        button_color_hover = (111, 94, 83)
        text_color = (89, 61, 59)
        button_text = f"End turn"

        mouse = self.pg.mouse.get_pos()
        button_color = button_color_normal
        if end_turn_rect.collidepoint(mouse):  # Check if mouse is hovering
            button_color = button_color_hover

        pg.draw.rect(self.screen, button_color, end_turn_rect, border_radius=100)
        font = pg.font.Font(None, 36)
        text = font.render(button_text, True, text_color)
        text_rect = text.get_rect(center=end_turn_rect.center)
        self.screen.blit(text, text_rect)

    def highlight_selected_peg(self):
        center_position = self.get_center_position(self.start_tile[0], self.start_tile[1])
        pg.draw.circle(surface=self.screen,
                       color=pg.Color('green'),
                       center=center_position,
                    radius=CIRCLE_RADIUS + 2,
                    width=5)

    def highlight_possible_moves(self, actions):
        if self.start_tile is not None:
            for action in actions:
                coords = action.dest
                center_position = self.get_center_position(coords[0], coords[1])
                if action.src == self.start_tile:
                    pg.draw.circle(surface=self.screen,
                                   color=pg.Color('white'),
                                   center=center_position,
                                   radius=CIRCLE_RADIUS,
                                   width=5)

    def is_move_ready(self):
        return self.selected_action is not None

    # Method is not used in the current version of the game
    def click(self, state: State, actions: List[Action]):
        mouse = self.pg.mouse.get_pos()
        pair = find_circle(self, mouse, state.board.board_size)

        if pair is None or not state.board.within_bounds((pair[0], pair[1])):
            return

        i, j = pair

        if state.board.matrix[i][j] == state.player:
            self.start_tile = (i, j)

        if state.board.matrix[i][j] == 0 and self.start_tile is not None:
            self.target_tile = (i, j)

            start = self.start_tile
            target = self.target_tile
            if target is not None and start is not None:
                for action in actions:
                    if action.src == start and action.dest == target and action.step_type != Step.END:
                        self.selected_action = action
                        break

    def get_action(self):
        self.start_tile = None
        if (self.selected_action is not None and
                self.selected_action.step_type == Step.JUMP):
            self.start_tile = self.target_tile
        self.target_tile = None
        return self.selected_action

    # if button is clicked change turn in GameController
    def click_button(self, state):
        mouse = self.pg.mouse.get_pos()
        res = find_button(mouse)

        if res is None or not state.mode == Step.JUMP:
            return

        self.selected_action = Action(state.peg, state.peg, Step.END)

    def hover(self, state: State):
        pair = find_circle(self,self.pg.mouse.get_pos(), state.board.board_size)

        if pair is None or not state.board.within_bounds((pair[0], pair[1])):
            return

        i, j = pair
        center_position = self.get_center_position(i, j)

        # color the outline of circles of the circle of current player's turn
        if state.board.matrix[i][j] == state.player and (i, j) is not self.start_tile:
            pg.draw.circle(surface=self.screen,
                           color=pg.Color('yellow'),
                           center=center_position,
                           radius=CIRCLE_RADIUS + 2,
                           width=5)
        # don't do anything if tile is not owned by any player, if it is then highlight possible moves
        elif state.board.matrix[i][j] == 0 and self.start_tile is not None:
            pg.draw.circle(surface=self.screen,
                           color=pg.Color('white'),
                           center=center_position,
                           radius=CIRCLE_RADIUS)

    def draw_end_game(self, player: int, utility: int):
        """
        Draw the end turn button with text
        """
        button_color_normal = (171, 148, 126)
        button_color_hover = (111, 94, 83)
        text_color = (89, 61, 59)
        if utility == 1:
            screen_text = f"Player {player}|{self.colors[player - 1]} wins!"
        else:
            screen_text = f"Player {player}|{self.colors[player - 1]} lost!"

        # Draw the end game screen #TODO: make it look better
