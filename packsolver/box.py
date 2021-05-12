from itertools import permutations
from typing import Set, Tuple, Optional, Union


class Box:
    def __init__(self, width: int, height: int, depth: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.depth = depth

    @property
    def all_placements2d(self) -> Set[Tuple[int, int]]:
        return set([(self.width, self.height), (self.height, self.width)])

    @property
    def all_placements(self) -> Union[Set[Tuple[int, int]], Set[Tuple[int, ...]]]:
        if self.depth is None:
            return self.all_placements2d
        else:
            return set(permutations([self.width, self.height, self.depth], 3))
