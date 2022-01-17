from unittest import TestCase

from src.circuit.Rotations import R
from src.architecture_graph.level_Graph import level_Graph
from src.utils.r_utils import *

class Testr_utils(TestCase):


    def test_matmul(self):
        matr1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
        matr2 = np.array([[2,2,2],[2,2,2],[2,2,2]])

        expected = np.array([[12,12,12],[30,30,30],[48,48,48]])
        result = matmul(matr1, matr2)

        self.assertTrue(np.array_equal(expected, result))

    def test_eurlerComplex(self):
        A = 2
        phi = np.pi/2
        num = eurlerComplex(phi, A).round(3)
        self.assertEqual(num, 2*1j )
        phi = np.pi / 4
        num = eurlerComplex(phi, A).round(3)
        exp = (2 * (np.sqrt(2)/2+ (np.sqrt(2)/2*1j))).round(3)
        self.assertEqual(num, exp)

    def test_rotation_cost_calc(self):
        test_sample_edges_1 = [(0, 5, {"delta_m": 1, "sensitivity": 3}),
                               (0, -1, {"delta_m": 0, "sensitivity": 1}),
                               (2, -1, {"delta_m": 0, "sensitivity": 1}),
                               (2, 6, {"delta_m": 0, "sensitivity": 1}),
                               (2, 1, {"delta_m": 0, "sensitivity": 1}),
                               (3, 6, {"delta_m": 0, "sensitivity": 1}),
                               (3, 1, {"delta_m": 0, "sensitivity": 1}),
                               (3, 4, {"delta_m": 0, "sensitivity": 1}),
                               (3, 7, {"delta_m": 1, "sensitivity": 3}),
                               ]
        test_sample_nodes_1 = [-1, 0, 1, 2, 3, 4, 5, 6, 7]

        ## NODES CAN BE INFERRED BY THE EDGES
        graph_1 = level_Graph(test_sample_edges_1, test_sample_nodes_1)
        graph_1.define__states([2, 3], [0], [-1, 1, 4, 5, 6, 7])

        R_sample = R(np.pi/4, 0, 1, 2, 9)

        cost = rotation_cost_calc(R_sample , graph_1)
        self.assertEqual(cost, 0.0015)
