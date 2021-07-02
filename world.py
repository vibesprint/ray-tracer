import ray
import base
import shapes
import color
import light

import utils

class world:
    def __init__(self):
        self.objects = []
        self.light_source = None

    def add_objs(self, *objs):
        self.objects.extend(objs)


def intersect_world(wrld, r):
    ints = []
    for obj in wrld.objects:
        ints.extend(ray.intersect(obj, r))
    return ray.intersections(*ints)


class computation:
    __slots__ = ["t", "object", "point", "eyev", "normalv", "inside", "over_point", "reflectv", "n1", "n2"]
    pass

EPSILON = 0.00001
def prepare_computations(i, r, ints=None):
    if ints is None:
        ints = ray.intersections(i)

    comps = computation()
    comps.t = i.t
    comps.object = i.object
    comps.point = ray.position(r, comps.t)
    comps.eyev = base.negate(r.direction)
    comps.normalv = shapes.normal_at(comps.object, comps.point)
    comps.inside = False
    if base.dot(comps.normalv, comps.eyev) < 0:
        comps.inside = True
        comps.normalv = base.negate(comps.normalv)

    comps.over_point = base.add(comps.point, base.scalar_mul(comps.normalv, EPSILON))
    comps.reflectv = light.reflect(r.direction, comps.normalv)


    calculate_refractive_indices(i, r, ints, comps)

    return comps


def calculate_refractive_indices(hit, r, xs, comps):
    container = []
    for i in xs:
        if i == hit:
            if len(container) == 0:
                comps.n1 = 1.0
            else:
                comps.n1 = container[-1].material.refractive_index

        if i.object in container:
            container.remove(i.object)
        else:
            container.append(i.object)

        if i == hit:
            if len(container) == 0:
                comps.n2 = 1.0
            else:
                comps.n2 = container[-1].material.refractive_index

            break



def shade_hit(w, comps, recur_thresh=4):
    shadowed = is_shadowed(w, comps.over_point)
    surface = light.lightning(comps.object.material,
            comps.object,
            w.light_source,
            comps.over_point, comps.eyev, comps.normalv,
            shadowed)
    reflected = reflected_color(w, comps, recur_thresh-1)
    return base.add(surface, reflected)


def color_at(wrld, r, recur_thresh=4):
    ints = intersect_world(wrld, r)
    hit = ray.hit(ints)
    if hit is None:
        return color.color(0, 0, 0)
    comps = prepare_computations(hit, r)
    return shade_hit(wrld, comps, recur_thresh)

def is_shadowed(wrld, point):
    vec = base.sub(wrld.light_source.position, point)
    distance = base.magnitude(vec)
    direction = base.normalize(vec)

    r = ray.ray(point, direction)
    ints = intersect_world(wrld, r)

    hit = ray.hit(ints)

    if hit is not None and hit.t < distance:
        return True

    return False

def reflected_color(wrld, comps, recur_thresh=4):
    if utils.fequals(comps.object.material.reflective, 0) or recur_thresh < 0:
        return color.color(0, 0, 0)
    reflect_ray = ray.ray(comps.over_point, comps.reflectv)
    col = color_at(wrld, reflect_ray, recur_thresh-1)
    return base.scalar_mul(col, comps.object.material.reflective)
