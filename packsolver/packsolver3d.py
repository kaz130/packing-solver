from itertools import product
from typing import List
from amplify import (
    BinaryPoly,
    BinaryConstraint,
    gen_symbols,
)
from amplify.constraint import less_equal, equal_to

from packsolver.packsolver import PackSolver


class PackSolver3d(PackSolver):
    def prepare_symbols(self) -> List[List[List[List[List[BinaryPoly]]]]]:
        q = gen_symbols(BinaryPoly, self.container.width, self.container.height, self.container.depth, len(self.boxes), 6)
        for x, y, z in product(range(self.container.width), range(self.container.height), range(self.container.depth)):
            for i, b in enumerate(self.boxes):
                for j, p in enumerate(b.all_placements):
                    if x + p[0] > self.container.width or y + p[1] > self.container.height or z + p[2] > self.container.depth:
                        q[x][y][z][i][j] = BinaryPoly(0)
                for j in range(len(b.all_placements), 6):
                    q[x][y][z][i][j] = BinaryPoly(0)
        return q

    def make_board_constraints(self, q: List) -> List[BinaryConstraint]:
        s = dict()
        for p in product(range(self.container.width), range(self.container.height), range(self.container.depth)):
            s[p] = BinaryPoly()

        for i, box in enumerate(self.boxes):
            for j, p in enumerate(list(box.all_placements)):
                for bx, by, bz in product(range(p[0]), range(p[1]), range(p[2])):
                    for cx, cy, cz in product(
                        range(self.container.width - p[0] + 1),
                        range(self.container.height - p[1] + 1),
                        range(self.container.depth - p[2] + 1),
                    ):
                        s[(cx + bx, cy + by, cz + bz)] += q[cx][cy][cz][i][j]
        board_constraints = [less_equal(q, 1) for q in s.values()]
        return board_constraints

    def make_once_constraints(self, q: List) -> List[BinaryConstraint]:
        s = dict()
        for p in product(range(self.container.width), range(self.container.height), range(self.container.depth)):
            s[p] = BinaryPoly()

        once_constraints = [
            equal_to(
                sum(
                    q[x][y][z][i][j]
                    for x in range(self.container.width)
                    for y in range(self.container.height)
                    for z in range(self.container.depth)
                    for j, _ in enumerate(b.all_placements)
                ),
                1,
            )
            for i, b in enumerate(self.boxes)
        ]
        return once_constraints

    def normalize(self, q_values: List) -> List:
        ret = list()
        for x, y, z in product(range(self.container.width), range(self.container.height), range(self.container.depth)):
            for i, b in enumerate(self.boxes):
                for j, p in enumerate(b.all_placements):
                    if q_values[x][y][z][i][j] == 1:
                        ret.append((x, y, z, p[0], p[1], p[2]))
        return ret
