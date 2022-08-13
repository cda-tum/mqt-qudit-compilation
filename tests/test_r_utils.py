from unittest import TestCase


from src.utils.r_utils import *


class Testr_utils(TestCase):

    def test_matmul(self):
        matr1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matr2 = np.array([[2, 2, 2], [2, 2, 2], [2, 2, 2]])

        expected = np.array([[12, 12, 12], [30, 30, 30], [48, 48, 48]])
        result = matmul(matr1, matr2)

        self.assertTrue(np.array_equal(expected, result))


    def test_pi_mod(self):
        res = Pi_mod(3*np.pi/2)
        self.assertEqual(res, -np.pi/2)

        res = Pi_mod(-3*np.pi/2)
        self.assertEqual(res, np.pi/2)

    def test_new_mod(self):
        res = newMod(-5*np.pi/2)
        self.assertEqual(res, -np.pi/2)

        res = newMod(5*np.pi/2)
        self.assertEqual(res, np.pi/2)
