from itertools import chain
import pytest
from packsolver.packsolver import PackSolver3d


@pytest.fixture
def solver():
    solver = PackSolver2d()
    solver.load("tests/sample2.toml")
    return solver


@pytest.mark.skip(reason="APIの呼び出しを含むテスト")
def test_boxの配置を最適化する(solver):
    p = [[False] * 5 for _ in range(4)] for _ in range(3)]
    for x, y, w, h in solver.solve():
        for bx in range(x, x + w):
            for by in range(y, y + h):
                assert p[bx][by] is False
                p[bx][by] = True


def test_入力ファイルを読み込む(solver):
    assert [(b.width, b.height, b.depth) for b in solver.boxes] == [(1, 3, 2), (2, 2, 2), (1, 1, 5)]
    assert (solver.container.width, solver.container.height) == (3, 4, 5)
