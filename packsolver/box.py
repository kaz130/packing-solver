from typing import Set, Tuple


class Box:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    @property
    def all_placements(self) -> Set[Tuple[int, int]]:
        return set([(self.width, self.height), (self.height, self.width)])
