from GameController import GameController


if __name__ == "__main__":
    controller = GameController(verbose=False, use_graphics=True)
    controller.game_loop()
