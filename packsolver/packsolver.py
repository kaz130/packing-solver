import os
from itertools import product
from typing import List
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import toml
from amplify import (
    BinaryQuadraticModel,
    BinaryConstraint,
    Solver,
    decode_solution,
)
from amplify.client import FixstarsClient

from packsolver.box import Box
from packsolver.container import Container


class PackSolver(ABC):
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

        self.boxes = [Box(*b) for b in problem["boxes"]]
        self.container = Container(*problem["container"])

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

    @abstractmethod
    def prepare_symbols(self) -> List:
        pass

    @abstractmethod
    def make_board_constraints(self, q: List) -> List[BinaryConstraint]:
        pass

    @abstractmethod
    def make_once_constraints(self, q: List) -> List[BinaryConstraint]:
        pass
