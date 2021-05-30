from packsolver.box import Box


def test_boxは幅と高さを持つ():
    box = Box(3, 4)
    assert (box.width, box.height) == (3, 4)


def test_boxは幅と高さと奥行きを持つ():
    box = Box(3, 4, 5)
    assert (box.width, box.height, box.depth) == (3, 4, 5)


def test_平面上のboxの全ての置き方を昇順に取得する():
    box = Box(3, 4)
    assert list(box.all_placements) == [(3, 4), (4, 3)]


def test_boxの全ての置き方を昇順に取得する():
    box = Box(3, 4, 5)
    assert list(box.all_placements) == [(3, 4, 5), (3, 5, 4), (4, 3, 5), (4, 5, 3), (5, 3, 4), (5, 4, 3)]


def test_平面上のboxの全ての置き方を昇順に回転を禁止して取得する():
    box = Box(3, 4, can_rotate=False)
    assert list(box.all_placements) == [(3, 4)]


def test_boxの全ての置き方を昇順に回転を禁止して取得する():
    box = Box(3, 4, 5, can_rotate=False)
    assert list(box.all_placements) == [(3, 4, 5)]
