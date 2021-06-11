import ray

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
