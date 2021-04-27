from packsolver.packsolver import PackSolver


def test_入力ファイルを読み込む():
    solver = PackSolver()
    solver.load("tests/sample1.toml")
    assert [(b.width, b.height) for b in solver.boxes] == [(3, 4), (12, 4), (6, 8)]
    assert (solver.container.width, solver.container.height) == (10, 12)
