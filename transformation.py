import matrix
import base
import math

def translation(x, y, z):
    mat = matrix.identity_matrix(4)
    mat[0, 3] = x
    mat[1, 3] = y
    mat[2, 3] = z
    return mat

def scale(x, y, z):
    mat = matrix.identity_matrix(4)
    mat[0, 0] = x
    mat[1, 1] = y
    mat[2, 2] = z
    return mat

def rotation_x(rad):
    mat = matrix.identity_matrix(4)
    sin = math.sin(rad)
    cos = math.cos(rad)
    mat[1, 1] = cos
    mat[1, 2] = -sin
    mat[2, 1] = sin
    mat[2, 2] = cos
    return mat

def rotation_y(r):
    mat = matrix.identity_matrix(4)
    sin = math.sin(r)
    cos = math.cos(r)

    mat[0, 0] = cos
    mat[0, 2] = sin
    mat[2, 0] = -sin
    mat[2, 2] = cos
    return mat

def rotation_z(r):
    mat = matrix.identity_matrix(4)

    sin = math.sin(r)
    cos = math.cos(r)

    mat[0, 0] = cos
    mat[0, 1] = -sin
    mat[1, 0] = sin
    mat[1, 1] = cos
    return mat

def apply(mat, tup):
    return matrix.mul(mat, tup)


def shear(xy, xz, yx, yz, zx, zy):
    mat = matrix.identity_matrix(4)
    mat[0, 1] = xy
    mat[0, 2] = xz
    mat[1, 0] = yx
    mat[1, 2] = yz
    mat[2, 0] = zx
    mat[2, 1] = zy
    return mat


def compose(*mats):
    result = matrix.identity_matrix(mats[0].shape[0])

    for mat in mats:
        result = matrix.mul(result, mat)

    return result

def view_transform(frm, to, up):
    forward = base.normalize(base.sub(to, frm))
    upn = base.normalize(up)
    left = base.cross(forward, upn)
    true_up = base.cross(left, forward)
    orientation = matrix.matrix_from(
            [[left[0], left[1], left[2], 0],
             [true_up[0], true_up[1], true_up[2], 0],
             [-forward[0], -forward[1], -forward[2], 0],
             [0, 0, 0, 1]]
            )
    return matrix.mul(orientation, translation(-frm[0], -frm[1], -frm[2]))
