import shapes
import transformation as transform
import matrix
import base
import material
import ray

import math


def test_sphere():
    s = shapes.sphere()
    assert matrix.equals(
            s.transform,
            matrix.identity_matrix()
            )

def test_sphere2():
    """Changing sphere's transformation"""
    s = shapes.sphere()
    t = transform.translation(2, 3, 4)
    s.set_transform(t)
    assert matrix.equals(
            s.transform,
            t
            )


def test_normat_at():
    s = shapes.sphere()
    n = shapes.normal_at(s, base.point(1, 0, 0))
    assert base.equals(n, base.vector(1, 0, 0))

def test_normal_at2():
    """Normal at y-axis"""
    s = shapes.sphere()
    n = shapes.normal_at(s, base.point(0, 1, 0))
    assert base.equals(n, base.vector(0, 1, 0))

def test_normal_at3():
    """Normal at z-axis"""
    s = shapes.sphere()
    n = shapes.normal_at(s, base.point(0, 0, 1))
    assert base.equals(n, base.vector(0, 0, 1))

def test_normal_at4():
    """Normal at nonaxial point"""
    s = shapes.sphere()
    const = math.sqrt(3) / 3
    n = shapes.normal_at(s, base.point(const, const, const))
    assert base.equals(n, base.vector(const, const, const))

def test_normal_at5():
    """Normal is normalized"""
    s = shapes.sphere()
    const = math.sqrt(3) / 3
    n = shapes.normal_at(s, base.point(const, const, const))
    assert base.equals(n,
            base.normalize(n)
            )


def test_normal_at6():
    """Normal on translated sphere"""
    s = shapes.sphere()
    s.set_transform(transform.translation(0, 1, 0))
    n = shapes.normal_at(s, base.point(0, 1.70711, -0.70711))
    assert base.equals(n,
            base.vector(0, 0.70711, -0.70711)
            )

def test_normal_at7():
    """Normal on transformed sphere"""
    s = shapes.sphere()
    m = transform.compose(
            transform.scale(1, 0.5, 1),
            transform.rotation_z(math.pi / 5)
            )
    s.set_transform(m)
    const = math.sqrt(2) / 2
    n = shapes.normal_at(s, base.point(0, const, -const))
    assert base.equals(
            n,
            base.vector(0, 0.97014, -0.24254)
            )


def test_reflect():
    v = base.vector(1, -1, 0)
    n = base.vector(0, 1, 0)
    r = shapes.reflect(v, n)
    assert base.equals(r, base.vector(1, 1, 0))

def test_reflect2():
    """Reflecting off a slanted surface"""
    v = base.vector(0, -1, 0)
    const = math.sqrt(2) / 2
    n = base.vector(const, const, 0)
    r = shapes.reflect(v, n)
    assert base.equals(r, base.vector(1, 0, 0))


def test_sphere3():
    """Sphere has default material"""
    s = shapes.sphere()
    m = material.material()
    assert m == s.material


def test_sphere3():
    """Sphere can be assigned a material"""
    s = shapes.sphere()
    m = material.material()
    m.ambient = 1
    s.material = m
    assert s.material == m


def default_shape():

    class TestShape(shapes.Shape):
        def local_intersect(self, ray_):
            self.saved_ray = ray_

        def local_normal_at(self, local_pt):
            return base.vector(local_pt[0], local_pt[1], local_pt[2])

    return TestShape()

def test_shape():
    s = default_shape()
    assert matrix.equals(
            s.transform,
            matrix.identity_matrix()
            )

def test_shape2():
    s = default_shape()
    s.transform = transform.translation(2, 3, 4)
    assert matrix.equals(
            s.transform,
            transform.translation(2, 3, 4)
            )

def test_shape3():
    s = default_shape()
    assert s.material == material.material()

def test_shape4():
    s = default_shape()
    m = material.material()
    m.ambient = 1
    s.material = m
    assert s.material == m

def test_shape5():
    s = default_shape()
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    s.transform = transform.scale(2, 2, 2)
    xs = ray.intersect(s, r)
    assert base.equals(
            s.saved_ray.origin,
            base.point(0, 0, -2.5)
            )
    assert base.equals(
            s.saved_ray.direction,
            base.vector(0, 0, 0.5)
            )


def test_shape6():
    """Intersecting a translated ray with a shape"""
    s = default_shape()
    r = ray.ray(base.point(0, 0, -5), base.vector(0, 0, 1))
    s.transform = transform.translation(5, 0, 0)
    xs = ray.intersect(s, r)
    assert base.equals(
            s.saved_ray.origin,
            base.point(-5, 0, -5)
            )
    assert base.equals(
            s.saved_ray.direction,
            base.vector(0, 0, 1)
            )

def test_shape7():
    """Computing the normal on a translated shape"""
    s = default_shape()
    s.transform = transform.translation(0, 1, 0)
    n = shapes.normal_at(s, base.point(0, 1.70711, -0.70711))
    assert base.equals(n, base.vector(0, 0.70711, -0.70711))

def test_shape8():
    """Computing normal on a transformed shape"""
    s = default_shape()
    s.transform = transform.compose(
            transform.scale(1, 0.5, 1),
            transform.rotation_z(math.pi/5)
            )

    n = shapes.normal_at(s, base.point(0, math.sqrt(2)/2, -math.sqrt(2)/2))
    assert base.equals(
            n,
            base.vector(0, 0.97014, -0.24254)
            )


def test_plane():
    p = shapes.plane()
    n1 = p.local_normal_at(base.point(0, 0, 0))
    n2 = p.local_normal_at(base.point(10, 0, -10))
    n3 = p.local_normal_at(base.point(-5, 0, 150))
    assert base.equals(n1, base.vector(0, 1, 0))
    assert base.equals(n2, base.vector(0, 1, 0))
    assert base.equals(n3, base.vector(0, 1, 0))

def test_plane2():
    """Intersect with a parallel ray"""
    p = shapes.plane()
    r = ray.ray(base.point(0, 10, 0), base.vector(0, 0, 1))
    ints = p.local_intersect(r)
    assert ints.count == 0

def test_plane3():
    """Intersect with a coplanar ray"""
    p = shapes.plane()
    r = ray.ray(base.point(0, 0, 0), base.vector(0, 0, 1))
    xs = p.local_intersect(r)
    assert xs.count == 0

def test_plane4():
    """Ray intersecting from above"""
    p = shapes.plane()
    r = ray.ray(base.point(0, 1, 0), base.vector(0, -1, 0))
    xs = p.local_intersect(r)
    assert xs.count == 1
    xs[0].t == 1
    xs[0].object == p

def test_plane5():
    """Ray intersecting from below"""
    p = shapes.plane()
    r = ray.ray(base.point(0, -1, 0), base.vector(0, 1, 0))
    xs = p.local_intersect(r)
    assert xs.count == 1
    assert xs[0].t == 1
    assert xs[0].object == p
