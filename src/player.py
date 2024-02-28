class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.color = (0, 0, 255) if player_id == 2 else (255, 0, 0)