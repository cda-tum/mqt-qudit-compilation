from unittest import TestCase
import numpy as np

from architecture_graph.level_Graph import level_Graph
from circuit.Rotations import R
from utils.cost_functions import rotation_cost_calc, theta_cost, phi_cost, theta_corrector


class Test(TestCase):
    def test_rotation_cost_calc(self):
        test_sample_edges_1 = [(0, 1, {"delta_m": 1, "sensitivity": 1}),
                               (0, 3, {"delta_m": 0, "sensitivity": 1}),
                               (4, 3, {"delta_m": 0, "sensitivity": 1}),
                               (4, 5, {"delta_m": 0, "sensitivity": 1}),
                               (4, 2, {"delta_m": 0, "sensitivity": 1})
                               ]
        test_sample_nodes_1 = [0, 1, 2, 3, 4, 5]
        test_sample_nodes_map = [0, 1, 2, 3, 4, 5]

        ## NODES CAN BE INFERRED BY THE EDGES
        test_graph_1 = level_Graph(test_sample_edges_1, test_sample_nodes_1, test_sample_nodes_map, [1])

        R_1 = R(np.pi/4, 0, 2, 4, 6)
        cost_1 = rotation_cost_calc(R_1, test_graph_1)
        self.assertEqual(cost_1, 4*1.25e-4)

        R_2 = R(np.pi/4, 0, 3, 4, 6)
        cost_2 = rotation_cost_calc(R_2, test_graph_1)
        self.assertEqual(cost_2, 3*1.25e-4)


    def test_theta_cost(self):
        cost = theta_cost(np.pi/8)
        self.assertEqual(cost, 6.25e-05)

        cost = theta_cost(np.pi / 4)
        self.assertEqual(cost, 1.25e-04)

    def test_phi_cost(self):
        cost = phi_cost(np.pi / 8)
        self.assertEqual(cost, 1.25e-05)

        cost = phi_cost(np.pi / 4)
        self.assertEqual(cost, 2.5e-05)

    def test_theta_corrector(self):

        newang = theta_corrector(-5*np.pi)
        self.assertEqual(newang, -1*np.pi)

        newang = theta_corrector(0.1*np.pi)
        self.assertEqual(newang, 4.1*np.pi )
