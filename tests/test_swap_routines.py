from unittest import TestCase

from src.circuit.swap_routines_ancilla_fixed import *
from src.architecture_graph.level_Graph import level_Graph
import networkx as nx


class Test(TestCase):
    def setUp(self) -> None:
        test_sample_edges_1 = [#(0, 5, {"delta_m": 1, "sensitivity": 3}),
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
        self.graph_1 = level_Graph(test_sample_edges_1, test_sample_nodes_1)
        self.graph_1.define__states([2, 3], [0], [-1, 1, 4, 5, 6, 7])

    def test_find_next_available(self):
        list_to_swap = [5, 0, -1, 2, 6, 3, 4]
        next_i = find_next_available(3, list_to_swap)
        self.assertTrue(next_i, 1)

        list_to_swap = [5, 0, -1, -2, 6, 3, 4]
        next_i = find_next_available(4, list_to_swap)
        self.assertTrue(next_i, 1)

    def test_pi_swap_routine(self):
        list_to_swap = [5, 0, -1, 2, 6, 3, 4]  # coming from graph 1
        next_i = 1
        i = 2
        # swapping 6 wih 0
        cost, pi_swapping_list, new_graph = pi_swap_routine(list_to_swap, i, next_i, self.graph_1,
                                                            len(list(self.graph_1.nodes)))

    def test_route_states2rotate(self):
        gate = R(np.pi, 0, 0, 6, 9)
        cost_of_pi_pulses, pi_pulses_routing, placement = route_states2rotate(gate, self.graph_1)

    def test_rotate_over_ancilla(self):
        self.fail()
