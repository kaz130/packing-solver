from packsolver.box import Box


def test_boxは幅と高さを持つ():
    box = Box(3, 4)
    assert (box.width, box.height) == (3, 4)


def test_boxの全ての置き方を取得する():
    box = Box(3, 4)
    assert box.all_placements == set([(3, 4), (4, 3)])
