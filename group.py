import shapes
import ray


class group(shapes.Shape):
    def __init__(self):
        shapes.Shape.__init__(self)
        self._shapes = []

    def __len__(self):
        return len(self._shapes)

    def __iter__(self):
        return iter(self._shapes)


    def add_child(self, child):
        self._shapes.append(child)
        child.parent = self


    def local_intersect(self, r):
        ints = []
        for child in self._shapes:
            ints.extend(list(ray.intersect(child, r)))

        return ray.intersections(*ints)


    def local_normal_at(self, pt):
        raise Exception("group local_normal_at function should not be called")
