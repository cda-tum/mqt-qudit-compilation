from unittest import TestCase
import numpy as np

from src.architecture_graph.level_Graph import level_Graph
from src.circuit.Rotations import R
from src.utils.costs_utils import *


class Testcost_utils(TestCase):

    def test_cost_calculator(self):

        test_sample_edges_1 = [(0, 1, {"delta_m": 1, "sensitivity": 1}),
                               (0, 3, {"delta_m": 0, "sensitivity": 1}),
                               (4, 3, {"delta_m": 0, "sensitivity": 1}),
                               (4, 5, {"delta_m": 0, "sensitivity": 1}),
                               (4, 2, {"delta_m": 0, "sensitivity": 1})
                               ]
        test_sample_nodes_1 = [0, 1, 2, 3, 4, 5]
        test_sample_nodes_map = [0, 1, 2, 3, 4, 5]
        non_zeros = 2

        ## NODES CAN BE INFERRED BY THE EDGES
        test_graph_1 = level_Graph(test_sample_edges_1, test_sample_nodes_1, test_sample_nodes_map, [1])

        R_1 = R(np.pi / 4, 0, 1, 4, 6)

        total_costing, pi_pulses_routing, new_placement, cost_of_pi_pulses, gate_cost = cost_calculator( R_1, test_graph_1, non_zeros)

        self.assertEqual(total_costing, 0.00425)
        self.assertEqual(len(pi_pulses_routing), 2)

        self.assertEqual(cost_of_pi_pulses, 2e-3)
        self.assertEqual(gate_cost, 1.25e-4)


