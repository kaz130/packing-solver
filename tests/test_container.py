from packsolver.container import Container


def test_containerは幅と高さを持つ():
    container = Container(10, 12)
    assert (container.width, container.height) == (10, 12)


def test_containerは幅と高さと奥行きを持つ():
    container = Container(10, 12, 15)
    assert (container.width, container.height, container.depth) == (10, 12, 15)
