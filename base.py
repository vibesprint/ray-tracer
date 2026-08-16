import math


EPSILON = 0.00001

def point(x, y, z):
    return (x, y, z, 1)

def vector(x, y, z):
    return (x, y, z, 0)


def equals(p1, p2):
    if len(p1) != len(p2):
        return False
    for i, j in zip(p1, p2):
        if abs( i-j ) > EPSILON:
            return False
    return True

def add(tup1, tup2):
    result = (None,)
    for i, j in zip(tup1, tup2):
        result = result + (i+j,)

    return result[1:]


def sub(tup1, tup2):
    result = (None,)
    for i, j in zip( tup1, tup2 ):
        result = result + (i-j, )
    return result[1:]

def negate(tup):
    result = (None, )
    for i in tup:
        result = result + (-i,)
    return result[1:]

def scalar_mul(tup, factor):
    result = tuple()
    for i in tup:
        result = result + (i*factor,)
    return result

def scalar_div(tup, factor):
    result = tuple()
    for i in tup:
        result = result + (i/factor,)
    return result


def magnitude(vec):
    sum_of_squares = sum( i*i for i in vec )
    return math.sqrt(sum_of_squares)


def normalize(vec):
    norm = magnitude(vec)
    result = tuple()
    for i in vec:
        result = result + ( i/norm, )

    return result

def dot(a, b):
    return sum( i*j for i,j in zip(a, b))


def cross(vec1, vec2):
    return vector(
            vec1[1] * vec2[2] - vec1[2] * vec2[1],
            vec1[2] * vec2[0] - vec1[0] * vec2[2],
            vec1[0] * vec2[1] - vec1[1] * vec2[0]
            )

