import pytest
from packsolver.packsolver import PackSolver


@pytest.fixture
def solver():
    solver = PackSolver()
    solver.load("tests/sample1.toml")
    return solver


def test_入力ファイルを読み込む(solver):
    assert [(b.width, b.height) for b in solver.boxes] == [(1, 3), (6, 2)]
    assert (solver.container.width, solver.container.height) == (4, 5)


def test_containerの中に入らない置き方を除外する(solver):
    q = solver.prepare_symbols()
    assert not q[1][3][0][0].is_number()
    assert not q[1][3][0][0].is_number()
    assert q[1][4][0][0] == 0
    assert q[2][3][0][1] == 0
