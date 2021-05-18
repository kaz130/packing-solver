from itertools import chain
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
    for x, y, z, w, h, d in solver.solve():
        for bx in range(x, x + w):
            for by in range(y, y + h):
                for bz in range(z, z + d):
                    assert p[bx][by][bz] is False
                    p[bx][by][bz] = True


def test_入力ファイルを読み込む(solver):
    assert [(b.width, b.height, b.depth) for b in solver.boxes] == [(1, 3, 2), (2, 2, 2), (1, 1, 3)]
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


def test_box同士は重ならないように制約する(solver):
    q = solver.prepare_symbols()
    constaraints = solver.make_board_constraints(q)
    test_case = [[[[[0] * 6 for _ in range(3)] for _ in range(5)] for _ in range(4)] for _ in range(3)]
    test_case[0][0][0][0][0] = 1
    test_case[1][1][1][1][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case)))))
    assert all([c.is_satisfied(test_case) for c in constaraints])

    test_case = [[[[[0] * 6 for _ in range(3)] for _ in range(5)] for _ in range(4)] for _ in range(3)]
    test_case[1][1][1][0][0] = 1
    test_case[1][1][1][1][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case)))))
    assert any([c.is_satisfied(test_case) is False for c in constaraints])


def test_全てのboxが一度ずつ使われるように制約する(solver):
    q = solver.prepare_symbols()
    constaraints = solver.make_once_constraints(q)
    test_case = [[[[[0] * 6 for _ in range(3)] for _ in range(5)] for _ in range(4)] for _ in range(3)]
    test_case[0][0][0][0][0] = 1
    test_case[0][0][0][1][0] = 1
    test_case[0][0][0][2][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case)))))
    assert all([c.is_satisfied(test_case) for c in constaraints])

    test_case = [[[[[0] * 6 for _ in range(3)] for _ in range(5)] for _ in range(4)] for _ in range(3)]
    test_case[0][0][0][0][0] = 1
    test_case[0][0][1][0][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case)))))
    assert any([c.is_satisfied(test_case) is False for c in constaraints])
