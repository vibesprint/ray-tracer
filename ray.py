from collections import namedtuple
import math

import base
import transformation
import matrix

ray = namedtuple("ray", "origin direction")


def position(r, t):
    return base.add(
            r.origin,
            base.scalar_mul(r.direction, t)
            )


class intersection:
    __slots__ = ['t', 'object', 'u', 'v']

    def __init__(self, t, obj, u=None, v=None):
        self.t = t
        self.object = obj
        self.u = u
        self.v = v

class intersections:
    def __init__(self, *intsects):
        self._data = list(intsects)
        self._data.sort(key=lambda i: i.t)
        self.count = len(self._data)

    def __getitem__(self, idx):
        return self._data[idx]

    def __iter__(self):
        return iter(self._data)

def intersect(shape, ray_):
    ray_ = transform(ray_, matrix.inverse(shape.transform))
    return shape.local_intersect(ray_)


def hit(ints):
    for i in ints:
        if i.t >= 0:
            return i
    return None


def transform(r, trans):
    origin = transformation.apply(trans, r.origin)
    direction = transformation.apply(trans, r.direction)
    return ray(origin, direction)


def intersection_with_uv(t, obj, u, v):
    i = intersection(t, obj)
    i.u = u
    i.v = v
    return i
