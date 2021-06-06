from fastapi import FastAPI
from pydantic import BaseModel
from packsolver.packsolver2d import PackSolver2d
from packsolver.packsolver3d import PackSolver3d


app = FastAPI()


class Problem2d(BaseModel):
    boxes: list[tuple[int, int]]
    container: tuple[int, int]
    can_rotate: bool


class Problem3d(BaseModel):
    boxes: list[tuple[int, int, int]]
    container: tuple[int, int, int]
    can_rotate: bool


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/solve2d/")
async def solve2d(problem: Problem2d):
    solver = PackSolver2d()
    solver.loadDict(problem.dict())
    return solver.solve()


@app.post("/solve3d/")
async def solve3d(problem: Problem3d):
    solver = PackSolver3d()
    solver.loadDict(problem.dict())
    return solver.solve()
