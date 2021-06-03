import numpy


def matrix(num_rows, num_cols):
    return numpy.zeros((now_rows, num_cols))

def matrix_from(arr_data):
    return numpy.array(arr_data, dtype=numpy.dtype('float64'))

def equals(mat1, mat2):
    return (mat1 == mat2).all()

def unequals(mat1, mat2):
    return ( mat1 != mat2 ).all()
