import transformation as transform
import matrix
import utils
import base

import math


def test_translation():
    trans = transform.translation(5, -3, 2)
    pt = base.point(-3, 4, 5)
    assert base.equals(
            matrix.mul(trans, pt),
            base.point(2, 1, 7)
            )

def test_vector_not_affected():
    trans = transform.translation(5, -3, 2)
    vt = base.vector(-3, 4, 5)
    assert base.equals(
            matrix.mul(trans, vt),
            vt)


def test_inverse():
    trans = transform.translation(5, -3, 2)
    inv = matrix.inverse(trans)
    p = base.point(-3, 4, 5)
    assert base.equals(
            matrix.mul(inv, p),
            base.point(-8, 7, 3)
            )


def test_scale():
    scale = transform.scale(2, 3, 4)
    pt = base.point(-4, 6, 8)
    assert base.equals(
            matrix.mul(scale, pt),
            base.point(-8, 18, 32)
            )

def test_scale_vector():
    scale = transform.scale(2, 3, 4)
    vt = base.vector(-4, 6, 8)
    assert base.equals(
            matrix.mul(scale, vt),
            base.vector(-8, 18, 32)
            )


def test_scale_inverse():
    scale = transform.scale(2, 3, 4)
    inv = matrix.inverse(scale)
    vect = base.vector(-4, 6, 8)
    assert base.equals(
            matrix.mul(inv, vect),
            base.vector(-2, 2, 2)
            )


def test_reflect():
    scale = transform.scale(-1, 1, 1)
    pt = base.point(2, 3, 4)
    assert base.equals(
            matrix.mul(scale, pt),
            base.point(-2, 3, 4)
            )


def test_rotation_x():
    p = base.point(0, 1, 0)
    half_quarter = transform.rotation_x(math.pi/4)
    full_quarter = transform.rotation_x(math.pi/2)

    assert base.equals(
            matrix.mul(half_quarter, p),
            base.point(0, math.sqrt(2)/2, math.sqrt(2)/2)
            )

    assert base.equals(
            matrix.mul(full_quarter, p),
            base.point(0, 0, 1)
            )

def test_rotation_x_inverse():
    p = base.point(0, 1, 0)
    half_quarter = transform.rotation_x(math.pi/4)
    inv = matrix.inverse(half_quarter)
    assert base.equals(
            matrix.mul(inv, p),
            base.point(0, math.sqrt(2)/2, -math.sqrt(2)/2)
            )


def test_rotation_y():
    p = base.point(0, 0, 1)
    half_quarter = transform.rotation_y(math.pi/4)
    full_quarter = transform.rotation_y(math.pi/2)

    assert base.equals(
            matrix.mul(half_quarter, p),
            base.point(math.sqrt(2)/2, 0, math.sqrt(2)/2)
            )

    assert base.equals(
            matrix.mul(full_quarter, p),
            base.point(1, 0, 0)
            )




def test_rotation_z():
    p = base.point(0, 1, 0)
    half_quarter = transform.rotation_z(math.pi/4)
    full_quarter = transform.rotation_z(math.pi/2)

    assert base.equals(
            matrix.mul(half_quarter, p),
            base.point(-math.sqrt(2)/2, math.sqrt(2)/2, 0)
            )

    assert base.equals(
            matrix.mul(full_quarter, p),
            base.point(-1, 0, 0)
            )

def test_shear_xy():
    shear = transform.shear(1, 0, 0, 0, 0, 0)
    pt = base.point(2, 3, 4)
    assert base.equals(
            transform.apply(shear, pt),
            base.point(5, 3, 4)
            )


def test_shear_xz():
    shear = transform.shear(0, 1, 0, 0, 0, 0)
    pt = base.point(2, 3, 4)
    assert base.equals(
            transform.apply(shear, pt),
            base.point(6, 3, 4)
            )



def test_shear_yx():
    shear = transform.shear(0, 0, 1, 0, 0, 0)
    pt = base.point(2, 3, 4)
    assert base.equals(
            transform.apply(shear, pt),
            base.point(2, 5, 4)
            )



def test_shear_yz():
    shear = transform.shear(0, 0, 0, 1, 0, 0)
    pt = base.point(2, 3, 4)
    assert base.equals(
            transform.apply(shear, pt),
            base.point(2, 7, 4)
            )



def test_shear_zx():
    shear = transform.shear(0, 0, 0, 0, 1, 0)
    pt = base.point(2, 3, 4)
    assert base.equals(
            transform.apply(shear, pt),
            base.point(2, 3, 6)
            )



def test_shear_zy():
    shear = transform.shear(0, 0, 0, 0, 0, 1)
    pt = base.point(2, 3, 4)
    assert base.equals(
            transform.apply(shear, pt),
            base.point(2, 3, 7)
            )


def test_compose():
    p = base.point(1, 0, 1)
    A = transform.rotation_x(math.pi/2)
    B = transform.scale(5, 5, 5)
    C = transform.translation(10, 5, 7)

    res = transform.apply(A, p)
    assert base.equals(
            res,
            base.point(1, -1, 0)
            )

    res = transform.apply(B, res)
    assert base.equals(
            res,
            base.point(5, -5, 0)
            )

    res = transform.apply(C, res)
    assert base.equals(
            res,
            base.point(15, 0, 7)
            )

    chained = transform.compose(C, B, A)
    res = transform.apply(chained, p)
    assert base.equals(
            res,
            base.point(15, 0, 7)
            )


def test_view_transform():
    """the matrix for default orientation"""
    frm = base.point(0, 0, 0)
    to = base.point(0, 0, -1)
    up = base.vector(0, 1, 0)
    t = transform.view_transform(frm, to, up)
    assert matrix.equals(
            t,
            matrix.identity_matrix()
            )

def test_view_transform2():
    """view transformation matrix when looking in the positive z direction"""
    frm = base.point(0, 0, 0)
    to = base.point(0, 0, 1)
    up = base.vector(0, 1, 0)
    t = transform.view_transform(frm, to, up)
    assert matrix.equals(
            t,
            transform.scale(-1, 1, -1)
            )

def test_view_transform3():
    """The view transform moves the world"""
    frm = base.point(0, 0, 8)
    to = base.point(0, 0, 0)
    up = base.vector(0, 1, 0)
    t = transform.view_transform(frm, to, up)
    assert matrix.equals(
            t,
            transform.translation(0, 0, -8)
            )

def test_view_transform4():
    """Arbitrary view transformation"""
    frm = base.point(1, 3, 2)
    to = base.point(4, -2, 8)
    up = base.vector(1, 1, 0)
    t = transform.view_transform(frm, to, up)
    assert matrix.equals(
            t,
            matrix.matrix_from(
                [[-0.50709, 0.50709, 0.67612, -2.36643],
                 [0.76772, 0.60609, 0.12122, -2.82843],
                 [-0.35857, 0.59761, -0.71714, 0.00000],
                 [0, 0, 0, 1]]
                )
            )
