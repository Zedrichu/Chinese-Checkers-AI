from game.Board import Board
from typing import Tuple, Optional


class Step:
    END = 0
    CRAWL = 1
    JUMP = 2

    @staticmethod
    def _validate_end(src: Tuple[int, int], dest: Tuple[int, int]) -> bool:
        """
        Validate if the src and dest coordinates are the same for an END type of movement
        :param src: coordinate tuple of source peg
        :param dest: coordinate tuple of destination peg
        :return: validation boolean result
        """
        if src == dest:
            return True
        return False

    # Validate a crawl type of movement from src coordinates to dest coordinates
    @staticmethod
    def _validate_crawl(board: Board, src: Tuple[int, int], dest: Tuple[int, int]) -> bool:
        x1, y1 = src
        x2, y2 = dest
        delta_x12 = abs(x1 - x2)
        delta_y12 = abs(y1 - y2)
        if (((delta_x12 == 1 and delta_y12 == 0) or
             (delta_x12 == 0 and delta_y12 == 1) or
             abs(x1 + y1 - (x2 + y2)) == 2 and delta_x12 == 1)
                and board.matrix[x2][y2] == 0):
            return True
        return False

    @staticmethod
    def _validate_jump(board: Board, src: Tuple[int, int], dest: Tuple[int, int]) -> bool:
        x1, y1 = src
        x2, y2 = dest
        delta_x12 = abs(x1 - x2)
        delta_y12 = abs(y1 - y2)
        if (((abs(x1 + y1 - (x2 + y2)) == 4 and delta_x12 == 2) or
             (delta_x12 == 2 and delta_y12 == 0) or
             (delta_x12 == 0 and delta_y12 == 2)) and
                board.matrix[(x1 + x2) // 2][(y1 + y2) // 2] != 0 and
                board.matrix[x2][y2] == 0):
            return True
        pass

    @staticmethod
    def validate_head(board: Board, src: Tuple[int, int], dest: Tuple[int, int]) -> Optional[int]:
        if (abs(src[0] - dest[0]) <= 1 and abs(src[1] - dest[1]) <= 1
                and Step._validate_crawl(board, src, dest)):
            return Step.CRAWL
        elif Step._validate_jump(board, src, dest):
            return Step.JUMP
        else:
            return None

    @staticmethod
    def validate_tail(board: Board, src: Tuple[int, int], dest: Tuple[int, int]) -> Optional[int]:
        if Step._validate_end(src, dest):
            return Step.END
        elif Step._validate_jump(board, src, dest):
            return Step.JUMP
        return None
