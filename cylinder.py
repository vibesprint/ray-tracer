import shapes
import base
import utils
import ray

import math

class cylinder(shapes.Shape):
    def __init__(self):
        shapes.Shape.__init__(self)
        self.minimum = float('-inf')
        self.maximum = float('inf')
        self.closed = False


    def local_intersect(self, r):
        a = r.direction[0]**2 + r.direction[2]**2

        if utils.fequals(a, 0):
            return ray.intersections()

        b = 2 * r.origin[0] * r.direction[0] + \
                2 * r.origin[2] * r.direction[2]

        c = r.origin[0] ** 2 + r.origin[2]**2 - 1

        disc = b**2 - 4 * a * c

        if disc < 0:
            return ray.intersections()

        t0 = (-b - math.sqrt(disc)) / (2*a)
        t1 = (-b + math.sqrt(disc)) / (2*a)

        if t0 > t1:
            t0, t1 = t1, t0

        ints = tuple()

        y0 = r.origin[1] + t0 * r.direction[1]
        if self.minimum < y0 and y0 < self.maximum:
            ints += (ray.intersection(t0, self), )

        y1 = r.origin[1] + t1 * r.direction[1]
        if self.minimum < y1 and y1 < self.maximum:
            ints += (ray.intersection(t1, self), )

        return ray.intersections(*ints)




    def normal_at(self, pt):
        return base.vector(pt[0], 0, pt[2])
