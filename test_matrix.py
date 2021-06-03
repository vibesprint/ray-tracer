import matrix

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
