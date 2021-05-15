from itertools import product
from typing import List
from amplify import (
    BinaryPoly,
    BinaryConstraint,
    gen_symbols,
)

from packsolver.packsolver import PackSolver


class PackSolver3d(PackSolver):
    def prepare_symbols(self) -> List[List[List[List[List[BinaryPoly]]]]]:
        q = gen_symbols(BinaryPoly, self.container.width, self.container.height, self.container.depth, len(self.boxes), 6)
        for x, y, z in product(range(self.container.width), range(self.container.height), range(self.container.depth)):
            for i, b in enumerate(self.boxes):
                for j, p in enumerate(b.all_placements3d):
                    if x + p[0] > self.container.width or y + p[1] > self.container.height or z + p[2] > self.container.depth:
                        q[x][y][z][i][j] = BinaryPoly(0)
                for j in range(len(b.all_placements3d), 6):
                    q[x][y][z][i][j] = BinaryPoly(0)
        return q

    def make_board_constraints(self, q: List) -> List[BinaryConstraint]:
        pass

    def make_once_constraints(self, q: List) -> List[BinaryConstraint]:
        pass
