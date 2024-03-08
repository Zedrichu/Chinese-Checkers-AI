class PlayerInterface:
    def __init__(self, player_id: int):
        self.player_id = player_id
        # This logic should belong to Graphics class
        # self.color = (0, 0, 255) if player_id == 2 else (255, 0, 0)