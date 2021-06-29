import ray
import base
import shapes
import color
import light

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
    __slots__ = ["t", "object", "point", "eyev", "normalv", "inside", "over_point"]
    pass

EPSILON = 0.00001
def prepare_computations(i, r):
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

    return comps


def shade_hit(w, comps):
    shadowed = is_shadowed(w, comps.over_point)
    return light.lightning(comps.object.material,
            w.light_source,
            comps.over_point, comps.eyev, comps.normalv,
            shadowed)


def color_at(wrld, r):
    ints = intersect_world(wrld, r)
    hit = ray.hit(ints)
    if hit is None:
        return color.color(0, 0, 0)
    comps = prepare_computations(hit, r)
    return shade_hit(wrld, comps)

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
