from itertools import permutations
from typing import Iterable, Optional


class Box:
    def __init__(self, width: int, height: int, depth: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.depth = depth

    @property
    def all_placements(self) -> Iterable:
        if self.depth is None:
            return sorted(set(permutations([self.width, self.height], 2)))
        else:
            return sorted(set(permutations([self.width, self.height, self.depth], 3)))
