from collections import namedtuple

import matrix
import base

import math


class sphere:
    def __init__(self):
        self.transform = matrix.identity_matrix()
        self.origin = base.point(0, 0, 0)

    def set_transform(self, t):
        self.transform = t
