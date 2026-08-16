import csg
import shapes
import ray
import base
import transformation as transform
import utils


def test_csg():
    s1 = shapes.sphere()
    s2 = shapes.cube()
    c = csg.csg("union", s1, s2)
    assert c.operation == "union"
    assert c.left == s1
    assert c.right == s2
    assert s1.parent == c
    assert s2.parent == c

def csg_op(op, lhit, inl, inr, expected):
    result = csg.intersection_allowed(op, lhit, inl, inr)
    assert result == expected


def test_union():
    csg_op("union", True, True, True, False)
    csg_op("union", True, True, False, True)
    csg_op("union", True, False, True, False)
    csg_op("union", True, False, False, True)
    csg_op("union", False, True, True, False)
    csg_op("union", False, True, False, False)
    csg_op("union", False, False, True, True)
    csg_op("union", False, False, False, True)


def test_intersection():
    truth_table = [
            (True, True, True, True),
            (True, True, False, False),
            (True, False, True, True),
            (True, False, False, False),
            (False, True, True, True),
            (False, True, False, True),
            (False, False, True, False),
            (False, False, False, False),
            ]

    for args in truth_table:
        csg_op("intersect", *args)


def test_difference():
    truth_table = [
            (True, True, True, False),
            (True, True, False, True),
            (True, False, True, False),
            (True, False, False, True),
            (False, True, True, True),
            (False, True, False, True),
            (False, False, True, False),
            (False, False, False, False),
            ]

    for args in truth_table:
        csg_op("difference", *args)


def filter_test(op, x1, x2):
    s1 = shapes.sphere()
    s2 = shapes.cube()
    c = csg.csg(op, s1, s2)
    xs = ray.intersections(
            ray.intersection(1, s1),
            ray.intersection(2, s2),
            ray.intersection(3, s1),
            ray.intersection(4, s2)
            )

    result = csg.filter_intersections(c, xs)

    assert result.count == 2
    assert result[0] == xs[x1]
    assert result[1] == xs[x2]

def test_filter_intersections():
    filter_test("union", 0, 3)
    filter_test("intersect", 1, 2)
    filter_test("difference", 0, 1)


def test_local_intersect():
    c = csg.csg("union", shapes.sphere(), shapes.cube())
    r = ray.ray(base.point(0, 2, -5), base.vector(0, 0, 1))
    xs = c.local_intersect(r)
    assert xs.count == 0

def test_local_intersect2():
    s1, s2 = shapes.sphere(), shapes.sphere()
    s2.transform = transform.translation(0, 0, .5)
    c = csg.csg("union", s1, s2)
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    xs = c.local_intersect(r)
    assert xs.count == 2
    assert xs[0].t == 4
    assert xs[0].object == s1
    assert utils.fequals(xs[1].t, 6.5)
    assert xs[1].object == s2
