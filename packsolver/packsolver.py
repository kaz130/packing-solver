import toml

from packsolver.box import Box
from packsolver.container import Container


class PackSolver:
    def __init__(self) -> None:
        pass

    def load(self, problem_file: str) -> None:
        with open(problem_file) as f:
            problem = toml.loads(f.read())

        self.boxes = [Box(b[0], b[1]) for b in problem["boxes"]]
        self.container = Container(problem["container"][0], problem["container"][1])
