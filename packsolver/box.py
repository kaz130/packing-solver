from itertools import permutations
from typing import Set, Optional


class Box:
    def __init__(self, width: int, height: int, depth: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.depth = depth

    @property
    def all_placements(self) -> Set:
        if self.depth is None:
            return set(permutations([self.width, self.height], 2))
        else:
            return set(permutations([self.width, self.height, self.depth], 3))
