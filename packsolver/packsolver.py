import os
from itertools import product
from typing import List
from dotenv import load_dotenv
import toml
from amplify import (
    BinaryPoly,
    gen_symbols,
)
from amplify.client import FixstarsClient

from packsolver.box import Box
from packsolver.container import Container


class PackSolver:
    def __init__(self) -> None:
        load_dotenv()
        self.client = FixstarsClient()
        self.client.token = os.getenv("TOKEN")
        self.client.parameters.timeout = 10000
        if os.getenv("https_proxy") is not None:
            self.client.proxy = os.getenv("https_proxy")

    def load(self, problem_file: str) -> None:
        with open(problem_file) as f:
            problem = toml.loads(f.read())

        self.boxes = [Box(b[0], b[1]) for b in problem["boxes"]]
        self.container = Container(problem["container"][0], problem["container"][1])

    def prepare_symbols(self) -> List[List[List[List[BinaryPoly]]]]:
        q = gen_symbols(
            BinaryPoly, self.container.width, self.container.height, len(self.boxes), 2
        )
        for x, y in product(range(self.container.width), range(self.container.height)):
            for i, b in enumerate(self.boxes):
                for j, p in enumerate(b.all_placements):
                    if (
                        x + p[0] > self.container.width
                        or y + p[1] > self.container.height
                    ):
                        q[x][y][i][j] = BinaryPoly(0)
                for j in range(len(b.all_placements), 2):
                    q[x][y][i][j] = BinaryPoly(0)

        return q
