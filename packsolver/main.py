from fastapi import FastAPI
from pydantic import BaseModel
from packsolver.packsolver2d import PackSolver2d


app = FastAPI()


class Problem2d(BaseModel):
    boxes: list[tuple[int, int]]
    container: tuple[int, int]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/solve2d/")
async def solve2d(problem: Problem2d):
    solver = PackSolver2d()
    solver.loadDict(problem.dict())
    return solver.solve()
