from unittest import TestCase

from src.circuit.Rotations import R
from src.architecture_graph.level_Graph import level_Graph
from src.utils.r_utils import *
from utils.cost_functions import rotation_cost_calc


class Testr_utils(TestCase):

    def test_matmul(self):
        matr1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matr2 = np.array([[2, 2, 2], [2, 2, 2], [2, 2, 2]])

        expected = np.array([[12, 12, 12], [30, 30, 30], [48, 48, 48]])
        result = matmul(matr1, matr2)

        self.assertTrue(np.array_equal(expected, result))



    def test_new_mod(self):
        self.fail()


    class Test(TestCase):
        def test_pi_mod(self):
            self.fail()
