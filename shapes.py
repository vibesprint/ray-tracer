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
        self.parent = None

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
    local_point = world_to_object(shape, pt)

    local_normal = shape.local_normal_at(local_point)

    return normal_to_world(shape, local_normal)

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


def world_to_object(shape, point):
    if shape.parent is not None:
        point = world_to_object(shape.parent, point)

    return transform.apply(
            matrix.inverse(shape.transform),
            point
            )



def normal_to_world(shape, normal):
    normal = transform.apply(
            matrix.transpose(matrix.inverse(shape.transform)),
            normal
            )

    normal[3] = 0
    normal = base.normalize(normal)

    if shape.parent is not None:
        return normal_to_world(shape.parent, normal)

    return normal



class triangle(Shape):
    def __init__(self, p1, p2, p3):
        Shape.__init__(self)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.e1 = base.sub(self.p2, self.p1)
        self.e2 = base.sub(self.p3, self.p1)
        self.normal = base.normalize(base.cross(self.e2, self.e1))


    def local_normal_at(self, pt):
        return self.normal

    def local_intersect(self, r):
        dir_cross_e2 = base.cross(r.direction, self.e2)
        det = base.dot(self.e1, dir_cross_e2)

        if utils.fequals(det, 0):
            return ray.intersections()

        f = 1.0 / det
        p1_to_origin = base.sub(r.origin, self.p1)
        u = f * base.dot(p1_to_origin, dir_cross_e2)

        if u < 0 or u > 1:
            return ray.intersections()

        origin_cross_e1 = base.cross(p1_to_origin, self.e1)
        v = f * base.dot(r.direction, origin_cross_e1)

        if v < 0 or (u + v) > 1:
            return ray.intersections()

        t = f * base.dot(self.e2, origin_cross_e1)

        return ray.intersections(
                ray.intersection_with_uv(t, self, u, v)
                )


class smooth_triangle(triangle):

    def __init__(self, p1, p2, p3, n1, n2, n3):
        triangle.__init__(self, p1, p2, p3)
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
