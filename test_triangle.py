import shapes
import color
import base
import ray

import utils


def test_triangle():
    p1 = base.point(0, 1, 0)
    p2 = base.point(-1, 0, 0)
    p3 = base.point(1, 0, 0)
    t = shapes.triangle(p1, p2, p3)

    assert base.equals(t.p1, p1)
    assert base.equals(t.p2, p2)
    assert base.equals(t.p3, p3)
    assert base.equals(t.e1, base.vector(-1, -1, 0))
    assert base.equals(t.e2, base.vector(1, -1, 0))
    assert base.equals(t.normal, base.vector(0, 0, -1))


def test_tri_local_normal_at():
    p1 = base.point(0, 1, 0)
    p2 = base.point(-1, 0, 0)
    p3 = base.point(1, 0, 0)
    t = shapes.triangle(p1, p2, p3)

    n1 = t.local_normal_at(base.point(0, .5, 0))
    n2 = t.local_normal_at(base.point(-.5, .75, 0))
    n3 = t.local_normal_at(base.point(.5, .25, 0))

    assert base.equals(n1, t.normal)
    assert base.equals(n2, t.normal)
    assert base.equals(n3, t.normal)



def test_tri_local_intersect():
    p1 = base.point(0, 1, 0)
    p2 = base.point(-1, 0, 0)
    p3 = base.point(1, 0, 0)
    t = shapes.triangle(p1, p2, p3)

    r = ray.ray(base.point(0, -1, -2), base.vector(0, 1, 0))
    xs = t.local_intersect(r)
    assert xs.count == 0


def test_tri_local_intersect2():
    p1 = base.point(0, 1, 0)
    p2 = base.point(-1, 0, 0)
    p3 = base.point(1, 0, 0)
    t = shapes.triangle(p1, p2, p3)

    r = ray.ray(base.point(1, 1, -2), base.vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert xs.count == 0


def test_tri_local_intersect3():
    p1 = base.point(0, 1, 0)
    p2 = base.point(-1, 0, 0)
    p3 = base.point(1, 0, 0)
    t = shapes.triangle(p1, p2, p3)

    r = ray.ray(base.point(-1, 1, -2), base.vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert xs.count == 0


def test_tri_local_intersect4():
    p1 = base.point(0, 1, 0)
    p2 = base.point(-1, 0, 0)
    p3 = base.point(1, 0, 0)
    t = shapes.triangle(p1, p2, p3)

    r = ray.ray(base.point(0, -1, -2), base.vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert xs.count == 0


def test_tri_local_intersect5():
    p1 = base.point(0, 1, 0)
    p2 = base.point(-1, 0, 0)
    p3 = base.point(1, 0, 0)
    t = shapes.triangle(p1, p2, p3)

    r = ray.ray(base.point(0, .5, -2), base.vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert xs.count == 1
    assert xs[0].t == 2


def make_smooth_tri():
    p1 = base.point(0, 1, 0)
    p2 = base.point(-1, 0, 0)
    p3 = base.point(1, 0, 0)
    n1 = base.vector(0, 1, 0)
    n2 = base.vector(-1, 0, 0)
    n3 = base.vector(1, 0, 0)

    return shapes.smooth_triangle(p1, p2, p3, n1, n2, n3)


def test_smooth_local_intersect():
    tri = make_smooth_tri()
    r = ray.ray(base.point(-.2, .3, -2), base.vector(0, 0, 1))
    xs = tri.local_intersect(r)
    assert utils.fequals(xs[0].u, .45)
    assert utils.fequals(xs[0].v, .25)


def test_smooth_normal_at():
    tri = make_smooth_tri()
    i = ray.intersection_with_uv(1, tri, .45, .25)
    n = tri.normal_at(base.point(0, 0, 0), i)
    assert base.equals(n, base.vector(-.5547, .83205, 0))
