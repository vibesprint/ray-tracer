import color
import math
import matrix
import transformation as transform
import base
import shapes


class Pattern:
    def __init__(self):
        self.transform = matrix.identity_matrix()

    def pattern_at_shape(self, obj, world_pt):
        object_point = shapes.world_to_object(obj, world_pt)

        pattern_point = transform.apply(matrix.inverse(self.transform), object_point)
        return self.pattern_at(pattern_point)


class stripe_pattern(Pattern):
    def __init__(self, col1, col2):
        Pattern.__init__(self)
        self.a = col1
        self.b = col2

    def pattern_at(self, pt):
        if math.floor(pt[0]) % 2 == 0:
            return self.a
        return self.b

    stripe_at = pattern_at


class gradient_pattern(Pattern):
    def __init__(self, col1, col2):
        Pattern.__init__(self)
        self.a = col1
        self.b = col2

    def pattern_at(self, local_pt):
        dist = base.sub(self.b, self.a)
        frac = local_pt[0] - math.floor(local_pt[0])

        return base.add(
                self.a,
                base.scalar_mul(dist, frac)
                )


class ring_pattern(Pattern):
    def __init__(self, col1, col2):
        Pattern.__init__(self)
        self.a = col1
        self.b = col2

    def pattern_at(self, local_pt):
        if math.floor(math.sqrt(local_pt[0]**2 + local_pt[2]**2)) % 2 == 0:
            return self.a
        return self.b


class checkers_pattern(Pattern):
    def __init__(self, col1, col2):
        Pattern.__init__(self)
        self.a = col1
        self.b = col2

    def pattern_at(self, pt):
        if (math.floor(pt[0]) + math.floor(pt[1]) + math.floor(pt[2])) % 2 == 0:
            return self.a
        return self.b
