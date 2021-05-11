import os
from itertools import product
from typing import List
from dotenv import load_dotenv
import toml
from amplify import (
    BinaryPoly,
    BinaryQuadraticModel,
    BinaryConstraint,
    gen_symbols,
    Solver,
    decode_solution,
)
from amplify.client import FixstarsClient
from amplify.constraint import less_equal, equal_to

from packsolver.box import Box
from packsolver.container import Container


class PackSolver:
    def __init__(self) -> None:
        load_dotenv()
        self.client = FixstarsClient()
        self.client.token = os.getenv("TOKEN")
        self.client.parameters.timeout = 1000
        if os.getenv("https_proxy") is not None:
            self.client.proxy = os.getenv("https_proxy")

    def load(self, problem_file: str) -> None:
        with open(problem_file) as f:
            problem = toml.loads(f.read())

        self.boxes = [Box(b[0], b[1]) for b in problem["boxes"]]
        self.container = Container(problem["container"][0], problem["container"][1])

    def solve(self) -> List:
        solver = Solver(self.client)
        q = self.prepare_symbols()
        constraints = sum(self.make_board_constraints(q)) + sum(self.make_once_constraints(q))
        model = BinaryQuadraticModel(constraints)
        result = solver.solve(model)
        if len(result) == 0:
            raise RuntimeError("Any one of constaraints is not satisfied.")
        solution = result[0]
        values = solution.values
        q_values = decode_solution(q, values)
        ret = list()
        for x, y in product(range(self.container.width), range(self.container.height)):
            for i, b in enumerate(self.boxes):
                for j, p in enumerate(b.all_placements):
                    if q_values[x][y][i][j] == 1:
                        ret.append((x, y, p[0], p[1]))
        return ret

    def prepare_symbols(self) -> List[List[List[List[BinaryPoly]]]]:
        q = gen_symbols(BinaryPoly, self.container.width, self.container.height, len(self.boxes), 2)
        for x, y in product(range(self.container.width), range(self.container.height)):
            for i, b in enumerate(self.boxes):
                for j, p in enumerate(b.all_placements):
                    if x + p[0] > self.container.width or y + p[1] > self.container.height:
                        q[x][y][i][j] = BinaryPoly(0)
                for j in range(len(b.all_placements), 2):
                    q[x][y][i][j] = BinaryPoly(0)
        return q

    def make_board_constraints(self, q: List) -> List[BinaryConstraint]:
        s = dict()
        for p in product(range(self.container.width), range(self.container.height)):
            s[p] = BinaryPoly()

        for i, box in enumerate(self.boxes):
            for j, p in enumerate(box.all_placements):
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
                    for j, _ in enumerate(b.all_placements)
                ),
                1,
            )
            for i, b in enumerate(self.boxes)
        ]
        return once_constraints
