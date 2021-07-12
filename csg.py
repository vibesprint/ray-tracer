import shapes
import group
import ray


class csg:
    def __init__(self, operation, left, right):
        left.parent = self
        right.parent = self
        self.left = left
        self.right = right
        self.operation = operation

    def __contains__(self, obj):
        inl = False
        inr = False

        if type(self.left) is group.group or type(self.left) is csg:
            inl = obj in self.left
        else:
            inl = obj == self.left

        if type(self.right) is group.group or type(self.right) is csg:
            inr = obj in self.right
        else:
            inr = obj == self.right

        return inr or inl

    def in_left(self, obj):
        if type(self.left) is group.group or type(self.left) is csg:
            return obj in self.left

        return obj == self.left


    def local_intersect(self, r):
        leftxs = ray.intersect(self.left, r)
        rightxs = ray.intersect(self.right, r)

        result = ray.intersections(*list(leftxs), *list(rightxs))
        return filter_intersections(self, result)




def intersection_allowed(op, lhit, inl, inr):
    if op == "union":
        return (lhit and (not inr)) or ( not lhit and (not inl))

    elif op == "intersect":
        return (lhit and inr) or (not lhit and inl)

    elif op == "difference":
        return (lhit and not inr) or (not lhit and inl)

    return False


def filter_intersections(c, ints):
    inl = False
    inr = False

    result = []

    for i in ints:
        lhit = c.in_left(i.object)

        if intersection_allowed(c.operation, lhit, inl, inr):
            result.append(i)

        if lhit:
            inl = not inl
        else:
            inr = not inr

    return ray.intersections(*result)
