from itertools import chain
import pytest
from packsolver.packsolver import PackSolver2d


@pytest.fixture
def solver():
    solver = PackSolver2d()
    solver.load("tests/sample1.toml")
    return solver


@pytest.mark.skip(reason="APIの呼び出しを含むテスト")
def test_boxの配置を最適化する(solver):
    p = [[False] * 5 for _ in range(4)]
    for x, y, w, h in solver.solve():
        for bx in range(x, x + w):
            for by in range(y, y + h):
                assert p[bx][by] is False
                p[bx][by] = True


def test_入力ファイルを読み込む(solver):
    assert [(b.width, b.height) for b in solver.boxes] == [(1, 3), (2, 2)]
    assert (solver.container.width, solver.container.height) == (4, 5)


def test_重複する置き方を除外する(solver):
    q = solver.prepare_symbols()
    assert not q[1][2][1][0].is_number()
    assert q[1][2][1][1] == 0


def test_containerの中に入らない置き方を除外する(solver):
    q = solver.prepare_symbols()
    assert not q[1][2][0][0].is_number()
    assert not q[1][2][0][1].is_number()
    assert (q[1][3][0][0] == 0) ^ (q[1][3][0][1] == 0)
    assert (q[2][2][0][0] == 0) ^ (q[2][2][0][1] == 0)


def test_box同士は重ならないよう制約条件を設定する(solver):
    q = solver.prepare_symbols()
    constaraints = solver.make_board_constraints(q)
    test_case = [[[[0, 0] for k in range(2)] for j in range(5)] for i in range(4)]
    test_case[0][1][0][0] = 1
    test_case[2][3][1][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case))))
    assert all([c.is_satisfied(test_case) for c in constaraints])

    test_case = [[[[0, 0] for k in range(2)] for j in range(5)] for i in range(4)]
    test_case[1][2][0][0] = 1
    test_case[1][2][1][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case))))
    assert any([c.is_satisfied(test_case) is False for c in constaraints])


def test_全てのboxが一度ずつ使われる(solver):
    q = solver.prepare_symbols()
    constaraints = solver.make_once_constraints(q)
    test_case = [[[[0, 0] for k in range(2)] for j in range(5)] for i in range(4)]
    test_case[0][1][0][0] = 1
    test_case[2][3][1][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case))))
    assert all([c.is_satisfied(test_case) for c in constaraints])

    test_case = [[[[0, 0] for k in range(2)] for j in range(5)] for i in range(4)]
    test_case[0][1][0][0] = 1
    test_case[2][3][0][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case))))
    assert any([c.is_satisfied(test_case) is False for c in constaraints])