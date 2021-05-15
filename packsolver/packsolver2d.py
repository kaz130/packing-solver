from itertools import product
from typing import List
from amplify import (
    BinaryPoly,
    BinaryConstraint,
    gen_symbols,
)
from amplify.constraint import less_equal, equal_to

from packsolver.packsolver import PackSolver


class PackSolver2d(PackSolver):
    def prepare_symbols(self) -> List[List[List[List[BinaryPoly]]]]:
        q = gen_symbols(BinaryPoly, self.container.width, self.container.height, len(self.boxes), 2)
        for x, y in product(range(self.container.width), range(self.container.height)):
            for i, b in enumerate(self.boxes):
                for j, p in enumerate(b.all_placements2d):
                    if x + p[0] > self.container.width or y + p[1] > self.container.height:
                        q[x][y][i][j] = BinaryPoly(0)
                for j in range(len(b.all_placements2d), 2):
                    q[x][y][i][j] = BinaryPoly(0)
        return q

    def make_board_constraints(self, q: List) -> List[BinaryConstraint]:
        s = dict()
        for p in product(range(self.container.width), range(self.container.height)):
            s[p] = BinaryPoly()

        for i, box in enumerate(self.boxes):
            for j, p in enumerate(box.all_placements2d):
                for bx, by in product(range(p[0]), range(p[1])):
                    for cx, cy in product(
                        range(self.container.width - p[0] + 1),
                        range(self.container.height - p[1] + 1),
                    ):
                        s[(cx + bx, cy + by)] += q[cx][cy][i][j]
        board_constraints = [less_equal(q, 1) for q in s.values()]
        return board_constraints

    def make_once_constraints(self, q: List) -> List[BinaryConstraint]:
        s = dict()
        for p in product(range(self.container.width), range(self.container.height)):
            s[p] = BinaryPoly()

        once_constraints = [
            equal_to(
                sum(
                    q[x][y][i][j]
                    for x in range(self.container.width)
                    for y in range(self.container.height)
                    for j, _ in enumerate(b.all_placements2d)
                ),
                1,
            )
            for i, b in enumerate(self.boxes)
        ]
        return once_constraints
