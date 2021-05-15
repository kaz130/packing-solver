from typing import Optional


class Container:
    def __init__(self, width: int, height: int, depth: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self._depth = depth

    @property
    def depth(self) -> int:
        if self._depth is None:
            raise Exception
        return self._depth
