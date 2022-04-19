from unittest import TestCase

from architecture_graph.level_Graph import level_Graph
from circuit.Rotations import R
from utils.cost_functions import rotation_cost_calc


class Test(TestCase):
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

        R_sample = R(np.pi / 4, 0, 1, 2, 9)

        cost = rotation_cost_calc(R_sample, graph_1)
        self.assertEqual(cost, 0.0015)



    def test_theta_cost(self):
        self.fail()



    def test_phi_cost(self):
        self.fail()
