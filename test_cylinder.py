import world
import light
import ray
import base
import color
import shapes
import utils

import math


def cylinder_ray_misses(orig, direction):
    """A ray misses the cylinder"""
    cyl = shapes.cylinder()
    orig = base.point(*orig)
    direction = base.normalize(direction)
    r = ray.ray(orig, direction)
    xs = cyl.local_intersect(r)
    assert xs.count == 0


def test_cylinder_local_intersect():
    cylinder_ray_misses(
            (1, 0, 0),
            (0, 1, 0)
            )

    cylinder_ray_misses(
            (0, 0, 0),
            (0, 1, 0)
            )

    cylinder_ray_misses(
            (0, 0, -5),
            (1, 1, 1)
            )


def cylinder_ray_hits(orig, direction, t1, t2):
    cyl = shapes.cylinder()
    direction = base.normalize(direction)
    r = ray.ray(orig, direction)
    xs = cyl.local_intersect(r)
    assert xs.count == 2
    assert utils.fequals(xs[0].t, t1)
    assert utils.fequals(xs[1].t, t2)


def test_cylinder_intersect_at2():
    cylinder_ray_hits(
            (1, 0, -5),
            (0, 0, 1),
            5, 5
            )

    cylinder_ray_hits(
            (0, 0, -5),
            (0, 0, 1),
            4, 6
            )

    cylinder_ray_hits(
            (.5, 0, -5),
            (.1, 1, 1),
            6.80798, 7.08872
            )


def cylinder_normal_at(pt, normal):
    cyl = shapes.cylinder()
    exp_normal = cyl.local_normal_at(base.point(*pt))
    assert base.equals(base.vector(*normal), exp_normal)

def test_normal_at():
    cylinder_normal_at(
            (1, 0, 0),
            (1, 0, 0)
            )

    cylinder_normal_at(
            (0, 5, -1),
            (0, 0, -1)
            )

    cylinder_normal_at(
            (0, -2, 1),
            (0, 0, 1)
            )

    cylinder_normal_at(
            (-1, 1, 0),
            (-1, 0, 0)
            )


def test_cylinder():
    cyl = shapes.cylinder()
    assert cyl.minimum == float('-inf')
    assert cyl.maximum == float('inf')


def cylinder_truncate_test(orig, direction, count):
    cyl = shapes.cylinder()
    cyl.minimum = 1
    cyl.maximum = 2
    direction = base.normalize(direction)
    r = ray.ray(base.point(*orig), direction)
    xs = cyl.local_intersect(r)
    assert xs.count == count


def test_cylinder_truncation():
    """Intersecting a constrained cylinder"""
    cylinder_truncate_test(
            (0, 1.5, 0),
            (.1, 1, 0),
            0
            )

    cylinder_truncate_test(
            (0, 3, -5),
            (0, 0, 1),
            0
            )

    cylinder_truncate_test(
            (0, 0, -5),
            (0, 0, 1),
            0
            )

    cylinder_truncate_test(
            (0, 2, -5),
            (0, 0, 1),
            0
            )

    cylinder_truncate_test(
            (0, 1, -5),
            (0, 0, 1),
            0
            )

    cylinder_truncate_test(
            (0, 1.5, -2),
            (0, 0, 1),
            2
            )



def test_cylinder2():
    cyl = shapes.cylinder()
    assert cyl.closed == False


def cylinder_intersect_cap(orig, direction, count):
    cyl = shapes.cylinder()
    cyl.minimum = 1
    cyl.maximum = 2
    cyl.closed = True
    direction = base.normalize(direction)
    r = ray.ray(orig, direction)
    xs = cyl.local_intersect(r)
    assert xs.count == count


def test_cylinder3():
    cylinder_intersect_cap(
            (0, 3, 0),
            (0, -1, 0),
            2
            )

    cylinder_intersect_cap(
            (0, 3, -2),
            (0, -1, 2),
            2
            )

    cylinder_intersect_cap(
            (0, 4, -2),
            (0, -1, 1),
            2
            )

    cylinder_intersect_cap(
            (0, 0, -2),
            (0, 1, 2),
            2
            )

    cylinder_intersect_cap(
            (0, -1, -2),
            (0, 1, 1),
            2
            )


def cylinder_normal_caps(point, normal):
    cyl = shapes.cylinder()
    cyl.minimum = 1
    cyl.maximum = 2
    cyl.closed = True
    point = base.point(*point)
    n = cyl.local_normal_at(point)
    normal = base.vector(*normal)
    assert base.equals(normal, n)


def test_cylinder_normal_at():
    cylinder_normal_caps(
            (0, 1, 0),
            (0, -1, 0)
            )

    cylinder_normal_caps(
            (.5, 1, 0),
            (0, -1, 0)
            )

    cylinder_normal_caps(
            (0, 1, .5),
            (0, -1, 0)
            )

    cylinder_normal_caps(
            (0, 2, 0),
            (0, 1, 0)
            )

    cylinder_normal_caps(
            (.5, 2, 0),
            (0, 1, 0)
            )

    cylinder_normal_caps(
            (0, 2, .5),
            (0, 1, 0)
            )
