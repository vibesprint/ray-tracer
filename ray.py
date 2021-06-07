from collections import namedtuple

import base

ray = namedtuple("ray", "origin direction")


def position(r, t):
    return base.add(
            r.origin,
            base.scalar_mul(r.direction, t)
            )
