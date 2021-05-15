from typing import List
from amplify import (
    BinaryConstraint,
)

from packsolver.packsolver import PackSolver


class PackSolver3d(PackSolver):
    def prepare_symbols(self) -> List:
        pass

    def make_board_constraints(self, q: List) -> List[BinaryConstraint]:
        pass

    def make_once_constraints(self, q: List) -> List[BinaryConstraint]:
        pass
