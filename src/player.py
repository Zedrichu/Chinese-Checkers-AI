class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.color = (0, 0, 255) if player_id == 2 else (255, 0, 0)
        self.selected_tile = None
        self.target_tile = None

    def select_own_tile(self, x, y):
        self.selected_tile = (x, y)

    def select_target_tile(self, x, y):
        self.target_tile = (x, y)

    def reset_selected(self):
        self.selected_tile = None
        self.target_tile = None
