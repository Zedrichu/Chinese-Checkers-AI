from typing import Tuple
from dataclasses import dataclass


@dataclass(frozen=True, eq=True, order=True)
class Action:
    """
    Class that represents actions in the game
    """
    src: Tuple[int, int]  # source peg coordinate tuple
    dest: Tuple[int, int]  # destination peg coordinate tuple
    step_type: int  # the type of step (CRAWL, JUMP, END)

    def __str__(self):
        return f"src: {self.src} dest: {self.dest} step_type: {self.step_type}"

    def __hash__(self):
        return hash((self.src, self.dest, self.step_type))
