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
            ints = []
            self.intersect_caps(r, ints)
            return ray.intersections(*ints)

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

        ints = list()

        y0 = r.origin[1] + t0 * r.direction[1]
        if self.minimum < y0 and y0 < self.maximum:
            ints.append(ray.intersection(t0, self))

        y1 = r.origin[1] + t1 * r.direction[1]
        if self.minimum < y1 and y1 < self.maximum:
            ints.append(ray.intersection(t1, self))

        self.intersect_caps(r, ints)
        return ray.intersections(*ints)


    def check_cap(self, r, t):
        x = r.origin[0] + t * r.direction[0]
        z = r.origin[2] + t * r.direction[2]

        return (x**2 + z**2) <= 1

    def intersect_caps(self, r, ints):
        if not self.closed or utils.fequals(r.direction[1], 0):
            return

        t = (self.minimum - r.origin[1]) / r.direction[1]
        if self.check_cap(r, t):
            ints.append(ray.intersection(t, self))

        t = (self.maximum - r.origin[1]) / r.direction[1]
        if self.check_cap(r, t):
            ints.append(ray.intersection(t, self))





    def local_normal_at(self, pt):
        dist = pt[0]**2 + pt[2]**2

        if dist < 1 and pt[1] >= self.maximum - utils.EPSILON:
            return base.vector(0, 1, 0)

        if dist < 1 and pt[1] <= self.minimum + utils.EPSILON:
            return base.vector(0, -1, 0)

        return base.vector(pt[0], 0, pt[2])
