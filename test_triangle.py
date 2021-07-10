import shapes
import color
import base
import ray


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
