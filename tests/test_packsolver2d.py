from itertools import chain
import pytest
from packsolver.box import Box
from packsolver.container import Container
from packsolver.packsolver2d import PackSolver2d


@pytest.fixture
def solver():
    solver = PackSolver2d()
    return solver


@pytest.mark.slow
def test_boxの配置を最適化する(solver):
    solver.load("tests/sample1.toml")
    p = [[False] * 5 for _ in range(4)]
    for x, y, w, h in solver.solve():
        for bx in range(x, x + w):
            for by in range(y, y + h):
                assert p[bx][by] is False
                p[bx][by] = True


def test_入力ファイルを読み込む(solver):
    solver.load("tests/sample1.toml")
    assert [(b.width, b.height) for b in solver.boxes] == [(1, 3), (2, 2)]
    assert (solver.container.width, solver.container.height) == (4, 5)


def test_辞書を読み込む(solver):
    solver.loadDict({"boxes": [[1, 3], [2, 2]], "container": [4, 5]})
    assert [(b.width, b.height) for b in solver.boxes] == [(1, 3), (2, 2)]
    assert (solver.container.width, solver.container.height) == (4, 5)


def test_重複する置き方を除外する(solver):
    solver.boxes = [Box(2, 2)]
    solver.container = Container(5, 6)
    q = solver.prepare_symbols()
    assert not q[3][4][0][0].is_number()
    assert q[3][4][0][1] == 0


def test_containerの中に入らない置き方を除外する(solver):
    solver.boxes = [Box(1, 5)]
    solver.container = Container(4, 8)
    q = solver.prepare_symbols()
    assert not q[2][3][0][0].is_number()
    assert q[2][3][0][1] == 0
    assert q[3][4][0][0] == 0


def test_box同士は重ならないように制約する(solver):
    solver.boxes = [Box(1, 2), Box(5, 6)]
    solver.container = Container(8, 9)
    q = solver.prepare_symbols()
    constaraints = solver.make_board_constraints(q)
    test_case = [[[[0, 0] for _ in range(2)] for _ in range(9)] for _ in range(8)]
    test_case[0][1][0][0] = 1
    test_case[1][2][1][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case))))
    assert all([c.is_satisfied(test_case) for c in constaraints])

    test_case = [[[[0, 0] for _ in range(2)] for _ in range(9)] for _ in range(8)]
    test_case[0][1][0][0] = 1
    test_case[0][2][1][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case))))
    assert any([c.is_satisfied(test_case) is False for c in constaraints])


def test_全てのboxが一度ずつ使われるように制約する(solver):
    solver.boxes = [Box(1, 2), Box(3, 4), Box(5, 6)]
    solver.container = Container(8, 9)
    q = solver.prepare_symbols()
    constaraints = solver.make_once_constraints(q)
    test_case = [[[[0, 0] for _ in range(3)] for _ in range(9)] for _ in range(8)]
    test_case[0][1][0][0] = 1
    test_case[0][2][0][0] = 1
    test_case[0][1][2][0] = 1
    test_case = list(chain.from_iterable(chain.from_iterable(chain.from_iterable(test_case))))
    assert not constaraints[0].is_satisfied(test_case)  # 二度使われる
    assert not constaraints[1].is_satisfied(test_case)  # 使われない
    assert constaraints[2].is_satisfied(test_case)  # 一度だけ使われる
