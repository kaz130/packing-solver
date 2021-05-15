import pytest
from packsolver.packsolver3d import PackSolver3d


@pytest.fixture
def solver():
    solver = PackSolver3d()
    solver.load("tests/sample2.toml")
    return solver


@pytest.mark.skip(reason="APIの呼び出しを含むテスト")
def test_boxの配置を最適化する(solver):
    p = [[[False] * 5 for _ in range(4)] for _ in range(3)]
    for x, y, w, h in solver.solve():
        for bx in range(x, x + w):
            for by in range(y, y + h):
                assert p[bx][by] is False
                p[bx][by] = True


def test_入力ファイルを読み込む(solver):
    assert [(b.width, b.height, b.depth) for b in solver.boxes] == [(1, 3, 2), (2, 2, 2), (1, 1, 5)]
    assert (solver.container.width, solver.container.height, solver.container.depth) == (3, 4, 5)


def test_重複する置き方を除外する(solver):
    q = solver.prepare_symbols()
    assert not q[1][2][3][1][0].is_number()
    assert q[1][2][3][1][1] == 0


def test_containerの中に入らない置き方を除外する(solver):
    q = solver.prepare_symbols()
    assert all([not q[0][0][0][0][p].is_number() for p in range(6)])
    assert any([q[1][2][3][0][p] == 0 for p in range(6)])
    assert all([q[2][3][4][0][p] == 0 for p in range(6)])
