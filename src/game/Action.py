from typing import Tuple
from dataclasses import dataclass


@dataclass(frozen=True, eq=True, order=True)
class Action:
    src: Tuple[int, int]
    dest: Tuple[int, int]
    step_type: int

    def __str__(self):
        return f"src: {self.src} dest: {self.dest} step_type: {self.step_type}"

    def __hash__(self):
        return hash((self.src, self.dest, self.step_type))
