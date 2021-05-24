import json
from fastapi.testclient import TestClient
import pytest

from packsolver.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_solve():
    response = client.post(
            "/solve2d/",
            headers={"X-Token": "coneofsilence"},
            json={"boxes": [[1, 3], [2, 2]], "container": [4, 5]},
            )
    assert response.status_code == 200
    p = [[False] * 5 for _ in range(4)]
    for x, y, w, h in response.json()["result"]:
        for bx in range(x, x + w):
            for by in range(y, y + h):
                assert p[bx][by] is False
                p[bx][by] = True
