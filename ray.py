from collections import namedtuple
import math

import base
import transformation

ray = namedtuple("ray", "origin direction")


def position(r, t):
    return base.add(
            r.origin,
            base.scalar_mul(r.direction, t)
            )


intersection = namedtuple("intersection", "t object")

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
    sphere_to_ray = base.sub(ray_.origin, base.point(0, 0, 0))
    a = base.dot(ray_.direction, ray_.direction)
    b = 2 * base.dot(ray_.direction, sphere_to_ray)
    c = base.dot(sphere_to_ray, sphere_to_ray) - 1

    discrim = b*b - 4*a*c

    if discrim < 0:
        return intersections()

    t1 = (-b - math.sqrt(discrim)) / (2*a)
    t2 = (-b + math.sqrt(discrim)) / (2*a)

    return intersections(
            intersection(t1, shape),
            intersection(t2, shape)
            )


def hit(ints):
    for i in ints:
        if i.t >= 0:
            return i
    return None


def transform(r, trans):
    origin = transformation.apply(trans, r.origin)
    direction = transformation.apply(trans, r.direction)
    return ray(origin, direction)
