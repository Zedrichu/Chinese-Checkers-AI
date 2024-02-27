from src.board import Board

board = Board(3)
# board.move()
# print(board)
board.move((4, 0), [(3, 0), (2, 0)])
print(board)
