import os
from typing import Any, List, MutableMapping
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
        self.loadDict(problem)

    def loadDict(self, problem: MutableMapping[str, Any]) -> None:
        self.boxes = [Box(*b, can_rotate = problem.get("can_rotate", True)) for b in problem["boxes"]]
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
        return self.normalize(q_values)

    @abstractmethod
    def prepare_symbols(self) -> List:
        pass

    @abstractmethod
    def make_board_constraints(self, q: List) -> List[BinaryConstraint]:
        pass

    @abstractmethod
    def make_once_constraints(self, q: List) -> List[BinaryConstraint]:
        pass

    @abstractmethod
    def normalize(self, q_values: List) -> List:
        pass
