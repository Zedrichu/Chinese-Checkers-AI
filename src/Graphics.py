import pygame as pg
from src.GameProblem import Step
from src.State import State

CIRCLE_RADIUS = 20
TILE_SIZE = 50
OFFSET = TILE_SIZE // 2
RESOLUTION = 720



# Rectangles in which the game is split
# 1. Game
game_rect = pg.Rect(0, 0, RESOLUTION, RESOLUTION-50)
# 2. Turn
turn_rect = pg.Rect((0, RESOLUTION - 50, 720, 50))
# 3. End-turn button
end_turn_rect = pg.Rect(RESOLUTION-150, RESOLUTION-150, 120, 50)

# Method to find the circle that the mouse is hovering over
def find_circle(mouse):
    # print(f'mouse: {mouse}')

    # Compute the tile position - swap mouse coordinates
    # x and y are swapped because of the way the board is drawn, and board is to be fixed
    x = mouse[1] // TILE_SIZE
    y = mouse[0] // TILE_SIZE

    # print(f'x: {x} y: {y}')

    # Verify if the mouse is inside the circle
    if ((x * TILE_SIZE - CIRCLE_RADIUS < mouse[1] - OFFSET < x * TILE_SIZE + CIRCLE_RADIUS) and
            (y * TILE_SIZE - CIRCLE_RADIUS < mouse[0] - OFFSET < y * TILE_SIZE + CIRCLE_RADIUS)):
        return x, y
    
    # print("Clicked/hovered outside of circle")
    return None

# Method to find if the mouse is hovering over the end-turn button
def find_button(mouse):
    
    x = mouse[0]
    y = mouse[1]

    # Verify that mouse is inside end-turn button
    if (end_turn_rect.left < x < end_turn_rect.right) and (end_turn_rect.top < y < end_turn_rect.bottom):
        return x, y
    
    return None


class Graphics:

    def __init__(self, board, screen):
        self.board = board
        # self.screen = pg.display.set_mode((self.board.board_size * 50, self.board.board_size * 50))
        self.colors = ['blue', 'red']
        self.start_tile = None
        self.target_tile = None

        self.game_container_res = [screen.get_width(), screen.get_height()]

    # Method to draw circles for each tile in a diamond shape
    def draw_diamond_board(self, screen):
        #Background - use img
        #screen.blit(img,)

        #screen.fill((255, 255, 255))
        for i in range(self.board.board_size):
            for j in range(self.board.board_size):
                
                # Blue
                if self.board.matrix[i][j] == 1:
                    pg.draw.circle(screen, (0, 0, 255),
                                   (j * TILE_SIZE + OFFSET, i * TILE_SIZE + OFFSET), CIRCLE_RADIUS)
                    
                # Black
                elif self.board.matrix[i][j] == 0:
                    pg.draw.circle(screen, (0, 0, 0),
                                   (j * TILE_SIZE + OFFSET, i * TILE_SIZE + OFFSET), CIRCLE_RADIUS, width=4)
                
                # Red
                elif self.board.matrix[i][j] == 2:
                    pg.draw.circle(screen, (255, 0, 0),
                                   (j * TILE_SIZE + OFFSET, i * TILE_SIZE + OFFSET), CIRCLE_RADIUS)

    # Draw the turn rectangle with text
    def draw_turn(self, turn: int, screen):
        pg.draw.rect(screen, (245, 245, 220), turn_rect)
        font = pg.font.Font(None, 36)
        text = font.render(f"Player {turn}'s turn", True, pg.Color(self.colors[turn - 1]))
        screen.blit(text, (270, screen.get_height() - 40))
    
    def draw_end_turn(self, screen):
        pg.draw.rect(screen, (170,170,170), end_turn_rect, border_radius=100)
        font = pg.font.Font(None, 36)
        text = font.render(f"End turn", True, pg.Color('black'))
        screen.blit(text, (RESOLUTION-140, RESOLUTION-140))

    def click(self, mouse, turn):
        pair = find_circle(mouse)

        if pair is None or not self.board.within_bounds(pair[0], pair[1]):
            return

        i, j = pair

        print(f'Clicked on tile: {i, j}')
        if self.board.matrix[i][j] == turn:
            self.start_tile = (i, j)

            print(f'Start tile: {self.start_tile}')

        print(self.board.matrix[i][j])
        print(self.start_tile)
        if self.board.matrix[i][j] == 0 and self.start_tile is not None:
            self.target_tile = (i, j)
            print(f'Target tile: {self.target_tile}')

            start = self.start_tile
            target = self.target_tile
            if target is not None and start is not None:
                x1, y1 = start
                x2, y2 = target
                if abs(x1 - x2) > 1 or abs(y1 - y2) > 1:
                    valid = Step.validate_jump(
                        self.board,
                        (start[0], start[1]),
                        (target[0], target[1])
                    )
                else:
                    valid = Step.validate_crawl(
                        self.board,
                        (start[0], start[1]),
                        (target[0], target[1])
                    )
                if valid:
                    self.board.matrix[target[0]][target[1]] = turn
                    self.board.matrix[start[0]][start[1]] = 0
                    self.start_tile = None
                    self.target_tile = None
                    return
    
    # if button is clicked change turn in GameController
    def click_button(self, mouse, gC):
        pair = find_button(mouse)

        if pair is None:
            return
        
        gC.end_turn()

    def hover(self, mouse, turn, screen):
        pair = find_circle(mouse)

        if pair is None or not self.board.within_bounds(pair[0], pair[1]):
            return

        i, j = pair

        # color the outline of circles of the circle of current player's turn
        if self.board.matrix[i][j] == turn:
            pg.draw.circle(screen, pg.Color(self.colors[turn - 1]), (j * 50 + 25, i * 50 + 25), CIRCLE_RADIUS, 5)
            pg.draw.circle(screen, pg.Color('green'), (j * 50 + 25, i * 50 + 25), 22, 5)
        elif self.board.matrix[i][j] == 0:
            # draw cross if tile is not owned by any player
            pg.draw.line(screen, pg.Color('white'), (j * 50 + 5, i * 50 + 5), (j * 50 + 45, i * 50 + 45), 5)
            pg.draw.line(screen, pg.Color('white'), (j * 50 + 45, i * 50 + 5), (j * 50 + 5, i * 50 + 45), 5)
