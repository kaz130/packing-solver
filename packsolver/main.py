from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Problem2d(BaseModel):
    boxes: list[list[int, int], ...]
    container: list[int, int]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/solve2d/")
async def solve2d(problem: Problem2d):
    return {"result": [[0, 0, 1, 3], [1, 0, 2, 2]]}
