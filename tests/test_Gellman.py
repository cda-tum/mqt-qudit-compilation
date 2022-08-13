from unittest import TestCase
from src.circuit.Gellman import *


class TestGellMann(TestCase):

    def test_m(self):
        dimension = 4
        Ga = GellMann(0, 1, 'a', dimension).matrix

        Gs = GellMann(0, 1, 's', dimension).matrix
        test_Ga = np.array([[0. + 0.j, 0. - 1.j, 0. + 0.j, 0. + 0.j],
                            [0. + 1.j, 0. + 0.j, 0. + 0.j, 0. + 0.j],
                            [0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j],
                            [0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j]])

        test_Gs = np.array([[0. + 0.j, 1. + 0.j, 0. + 0.j, 0. + 0.j],
                            [1. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j],
                            [0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j],
                            [0. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j]])

        self.assertTrue(np.allclose(Ga, test_Ga))
        self.assertTrue(np.allclose(Gs, test_Gs))

        dimension = 3
        Ga = GellMann(0, 1, 'a', dimension).matrix

        Gs = GellMann(0, 1, 's', dimension).matrix
        test_Ga = np.array([[0. + 0.j, 0. - 1.j, 0. + 0.j],
                            [0. + 1.j, 0. + 0.j, 0. + 0.j],
                            [0. + 0.j, 0. + 0.j, 0. + 0.j]])

        test_Gs = np.array([[0. + 0.j, 1. + 0.j, 0. + 0.j],
                            [1. + 0.j, 0. + 0.j, 0. + 0.j],
                            [0. + 0.j, 0. + 0.j, 0. + 0.j]])

        self.assertTrue(np.allclose(Ga, test_Ga))
        self.assertTrue(np.allclose(Gs, test_Gs))

        dimension = 3
        Ga = GellMann(0, 2, 'a', dimension).matrix

        Gs = GellMann(0, 2, 's', dimension).matrix
        test_Ga = np.array([[0. + 0.j, 0. + 0.j, 0. - 1.j],
                            [0. + 0.j, 0. + 0.j, 0. + 0.j],
                            [0. + 1.j, 0. + 0.j, 0. + 0.j]])

        test_Gs = np.array([[0. + 0.j, 0. + 0.j, 1. + 0.j],
                            [0. + 0.j, 0. + 0.j, 0. + 0.j],
                            [1. + 0.j, 0. + 0.j, 0. + 0.j]])

        self.assertTrue(np.allclose(Ga, test_Ga))
        self.assertTrue(np.allclose(Gs, test_Gs))
