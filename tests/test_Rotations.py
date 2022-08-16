from unittest import TestCase

import numpy as np
from src.circuit.Rotations import R, Rz, Custom_Unitary


class Testcustom_Unitary(TestCase):

    def test_cost(self):
        dimension = 4
        example = np.identity(dimension, dtype='complex')
        matrix_obj = Custom_Unitary(example, dimension)

        self.assertTrue(np.equal(matrix_obj.matrix, example).all())

        self.assertTrue(np.isclose(matrix_obj.cost, np.NAN, equal_nan=True))


class TestR(TestCase):
    def test_dag(self):
        self.R1 = R(np.pi / 3, np.pi / 7, 1, 2, 3)
        R1_test = [[1. + 0.j, 0. + 0.j, 0. + 0.j],
                   [0. + 0.j, 0.86602 + 0.j, -0.21694 - 0.45048j],
                   [0. + 0.j, 0.21694 - 0.45048j, 0.86602 + 0.j]]

        self.assertTrue(np.allclose(self.R1.matrix, R1_test))

        R1_test_dag = [[1. + 0.j, 0. + 0.j, 0. + 0.j],
                       [0. + 0.j, 0.86602 + 0.j, 0.21694 + 0.45048j],
                       [0. + 0.j, -0.21694 + 0.45048j, 0.86602 + 0.j]]

        self.assertTrue(np.allclose(self.R1.dag, R1_test_dag))

        self.R1 = R(np.pi / 3, np.pi / 7, 0, 2, 4)
        R1_test = [[0.8660254 + 0.j, 0. + 0.j, -0.21694187 - 0.45048443j, 0. + 0.j],
                   [0. + 0.j, 1. + 0.j, 0. + 0.j, 0. + 0.j],
                   [0.21694187 - 0.45048443j, 0. + 0.j, 0.8660254 + 0.j, 0. + 0.j],
                   [0. + 0.j, 0. + 0.j, 0. + 0.j, 1. + 0.j]]

        self.assertTrue(np.allclose(self.R1.matrix, R1_test))

        R1_test_dag = [[0.8660254 + 0.j, 0. + 0.j, 0.21694187 + 0.45048443j, 0. + 0.j],
                       [0. + 0.j, 1. + 0.j, 0. + 0.j, 0. + 0.j],
                       [-0.21694187 + 0.45048443j, 0. + 0.j, 0.8660254 + 0.j, 0. + 0.j],
                       [0. + 0.j, 0. + 0.j, 0. + 0.j, 1. + 0.j]]

        self.assertTrue(np.allclose(self.R1.dag, R1_test_dag))

    def test_regulate_theta(self):
        self.R1 = R(0.01 * np.pi, np.pi / 7, 0, 2, 3)
        self.assertAlmostEqual(round(self.R1.theta, 4), 12.5978)

    def test_levels_setter(self):
        self.R1 = R(0.01 * np.pi, np.pi / 7, 2, 0, 3)
        self.assertEqual(self.R1.lev_a, 0)
        self.assertEqual(self.R1.lev_b, 2)
        self.assertEqual(self.R1.original_lev_a, 2)
        self.assertEqual(self.R1.original_lev_b, 0)

    def test_cost(self):
        self.R1 = R(0.01 * np.pi, np.pi / 7, 2, 0, 3)
        self.assertEqual(round(self.R1.cost, 4), 0.00160)


class TestRz(TestCase):
    def test_dag(self):
        self.RZ1 = Rz(np.pi / 3, 1, 3)
        RZ1_test = [[1. + 0.j, 0. + 0.j, 0. + 0.j],
                    [0. + 0.j, 0.5 - 0.8660254j, 0. + 0.j],
                    [0. + 0.j, 0. + 0.j, 1. + 0.j]]

        self.assertTrue(np.allclose(self.RZ1.matrix, RZ1_test))

        RZ1_test_dag = [[1. + 0.j, 0. + 0.j, 0. + 0.j],
                        [0. + 0.j, 0.5 + 0.8660254j, 0. + 0.j],
                        [0. + 0.j, 0. + 0.j, 1. + 0.j]]

        self.assertTrue(np.allclose(self.RZ1.dag, RZ1_test_dag))

        self.RZ1 = Rz(np.pi / 3, 1, 4)
        RZ1_test = [[1. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j],
                    [0. + 0.j, 0.5 - 0.8660254j, 0. + 0.j, 0. + 0.j],
                    [0. + 0.j, 0. + 0.j, 1. + 0.j, 0. + 0.j],
                    [0. + 0.j, 0. + 0.j, 0. + 0.j, 1. + 0.j]]

        self.assertTrue(np.allclose(self.RZ1.matrix, RZ1_test))

        RZ1_test_dag = [[1. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j],
                        [0. + 0.j, 0.5 + 0.8660254j, 0. + 0.j, 0. + 0.j],
                        [0. + 0.j, 0. + 0.j, 1. + 0.j, 0. + 0.j],
                        [0. + 0.j, 0. + 0.j, 0. + 0.j, 1. + 0.j]]

        self.assertTrue(np.allclose(self.RZ1.dag, RZ1_test_dag))

    def test_regulate_theta(self):
        self.RZ1 = Rz(0.01 * np.pi, 1, 4)
        self.assertAlmostEqual(round(self.RZ1.theta, 4), 12.5978)

    def test_levels_setter(self):
        self.RZ1 = Rz(0.01 * np.pi, -1, 4)
        self.assertEqual(self.RZ1.lev, 3)

    def test_cost(self):
        self.RZ1 = Rz(0.01 * np.pi, 1, 4)
        self.assertEqual(round(self.RZ1.cost, 4), 0.0004)



