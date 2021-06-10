
EPSILON = 1e-5

def color(red, green, blue):
    return red, green, blue

def red(col):
    return col[0]

def green(col):
    return col[1]

def blue(col):
    return col[2]


def add(col1, col2):
    return tuple(i+j for i,j in zip(col1, col2))


def sub(col1, col2):
    return tuple(i-j for i,j in zip(col1, col2))

def scalar_mul(col, scalar):
    return tuple(i*scalar for i in col)

def hadamard_mul(col1, col2):
    return tuple(i*j for i, j in zip(col1, col2))

def equals(col1, col2):
    for i, j in zip(col1, col2):
        if abs(i - j) > EPSILON:
            return False

    return True
