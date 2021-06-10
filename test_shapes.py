import shapes
import transformation as transform
import matrix
import base

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
