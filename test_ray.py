import ray
import base
import shapes
import transformation as transform


def test_ray():
    position = base.point(1, 2, 3)
    direction = base.vector(4, 5, 6)
    r = ray.ray(position, direction)

    assert base.equals(
            r.origin,
            position
            )

    assert base.equals(
            r.direction,
            direction
            )


def test_position():
    r = ray.ray(
            base.point(2, 3, 4),
            base.vector(1, 0, 0)
            )

    assert base.equals(
            ray.position(r, 0),
            base.point(2, 3, 4)
            )

    assert base.equals(
            ray.position(r, 1),
            base.point(3, 3, 4)
            )

    assert base.equals(
            ray.position(r, -1),
            base.point(1, 3, 4)
            )

    assert base.equals(
            ray.position(r, 2.5),
            base.point(4.5, 3, 4)
            )


def test_intersect():
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    s = shapes.sphere()
    xs = ray.intersect(s, r)
    assert xs.count == 2
    assert xs[0].t == 4.0
    assert xs[1].t == 6.0


def test_intersect2():
    """Ray intersection at a tangent"""
    r = ray.ray(base.point(0, 1, -5), base.vector(0, 0, 1))
    s = shapes.sphere()
    xs = ray.intersect(s, r)
    assert xs.count == 2
    assert xs[0].t == 5.0
    assert xs[1].t == 5.0

def test_intersect3():
    """Ray misses sphere"""
    r = ray.ray(base.point(0, 2, -5), base.vector(0, 0, 1))
    s = shapes.sphere()
    xs = ray.intersect(s, r)
    assert xs.count == 0

def test_intersect4():
    """Ray originates inside the sphere"""
    r = ray.ray(base.point(0, 0, 0), base.vector(0, 0, 1))
    s = shapes.sphere()
    xs = ray.intersect(s, r)
    assert xs.count == 2
    assert xs[0].t == -1.0
    assert xs[1].t == 1.0


def test_intersect5():
    """Sphere is behind the ray"""
    r = ray.ray(
            base.point(0, 0, 5),
            base.vector(0, 0, 1)
            )

    s = shapes.sphere()
    xs = ray.intersect(s, r)
    assert xs.count == 2
    assert xs[0].t == -6.0
    assert xs[1].t == -4.0


def test_intersection():
    s = shapes.sphere()
    i = ray.intersection(3.5, s)

    assert i.t == 3.5
    assert i.object == s


def test_intersections():
    s = shapes.sphere()
    i1 = ray.intersection(1, s)
    i2 = ray.intersection(2, s)
    ints = ray.intersections(i1, i2)
    assert ints.count == 2
    assert ints[0].t == 1
    assert ints[1].t == 2


def test_intersect6():
    """Intersect sets the object on intersection"""
    s = shapes.sphere()
    r = ray.ray(
            base.point(0, 0, -5),
            base.vector(0, 0, 1)
            )
    ints = ray.intersect(s, r)

    assert ints.count == 2
    assert ints[0].object == s
    assert ints[1].object == s


def test_hit():
    """when all intersections are positive"""
    s = shapes.sphere()
    i1 = ray.intersection(1, s)
    i2 = ray.intersection(2, s)
    ints = ray.intersections(i1, i2)
    assert ray.hit(ints) == i1


def test_hit2():
    """when some intersections have negative value"""
    s = shapes.sphere()
    i1 = ray.intersection(-1, s)
    i2 = ray.intersection(1, s)
    ints = ray.intersections(i1, i2)
    assert ray.hit(ints) == i2

def test_hit3():
    """the hit when all intersections are negative"""
    s = shapes.sphere()
    i1 = ray.intersection(-2, s)
    i2 = ray.intersection(-1, s)
    ints = ray.intersections(i1, i2)
    assert ray.hit(ints) == None


def test_hit4():
    """hit is always the lowest nonnegative value"""
    s = shapes.sphere()
    i1 = ray.intersection(5, s)
    i2 = ray.intersection(7, s)
    i3 = ray.intersection(-3, s)
    i4 = ray.intersection(2, s)
    ints = ray.intersections(i1, i2, i3, i4)
    assert ray.hit(ints) == i4


def test_transform():
    r = ray.ray(base.point(1, 2, 3), base.vector(0, 1, 0))
    m = transform.translation(3, 4, 5)
    r2 = ray.transform(r, m)
    assert base.equals(
            r2.origin,
            base.point(4, 6, 8)
            )
    assert base.equals(
            r2.direction,
            base.vector(0, 1, 0)
            )

def test_transform2():
    """Scaling a ray"""
    r = ray.ray(base.point(1, 2, 3), base.vector(0, 1, 0))
    m = transform.scale(2, 3, 4)
    r2 = ray.transform(r, m)
    assert base.equals(
            r2.origin,
            base.point(2, 6, 12)
            )

    assert base.equals(
            r2.direction,
            base.vector(0, 3, 0)
            )


def test_intersect7():
    """Intersecting a scaled sphere with a ray"""
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    s = shapes.sphere()
    t = transform.scale(2, 2, 2)
    s.set_transform(t)
    ints = ray.intersect(s, r)
    assert ints.count == 2
    assert ints[0].t == 3
    assert  ints[1].t == 7


def test_intersectt8():
    """Intersecting a translated sphere with a ray"""
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    s = shapes.sphere()
    s.set_transform(transform.translation(5, 0, 0))
    ints = ray.intersect(s, r)
    assert ints.count == 0
