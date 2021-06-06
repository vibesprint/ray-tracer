import matrix
import utils

def test_4matrix():
    matr = [[1, 2, 3, 4],
              [5.5, 6.5, 7.5, 8.5],
              [9, 10, 11, 12],
              [13.5, 14.5, 15.5, 16.5]]

    matr = matrix.matrix_from(matr)

    assert matr[0, 0] == 1
    assert matr[0, 3] == 4
    assert matr[1, 0] == 5.5
    assert matr[1, 2] == 7.5
    assert matr[2, 2] == 11
    assert matr[3, 0] == 13.5
    assert matr[3,2 ] == 15.5


def test_2matrix():
    matr = [[-3, 5],
            [1, 2]]
    matr = matrix.matrix_from(matr)

    assert matr[0, 0] == -3
    assert matr[0, 1] == 5
    assert matr[1, 0] == 1
    assert matr[1, 1] == 2

def test_3matrix():
    matr = [[-3, 5, 0],
            [1, -2, -7],
            [0, 1, 1]]
    matr = matrix.matrix_from(matr)

    assert matr[0, 0] == -3
    assert matr[1, 1] == -2
    assert matr[2, 2] == 1


def test_equality():
    matr = [[1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]]

    matr1 = matrix.matrix_from(matr)
    matr2 = matrix.matrix_from(matr)

    assert matrix.equals(matr1, matr2)


def test_inequality():
    matr1 = [[1, 2, 3, 4],
             [5, 6, 7, 8],
             [9, 10, 11, 12],
             [13, 14, 15, 16]]

    matr1 = matrix.matrix_from(matr1)

    matr2 = [[2, 3, 4, 5],
             [6, 7, 8, 9],
             [10, 11, 12, 13],
             [14, 15, 16, 17]]

    matr2 = matrix.matrix_from(matr2)

    assert matrix.unequals(matr1, matr2)


def test_multiply():
    matr1 = [[1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 8, 7, 6],
            [5, 4 , 3, 2]]

    matr1 = matrix.matrix_from(matr1)

    matr2 = [
            [-2, 1, 2, 3],
            [3, 2, 1, -1],
            [4, 3, 6, 5],
            [1, 2, 7, 8]
            ]

    matr2 = matrix.matrix_from(matr2)

    exp_result = [[20, 22, 50, 48],
                  [44, 54, 114, 108],
                  [40, 58, 110, 102],
                  [16, 26, 46, 42]]

    exp_result = matrix.matrix_from(exp_result)

    result = matr1.dot(matr2)
    print(result)
    assert matrix.equals( result, exp_result)


def test_multiply_tuple():
    matr = [[1, 2, 3, 4],
            [2, 4, 4, 2],
            [8, 6, 4, 1],
            [0, 0, 0, 1]]

    tup = matrix.column_vector((1, 2, 3, 1))
    matr = matrix.matrix_from(matr)

    exp_result = matrix.column_vector(
            [18, 24, 33, 1]
            )

    result = matrix.mul(matr, tup)
    print(result)

    assert matrix.equals(result, exp_result )


def test_identity():
    matr = matrix.matrix_from(
            [[0, 1, 2, 4],
                [1, 2, 4, 8],
                [2, 4, 8, 16],
                [4, 8, 16, 32]]
            )

    id_mat = matrix.identity_matrix(4)

    assert matrix.equals(
            matrix.mul(matr, id_mat),
            matr)

    col_vect = matrix.column_vector([1, 2, 3, 4])

    assert matrix.equals(
            matrix.mul(id_mat, col_vect),
            col_vect
            )


def test_transpose():
    matr = matrix.matrix_from(
            [[0, 9, 3, 0],
             [9, 8, 0, 8],
             [1, 8, 5, 3],
             [0, 0, 5, 8]]
            )

    transposed = matrix.matrix_from(
            [[0, 9, 1, 0],
             [9, 8, 8, 0],
             [3, 0, 5, 5],
             [0, 8, 3, 8]]
            )

    assert matrix.equals(
            matrix.transpose(matr),
            transposed
            )

def test_tranpose_identity():
    id_mat = matrix.identity_matrix(4)

    assert matrix.equals(
            matrix.transpose(id_mat),
            id_mat
            )


def test_determinant():
    mat = matrix.matrix_from([
        [1, 5],
        [-3, 2]
        ])
    assert matrix.determinant(mat) == 17


def test_submatrix():
    mat = matrix.matrix_from([
        [1, 5, 0],
        [-3, 2, 7],
        [0, 6, -3]
        ])
    submat = matrix.matrix_from([
        [-3, 2],
        [0, 6]
        ])

    assert matrix.equals(
            matrix.submatrix(mat, 0, 2),
            submat
            )

    mat = matrix.matrix_from([
        [-6, 1, 1, 6],
        [-8, 5, 8, 6],
        [-1, 0, 8, 2],
        [-7, 1, -1, 1]
        ])

    submat = matrix.matrix_from([
        [-6, 1, 6],
        [-8, 8, 6],
        [-7, -1, 1]
        ])

    assert matrix.equals(
            matrix.submatrix(mat, 2, 1),
            submat
            )


def test_minor():
    mat = matrix.matrix_from([
        [3, 5, 0],
        [2, -1, -7],
        [6, -1, 5]
        ])

    submat = matrix.submatrix(mat, 1, 0)

    assert matrix.determinant(submat) == 25
    assert matrix.minor(mat, 1, 0) == 25


def test_cofactor():
    mat = matrix.matrix_from([
        [3, 5, 0],
        [2, -1, -7],
        [6, -1, 5]
        ])

    assert matrix.minor(mat, 0, 0) == -12
    assert matrix.cofactor(mat, 0, 0) == -12
    assert matrix.minor(mat, 1, 0) == 25
    assert matrix.cofactor(mat, 1, 0) == -25

def test_determinant_3by3():
    mat = matrix.matrix_from([
        [1, 2, 6],
        [-5, 8, -4],
        [2, 6, 4]
        ])

    assert matrix.cofactor(mat, 0, 0) == 56
    assert matrix.cofactor(mat, 0, 1) == 12
    assert matrix.cofactor(mat, 0, 2) == -46
    assert matrix.determinant(mat) == -196


def test_determinant_4by4():
    mat = matrix.matrix_from([
        [-2, -8, 3, 5],
        [-3, 1, 7, 3],
        [1, 2, -9, 6],
        [-6, 7, 7, -9]
        ])

    assert matrix.cofactor(mat, 0, 0) == 690
    assert matrix.cofactor(mat, 0, 1) == 447
    assert matrix.cofactor(mat, 0, 2) == 210
    assert matrix.cofactor(mat, 0, 3) == 51
    assert matrix.determinant(mat) == -4071


def test_invertibility():
    mat = matrix.matrix_from([
        [6, 4, 4, 4],
        [5, 5, 7, 6],
        [4, -9, 3, -7],
        [9, 1, 7, -6]
        ])

    assert matrix.determinant(mat) == -2120
    assert matrix.is_invertible(mat) == True


    mat = matrix.matrix_from([
        [-4, 2, -2, -3],
        [9, 6, 2, 6],
        [0, -5, 1, -5],
        [0, 0, 0, 0]
        ])

    assert matrix.determinant(mat) == 0
    assert matrix.is_invertible(mat) == False


def test_inverse():
    mat = matrix.matrix_from([
        [-5, 2, 6, -8],
        [1, -5, 1, 8],
        [7, 7, -6, -7],
        [1, -3, 7, 4]
        ])

    inv = matrix.inverse(mat)

    assert matrix.determinant(mat) == 532
    assert matrix.cofactor(mat, 2, 3) == -160
    assert utils.fequals(inv[3, 2], round(-160/532, 5))
    assert matrix.cofactor(mat, 3, 2) == 105
    assert utils.fequals(inv[2, 3], round(105/532, 5))

    exp_inv = matrix.matrix_from([
        [0.21805, 0.45113, 0.24060, -0.04511],
        [-0.80827, -1.45677, -0.44361, 0.52068],
        [-0.07895, -0.22368, -0.05263, 0.19737],
        [-0.52256, -0.81391, -0.30075, 0.30639]
        ])

    assert matrix.equals(inv, exp_inv)


def test_inverse2():
    mat = matrix.matrix_from([
        [8, -5, 9, 2],
        [7, 5, 6, 1],
        [-6, 0, 9, 6],
        [-3, 0, -9, -4]
        ])

    inv = matrix.matrix_from([
[-0.15385 , -0.15385 ,-0.28205 ,-0.53846],
[ -0.07692 ,0.12308 ,0.02564 ,0.03077],
[ 0.35897 ,0.35897 ,0.43590 ,0.92308],
[ -0.69231 ,-0.69231 ,-0.76923 ,-1.92308]
])

    assert matrix.equals(matrix.inverse(mat), inv)


def test_inverse3():
    mat = matrix.matrix_from([
        [9, 3, 0, 9],
        [-5, -2, -6, -3],
        [-4, 9, 6, 4],
        [-7, 6, 6, 2]
        ])

    exp_inv = matrix.matrix_from([
[-0.04074, -0.07778, 0.14444, -0.22222],
[-0.07778, 0.03333, 0.36667, -0.33333],
[-0.02901, -0.14630, -0.10926, 0.12963],
[0.17778, 0.06667, -0.26667, 0.33333]
])

    assert matrix.equals(
            matrix.inverse(mat),
            exp_inv
            )

def test_inverse4():
    mat1 = matrix.matrix_from([
        [3, -9, 7, 3],
        [3, -8, 2, -9],
        [-4, 4, 4, 1],
        [-6, 5, -1, 1]
        ])

    mat2 = matrix.matrix_from([
        [8, 2, 2, 2],
        [3, -1, 7, 0],
        [7, 0, 5, 4],
        [6, -2, 0, 5]
        ])

    mat3 = matrix.mul(mat1, mat2)
    mat1_inv = matrix.inverse(mat2)
    result = matrix.mul(mat3, mat1_inv)

    print(f"Mat3: {mat3}")
    print(f"Result: {result}")

    assert matrix.equals(
            result,
            mat1
            )
