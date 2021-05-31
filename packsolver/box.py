from itertools import permutations
from typing import Iterable, Optional


class Box:
    def __init__(self, width: int, height: int, depth: Optional[int] = None, can_rotate: bool = True) -> None:
        self.width = width
        self.height = height
        self.depth = depth
        self.can_rotate = can_rotate

    @property
    def all_placements(self) -> Iterable:
        if self.can_rotate:
            if self.depth is None:
                return sorted(set(permutations([self.width, self.height], 2)))
            else:
                return sorted(set(permutations([self.width, self.height, self.depth], 3)))
        else:
            if self.depth is None:
                return [(self.width, self.height)]
            else:
                return [(self.width, self.height, self.depth)]
