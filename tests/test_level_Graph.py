from unittest import TestCase
from src.architecture_graph.level_Graph import *


class Testlevel_Graph(TestCase):

    def setUp(self) -> None:
        test_sample_edges_1 = [(0, 5, {"delta_m": 0, "sensitivity": 1}),
                               (0, 4, {"delta_m": 0, "sensitivity": 1}),
                               (0, 3, {"delta_m": 1, "sensitivity": 3}),
                               (0, 2, {"delta_m": 1, "sensitivity": 3}),
                               (1, 5, {"delta_m": 0, "sensitivity": 1}),
                               (1, 4, {"delta_m": 0, "sensitivity": 1}),
                               (1, 3, {"delta_m": 1, "sensitivity": 3}),
                               (1, 2, {"delta_m": 1, "sensitivity": 3})
                               ]

        test_sample_nodes_1 = [0, 1, 2, 3, 4, 5]
        test_sample_nmap_1 = [0, 1, 2, 3, 4, 5]

        self.graph_1 = level_Graph(test_sample_edges_1, test_sample_nodes_1, test_sample_nmap_1, [1])

    def test_phase_storing_setup(self):
        self.graph_1.phase_storing_setup()
        self.assertEqual(self.graph_1.nodes[0]['phase_storage'], 0.0)

    def test_distance_nodes(self):
        self.assertEqual(self.graph_1.distance_nodes(2, 3), 2)

    def test_distance_nodes_pi_pulses_fixed_ancilla(self):
        self.assertEqual(self.graph_1.distance_nodes_pi_pulses_fixed_ancilla(0, 1), 1)

    def test_define__states(self):
        self.assertEqual(self.graph_1._1stInode, 1)

    def test_update_list(self):
        graph_1_list = [(0, 5), (0, 4), (0, 3), (0, 2), (1, 5), (1, 4), (1, 3), (1, 2)]
        self.assertNotEqual(self.graph_1.update_list(graph_1_list, 0, 5),
                            [(6, 0), (5, 4), (5, 3), (5, 2), (1, 0), (1, 4), (1, 3), (1, 2)])
        self.assertEqual(self.graph_1.update_list(graph_1_list, 0, 5),
                         [(5, 0), (5, 4), (5, 3), (5, 2), (1, 0), (1, 4), (1, 3), (1, 2)])

    def test_swap_nodes(self):
        list_1 = [(5, 0), (5, 4), (5, 3), (5, 2), (1, 0), (1, 4), (1, 3), (1, 2)]
        list_2 = [(0, 5), (0, 4), (0, 3), (0, 2), (1, 5), (1, 4), (1, 3), (1, 2)]

        #self.graph_1.define__states([1], [0], [2, 3, 4, 5])
        nodes = list(self.graph_1.nodes)
        edges = list(self.graph_1.edges)

        temp1 = self.graph_1.swap_nodes(0, 5)
        temp2 = self.graph_1.swap_nodes(0, 1)

        self.assertEqual(list(temp1.nodes), nodes)
        self.assertEqual(list(temp2.nodes), nodes)

        edge1 = temp1.edges
        edge2 = temp2.edges
        bool1 = True
        bool2 = True

        for tup in list_1:
            tempbool = False
            for e in edge1:
                if (tup[0] in e and tup[1] in e):
                    tempbool = True

            bool1 = bool1 and tempbool

        self.assertTrue(bool1)

        for tup in list_2:
            tempbool = False
            for e in edge2:
                if (tup[0] in e and tup[1] in e):
                    tempbool = True
            bool2 = bool2 and tempbool

        self.assertTrue(bool2)

    def test_get_node_sensitivity_cost(self):
        sensitivity = self.graph_1.get_node_sensitivity_cost(0)
        self.assertEqual(sensitivity, 8)

    def test_get_edge_sensitivity(self):
        sensitivity = self.graph_1.get_edge_sensitivity(1, 2)
        self.assertEqual(sensitivity, 3)




    def test_logic_physical_map(self):
        self.fail()

    def test_deep_copy_func(self):
        self.fail()

    def test_index(self):
        self.fail()

    def test_swap_node_attributes(self):
        self.fail()

    def test_swap_node_attr_simple(self):
        self.fail()

    def test_get_rz_gates(self):
        self.fail()


    def test__1st_rnode(self):
        self.fail()

    def test__1st_inode(self):
        self.fail()

    def test_is_inode(self):
        self.fail()

    def test_lpmap(self):
        self.fail()
