import os
from dotenv import load_dotenv
import toml
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
