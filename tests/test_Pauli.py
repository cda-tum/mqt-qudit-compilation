from unittest import TestCase
import numpy as np

from src.evaluation.Pauli import H, Z, X, S

class Test_Pauli(TestCase):

    def test_H(self):
        dimension = 3
        H_test = H(dimension).matrix.round(5)
        compare = np.array([
                [ 0.57735027+0.j,   0.57735027+0.j,  0.57735027+0.j  ],
                [ 0.57735027+0.j,  -0.28867513+0.5j, -0.28867513-0.5j],
                [ 0.57735027+0.j,  -0.28867513-0.5j, -0.28867513+0.5j]
                ])
        compare = compare.round(5)
        self.assertTrue(np.array_equal(H_test, compare))

        dimension = 4
        H_test = H(dimension).matrix.round(5)
        compare = np.array([[ 0.5+0.j  , 0.5+0.j ,  0.5+0.j,   0.5+0.j ],
                            [ 0.5+0.j  , 0. +0.5j,-0.5+0.j , -0. -0.5j],
                            [ 0.5+0.j  ,-0.5+0.j ,  0.5+0.j,  -0.5+0.j ],
                            [ 0.5+0.j  ,-0. -0.5j, -0.5+0.j,   0. +0.5j]])
        compare = compare.round(5)
        self.assertTrue(np.array_equal(H_test, compare))

    def test_Z(self):
        dimension = 3
        Z_test = Z(dimension).matrix.round(5)
        compare = np.array([[ 1. +0.j,       0. +0.j,       0. +0.j     ],
                            [ 0. +0.j,      -0.5+0.86603j,  0. +0.j     ],
                            [ 0. +0.j,       0. +0.j,      -0.5-0.86603j]])
        compare = compare.round(5)
        self.assertTrue(np.array_equal(Z_test, compare))

        dimension = 4
        Z_test = Z(dimension).matrix.round(5)
        compare = np.array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
                            [ 0.+0.j,  0.+1.j,  0.+0.j,  0.+0.j],
                            [ 0.+0.j,  0.+0.j, -1.+0.j,  0.+0.j],
                            [ 0.+0.j,  0.+0.j,  0.+0.j, -0.-1.j]
                            ])
        compare = compare.round(5)
        self.assertTrue(np.array_equal(Z_test, compare))


    def test_X(self):
        dimension = 3
        X_test = X(dimension).matrix.round(5)
        compare = np.array([[0.+0.j, 0.+0.j, 1.+0.j],
                            [1.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 1.+0.j, 0.+0.j]])
        compare = compare.round(5)
        self.assertTrue(np.array_equal(X_test, compare))

        dimension = 4
        X_test = X(dimension).matrix.round(5)
        compare = np.array([[0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
                            [1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
                            [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j]
                            ])
        compare = compare.round(5)
        self.assertTrue(np.array_equal(X_test, compare))


    def test_S(self):
        dimension = 3
        S_test = S(dimension).matrix.round(5)
        compare = np.array([[ 1. +0.j,       0. +0.j,       0. +0.j     ],
                            [ 0. +0.j,      -0.5+0.86603j,  0. +0.j     ],
                            [ 0. +0.j,       0. +0.j,      1. +0.j     ]])
        compare = compare.round(5)
        self.assertTrue(np.array_equal(S_test, compare))

        dimension = 4
        S_test = S(dimension).matrix.round(5)
        compare = np.array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
                            [ 0.+0.j,  0.+1.j,  0.+0.j,  0.+0.j],
                            [ 0.+0.j,  0.+0.j, -0.-1.j,  0.+0.j],
                            [ 0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j]])
        compare = compare.round(5)
        self.assertTrue(np.array_equal(S_test, compare))
