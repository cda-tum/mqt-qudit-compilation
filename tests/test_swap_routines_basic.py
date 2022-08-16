from unittest import TestCase

from circuit.swap_routines_basic import find_logic_from_phys, graph_rule_update, graph_rule_ongate, \
    gate_chain_condition, route_states2rotate_basic
from src.circuit.swap_routines_ancilla_fixed import *
from src.architecture_graph.level_Graph import level_Graph



class Test(TestCase):
    def setUp(self) -> None:
        test_sample_edges = [(0, 4, {"delta_m": 0, "sensitivity": 1}),
                             (0, 3, {"delta_m": 1, "sensitivity": 3}),
                             (0, 2, {"delta_m": 1, "sensitivity": 3}),
                             (1, 4, {"delta_m": 0, "sensitivity": 1}),
                             (1, 3, {"delta_m": 1, "sensitivity": 3}),
                             (1, 2, {"delta_m": 1, "sensitivity": 3})
                             ]
        test_sample_nodes = [0, 1, 2, 3, 4]
        test_sample_nodes_map = [3, 2, 4, 1, 0]

        self.graph_1 = level_Graph(test_sample_edges, test_sample_nodes, test_sample_nodes_map, [0])
        self.graph_1.phase_storing_setup()

    def test_swap_elements(self):
        example = [0, 1, 2, 3]
        test_swapped = [3, 1, 2, 0]
        swapped_example = swap_elements(example, 0, 3)

        self.assertEqual(swapped_example, test_swapped)

    def test_find_logic_from_phys(self):
        plev_a = 0
        plev_b = 1

        la, lb = find_logic_from_phys(plev_a, plev_b, self.graph_1)
        self.assertEqual(la, 4)
        self.assertEqual(lb, 3)

    def test_graph_rule_update(self):
        gate = R(np.pi, np.pi / 2, 0, 1, 5)
        nodes_data = self.graph_1.nodes(data=True)

        la, lb = find_logic_from_phys(0, 1, self.graph_1)
        self.assertEqual(nodes_data[lb]['phase_storage'], 0.0)

        graph_rule_update(gate, self.graph_1)

        self.assertEqual(nodes_data[lb]['phase_storage'], np.pi)

    def test_graph_rule_ongate(self):
        gate = R(np.pi, np.pi / 2, 0, 1, 5)
        nodes_data = self.graph_1.nodes(data=True)

        graph_rule_update(gate, self.graph_1)

        new_gate = graph_rule_ongate(gate, self.graph_1)

        self.assertEqual(new_gate.phi, 3 / 2 * np.pi)

    def test_gate_chain_condition(self):
        pi_pulses = [R(np.pi, np.pi / 2, 0, 1, 5), R(np.pi, np.pi / 2, 1, 2, 5)]
        gate = R(np.pi / 3, np.pi / 2, 0, 2, 5)

        new_gate = gate_chain_condition(pi_pulses, gate)

        self.assertEqual(new_gate.theta, -np.pi / 3)

    def test_route_states2rotate_basic(self):
        gate = R(np.pi / 3, np.pi / 2, 2, 4, 5)
        cost_of_pi_pulses, pi_pulses_routing, placement = route_states2rotate_basic(gate, self.graph_1)

        self.assertEqual(cost_of_pi_pulses, 0.0004)
        self.assertEqual(len(pi_pulses_routing), 1)
        self.assertEqual(placement.lpmap, [0, 2, 4, 1, 3])
