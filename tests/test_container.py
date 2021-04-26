from packsolver.container import Container


def test_containerは幅と高さを持つ():
    container = Container(10, 12)
    assert (container.width, container.height) == (10, 12)
