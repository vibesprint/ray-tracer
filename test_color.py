import color


def test_color():
    col = color.color(1, 2, 3)
    assert color.red(col) == 1
    assert color.blue(col) == 3
    assert color.green(col) == 2


def test_add():
    col1 = color.color(1, 2, 3)
    col2 = color.color(3, 4, 5)
    assert color.equals(
            color.add(col1, col2),
            color.color(4, 6, 8)
            )

def test_sub():
    col1 = color.color(0.9, 0.6, 0.75)
    col2 = color.color(0.7, 0.1, 0.25)
    assert color.equals(
            color.sub(col1, col2),
            color.color(0.2, 0.5, 0.5)
            )

def test_scalar_mul():
    col = color.color(0.2, 0.3, 0.4)
    assert color.equals(
            color.scalar_mul(col, 2),
            color.color(0.4, 0.6, 0.8)
            )

def test_hadamard_mul():
    col1 = color.color(1, 0.2, 0.4)
    col2 = color.color(0.9, 1, 0.1)
    assert color.equals(
            color.hadamard_mul(col1, col2),
            color.color(0.9, 0.2, 0.04)
            )
