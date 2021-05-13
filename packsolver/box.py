from itertools import permutations
from typing import Set, Tuple, Optional


class Box:
    def __init__(self, width: int, height: int, depth: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.depth = depth

    @property
    def all_placements2d(self) -> Set[Tuple[int, int]]:
        return set([(self.width, self.height), (self.height, self.width)])

    @property
    def all_placements3d(self) -> Set[Tuple[Optional[int], ...]]:
        return set(permutations([self.width, self.height, self.depth], 3))
