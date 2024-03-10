from src.Board import Board
from typing import Tuple


class Step:
    END = 0
    CRAWL = 1
    JUMP = 2

    @staticmethod
    def validate_end(board: Board, src: Tuple[int, int], dest: Tuple[int, int]):
        if src == dest:
            return True
        return False

    # Validate move based on available moves in 2D space.
    @staticmethod
    def validate_crawl(board: Board, src: Tuple[int, int], dest: Tuple[int, int]):
        x1, y1 = src
        x2, y2 = dest
        print(f"dest: {x2} {y2} src: {x1} {y1}")
        if (((abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or
             (abs(x1 - x2) == 0 and abs(y1 - y2) == 1) or
             abs(x2 + y2 - (x1 + y1)) == 2 and abs(x2 - x1) == 1)
                and board.matrix[x2][y2] == 0):
            return True
        return False

    @staticmethod
    def validate_jump(board: Board, src: Tuple[int, int], dest: Tuple[int, int]):
        x1, y1 = src
        x2, y2 = dest
        print(f"dest: {x2} {y2} src: {x1} {y1}")
        if (((abs(x2 + y2 - (x1 + y1)) == 4 and abs(x2 - x1) == 2) or
             (abs(x1 - x2) == 2 and abs(y1 - y2) == 0) or
             (abs(x1 - x2) == 0 and abs(y1 - y2) == 2)) and
                board.matrix[(x1 + x2) // 2][(y1 + y2) // 2] != 0):
            return True
        pass

    @staticmethod
    def validate_step(board: Board, src: Tuple[int, int], dest: Tuple[int, int]):
        if (abs(src[0] - dest[0]) <= 1 and abs(src[1] - dest[1]) <= 1
                and Step.validate_crawl(board, src, dest)):
            return Step.CRAWL
        elif Step.validate_jump(board, src, dest):
            return Step.JUMP
        elif Step.validate_end(board, src, dest):
            return Step.END
        return None