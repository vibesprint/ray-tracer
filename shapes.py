from collections import namedtuple

import matrix
import base
import transformation as transform
import material
import ray
import utils

import math

class Shape:
    def __init__(self):
        self.transform = matrix.identity_matrix()
        self.material = material.material()

    def __eq__(self, other):
        return matrix.equals(self.transform, other.transform) and \
                self.material == other.material

class sphere(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.origin = base.point(0, 0, 0)

    def set_transform(self, t):
        self.transform = t

    def __eq__(self, other):
        return matrix.equals(self.transform, other.transform) and \
                self.material == other.material

    def local_intersect(self, ray_):
        sphere_to_ray = base.sub(ray_.origin, base.point(0, 0, 0))
        a = base.dot(ray_.direction, ray_.direction)
        b = 2 * base.dot(ray_.direction, sphere_to_ray)
        c = base.dot(sphere_to_ray, sphere_to_ray) - 1

        discrim = b*b - 4*a*c

        if discrim < 0:
            return ray.intersections()

        t1 = (-b - math.sqrt(discrim)) / (2*a)
        t2 = (-b + math.sqrt(discrim)) / (2*a)

        return ray.intersections(
                ray.intersection(t1, self),
                ray.intersection(t2, self)
                )

    def local_normal_at(self, local_pt):
        return base.sub(local_pt, base.point(0, 0, 0))



def normal_at(shape, pt):
    local_point = transform.apply(
            matrix.inverse(shape.transform),
            pt)

    local_normal = shape.local_normal_at(local_point)

    world_normal = matrix.mul(
            matrix.transpose(matrix.inverse(shape.transform)),
            local_normal
            )

    world_normal[3] = 0
    return base.normalize(world_normal)

def reflect(vect, normal):
    return base.sub(
            vect,
            base.scalar_mul(
                normal,
                2 * base.dot(vect, normal)
                )
            )


class plane(Shape):
    def __init__(self):
        Shape.__init__(self)

    def local_normal_at(self, local_pt):
        return base.vector(0, 1, 0)

    def local_intersect(self, ray_):
        if utils.fequals(ray_.direction[1], 0):
            return ray.intersections()
        t = -ray_.origin[1]/ray_.direction[1]
        return ray.intersections(
                ray.intersection(t, self)
                )

class glass_sphere(sphere):
    def __init__(self):
        sphere.__init__(self)
        self.material.transparency = 1.0
        self.material.refractive_index = 1.5


class cube(Shape):
    def __init__(self):
        Shape.__init__(self)

    def local_intersect(self, r):
        xtmin, xtmax = self.check_axis(r.origin[0], r.direction[0])
        ytmin, ytmax = self.check_axis(r.origin[1], r.direction[1])
        ztmin, ztmax = self.check_axis(r.origin[2], r.direction[2])

        tmin = max(xtmin, ytmin, ztmin)
        tmax = min(xtmax, ytmax, ztmax)

        if tmin > tmax:
            return ray.intersections()

        return ray.intersections(
                ray.intersection(tmin, self),
                ray.intersection(tmax, self)
                )


    def check_axis(self, orig, direction):
        tmin_numerator = (-1 - orig)
        tmax_numerator = (1 - orig)

        if abs(direction) > utils.EPSILON:
            tmin = tmin_numerator / direction
            tmax = tmax_numerator / direction

        else:
            tmin = tmin_numerator * float('inf')
            tmax = tmax_numerator * float('inf')

        if tmin > tmax:
            tmin, tmax = tmax, tmin

        return tmin, tmax


    def local_normal_at(self, pt):
        maxc = max(abs(i) for i in pt)

        if maxc == abs(pt[0]):
            return base.vector(pt[0], 0, 0)

        if maxc == abs(pt[1]):
            return base.vector(0, pt[1], 0)

        return base.vector(0, 0, pt[2])



from cylinder import *
