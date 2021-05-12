from typing import Optional


class Container:
    def __init__(self, width: int, height: int, depth: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.depth = depth
