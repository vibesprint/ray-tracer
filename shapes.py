from collections import namedtuple

import matrix
import base
import transformation as transform

import math


class sphere:
    def __init__(self):
        self.transform = matrix.identity_matrix()
        self.origin = base.point(0, 0, 0)

    def set_transform(self, t):
        self.transform = t


def normal_at(sphere, pt):
    object_point = transform.apply(
            matrix.inverse(sphere.transform),
            pt)

    object_normal = base.sub(object_point, base.point(0, 0, 0))
    world_normal = matrix.mul(
            matrix.transpose(matrix.inverse(sphere.transform)),
            object_normal)
    world_normal[3] = 0
    return base.normalize(world_normal)
