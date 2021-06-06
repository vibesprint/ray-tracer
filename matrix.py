import numpy


def matrix(num_rows, num_cols):
    return numpy.zeros((now_rows, num_cols))

def matrix_from(arr_data):
    return numpy.array(arr_data, dtype=numpy.dtype('float64'))

def equals(mat1, mat2):
    diff = abs(mat1 - mat2)
    epsilon = EPSILON(mat1.shape)
    return (diff <= epsilon).all()

def EPSILON(shape):
    DELTA = 0.00001
    mat = numpy.zeros(shape)
    rows, cols = shape

    for row in range(rows):
        for col in range(cols):
            mat[row, col] = DELTA

    return mat

def unequals(mat1, mat2):
    return ( mat1 != mat2 ).any()

def mul(mat1, mat2):
    return mat1.dot(mat2)

def column_vector(lst):
    return numpy.ndarray((len(lst), 1), buffer=numpy.array(lst), dtype=float)

def identity_matrix(n):
    return numpy.identity(n)

def transpose(mat):
    return mat.T


def determinant(mat):
    if mat.shape == (2, 2):
        return mat[0, 0]*mat[1, 1] - mat[0, 1]*mat[1, 0]
    num_cols = mat.shape[1]

    det = 0
    for i in range(num_cols):
        det += mat[0, i] * cofactor(mat, 0, i)

    return det



def submatrix(mat, row, col):
    nrows, ncols = mat.shape
    submat = []

    for i in range(nrows):
        if i == row:
            continue
        row_data = [None] * (ncols-1)
        row_idx = 0

        for j in range(ncols):
            if j == col:
                continue
            row_data[row_idx] = mat[i, j]
            row_idx += 1

        submat.append(row_data)

    return matrix_from(submat)


def minor(mat, row, col):
    return determinant(
            submatrix(mat, row, col)
            )


def cofactor(mat, row, col):
    mnor = minor(mat, row, col)

    if ((row+col) % 2) == 0:
        return mnor
    return -mnor


def is_invertible(mat):
    return determinant(mat) != 0

def inverse(mat):
    if not is_invertible(mat):
        raise ValueError(f"matrix is not invertible: {mat}")

    inv = numpy.zeros(mat.shape)
    det = determinant(mat)

    rows, cols = inv.shape

    for row in range(rows):
        for col in range(cols):
            inv[col, row] = cofactor(mat, row, col) / det

    return inv
