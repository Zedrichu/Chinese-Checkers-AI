from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Action:
    steps: List[Tuple[int, int]]

    def __str__(self):
        return '; '.join((f'({step[0]}, {step[1]})' for step in self.steps))

    def __hash__(self):
        return hash(tuple(self.steps))
