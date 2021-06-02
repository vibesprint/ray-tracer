import base
import math


def test_point():
    pt = base.point(4, -4, 3)
    assert pt == (4, -4, 3, 1)

def test_vector():
    vec = base.vector(4, -4, 3)
    assert vec == (4, -4, 3, 0)


def test_equals():
    vec1 = base.point(3.2, 3.1, 8.3)
    assert base.equals(vec1, (3.20000001, 3.100000001, 8.3000000001))


def test_add():
    a1 = base.point(3, -2, 5)
    a2 = base.vector(-2, 3, 1)
    assert base.equals(
            base.add(a1, a2),
            (1, 1, 6, 1)
            )


def test_sub():
    a1 = base.point(3, 2, 1)
    a2 = base.point(5, 6, 7)
    assert base.equals(
            base.sub(a1, a2),
            base.vector(-2, -4, -6)
            )

    a2 = base.vector(5, 6, 7)
    assert base.equals(
            base.sub(a1, a2),
            base.point(-2, -4, -6)
            )

def test_negate():
    tup = (1, -2, 3, -4)
    assert base.equals(
            base.negate(tup),
            (-1, 2, -3, 4)
            )

def test_scalar_mul():
    tup = (1, -2, 3, -4)
    assert base.equals(
            base.scalar_mul(tup, 3.5),
            (3.5, -7, 10.5, -14)
            )

def test_scalar_div():
    tup = (1, -2, 3, -4)
    assert base.equals(
            base.scalar_div(tup, 2),
            (0.5, -1, 1.5, -2)
            )


def test_magnitude():
    vec = base.vector(1, 0, 0)
    assert base.magnitude(vec) == 1

    vec = base.vector(0, 1, 0)
    assert base.magnitude(vec) == 1

    vec = base.vector(0, 0, 1)
    assert base.magnitude(vec) == 1

    vec = base.vector(1, 2, 3)
    assert base.magnitude(vec) == math.sqrt(14)

    vec = base.vector(-1, -2, -3)
    assert base.magnitude(vec) == math.sqrt(14)


def test_normalize():
    vec = base.vector(4, 0, 0)
    assert base.equals(
            base.normalize(vec),
            base.vector(1, 0, 0)
            )

    vec = base.vector(1, 2, 3)
    assert base.equals(
            base.normalize(vec),
            base.vector(0.26726, 0.53452, 0.80178)
            )

    norm = base.magnitude(base.normalize(vec))
    assert norm == 1


def test_dot():
    vec1 = base.vector(1, 2, 3)
    vec2 = base.vector(2, 3, 4)
    assert base.dot(vec1, vec2) == 20


def test_cross():
    vec1 = base.vector(1, 2, 3)
    vec2 = base.vector(2, 3, 4)
    assert base.equals(
            base.cross(vec1, vec2),
            base.vector(-1, 2, -1)
            )

    assert base.equals(
            base.cross(vec2, vec1),
            base.vector(1, -2, 1)
            )

