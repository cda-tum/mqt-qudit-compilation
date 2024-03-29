from unittest import TestCase

from src.evaluation.Pauli import H
from src.architecture_graph.level_Graph import level_Graph
from src.decomposition.tree_struct import *
import numpy as np


class TestNode(TestCase):
    def setUp(self) -> None:
        test_sample_edges = [(0, 5, {"delta_m": 0, "sensitivity": 1}),
                             (0, 4, {"delta_m": 0, "sensitivity": 1}),
                             (0, 3, {"delta_m": 1, "sensitivity": 3}),
                             (0, 2, {"delta_m": 1, "sensitivity": 3}),
                             (1, 5, {"delta_m": 0, "sensitivity": 1}),
                             (1, 4, {"delta_m": 0, "sensitivity": 1}),
                             (1, 3, {"delta_m": 1, "sensitivity": 3}),
                             (1, 2, {"delta_m": 1, "sensitivity": 3})
                             ]
        test_sample_nodes = [0, 1, 2, 3, 4, 5]
        test_sample_nodes_map = [0, 2, 5, 4, 1, 3]

        self.graph_1 = level_Graph(test_sample_edges, test_sample_nodes, test_sample_nodes_map, [0])

        self.U = H(6).matrix

        self.root = Node(0, None, self.U, self.graph_1, 0, 10e-4, 1, [], -1, None)

    def test_add(self):
        self.root.add(1, None, self.U, self.graph_1, 0, 10e-4, 1, [])
        self.assertEqual(self.root.size, 1)
        self.assertEqual(self.root.children[0].key, 1)
        self.assertEqual(self.root.children[0].current_cost, 0)

    def test_print(self):
        self.root.add(1, None, self.U, self.graph_1, 0, 10e-4, 1, [])
        print(self.root.children[0])


class TestN_ary_Tree(TestCase):
    def setUp(self) -> None:
        test_sample_edges = [(0, 5, {"delta_m": 0, "sensitivity": 1}),
                             (0, 4, {"delta_m": 0, "sensitivity": 1}),
                             (0, 3, {"delta_m": 1, "sensitivity": 3}),
                             (0, 2, {"delta_m": 1, "sensitivity": 3}),
                             (1, 5, {"delta_m": 0, "sensitivity": 1}),
                             (1, 4, {"delta_m": 0, "sensitivity": 1}),
                             (1, 3, {"delta_m": 1, "sensitivity": 3}),
                             (1, 2, {"delta_m": 1, "sensitivity": 3})
                             ]
        test_sample_nodes = [0, 1, 2, 3, 4, 5]
        test_sample_nodes_map = [0, 2, 5, 4, 1, 3]

        self.graph_1 = level_Graph(test_sample_edges, test_sample_nodes, test_sample_nodes_map, [0])

        self.U = H(6).matrix

        self.T = N_ary_Tree()
        self.T.add(0, None, None, None, 0, 0, 0, [])

    def test_add(self):
        # new_key, rotation, U_of_level, graph_current, current_cost, current_decomp_cost, max_cost, pi_pulses, parent_key
        self.T.add(2, None, None, None, 0, 0, 0, [], 0)
        self.T.add(3, None, None, None, 0, 0, 0, [], 0)

        self.assertEqual(self.T.root.children[0].key, 2)
        self.assertEqual(self.T.root.children[1].key, 3)

    def test_find_node(self):
        self.T.add(2, None, None, None, 0, 0, 0, [], 0)

        node = self.T.find_node(self.T.root, 2)
        self.assertEqual(node.parent_key, 0)
        self.assertEqual(node.key, 2)

    def test_depth(self):
        self.T.add(2, None, None, None, 0, 0, 0, [], 0)
        self.T.add(3, None, None, None, 0, 0, 0, [], 2)

        d0 = self.T.depth(0)
        d2 = self.T.depth(2)
        self.assertEqual(d0, 2)
        self.assertEqual(d2, 1)

    def test_max_depth(self):
        self.T.add(2, None, None, None, 0, 0, 0, [], 0)
        self.T.add(3, None, None, None, 0, 0, 0, [], 2)
        self.T.add(4, None, None, None, 0, 0, 0, [], 3)

        node = self.T.find_node(self.T.root, 2)

        d2 = self.T.max_depth(node)
        self.assertEqual(d2, 2)

    def test_size_refresh(self):
        size = self.T.size_refresh(self.T.root)

        self.assertEqual(size, 0)

        self.T.add(2, None, None, None, 0, 0, 0, [], 0)
        self.T.add(3, None, None, None, 0, 0, 0, [], 2)
        self.T.add(4, None, None, None, 0, 0, 0, [], 2)
        self.T.add(5, None, None, None, 0, 0, 0, [], 3)

        size = self.T.size_refresh(self.T.root)

        self.assertEqual( size, 4 )



    def test_found_checker(self):
        self.T.add(2, None, None, None, 0.1, 0.1, 10, [], 0)
        self.T.add(3, None, None, None, 0.11, 0.1, 10, [], 2)
        self.T.add(4, None, None, None, 0.01, 0.01, 10, [], 2)

        self.T.root.finished = False
        self.T.root.children[0].finished = False
        self.T.root.children[0].children[0].finished = False
        self.T.root.children[0].children[1].finished = True

        self.assertTrue(self.T.found_checker(self.T.root))
        self.T.root.finished = False
        self.T.root.children[0].finished = False
        self.T.root.children[0].children[0].finished = False
        self.T.root.children[0].children[1].finished = False

        self.assertFalse(self.T.found_checker(self.T.root))


    def test_min_cost_decomp(self):
        self.T.add(2, None, None, None, 0.1, 0.1, 10, [], 0)
        self.T.add(3, None, None, None, 0.11, 0.1, 10, [], 2)
        self.T.add(4, None, None, None, 0.01, 0.01, 10, [], 2)

        self.T.root.finished = True
        self.T.root.children[0].finished = True
        self.T.root.children[0].children[0].finished = True
        self.T.root.children[0].children[1].finished = True

        node_seq, best_cost, final_graph = self.T.min_cost_decomp(self.T.root)
        self.assertEqual(best_cost[0], 0.01)
        self.assertEqual(best_cost[1], 0.01)
        self.assertEqual(final_graph, None)
        self.assertEqual(node_seq[0].key, 0)
        self.assertEqual(node_seq[1].key, 2)
        self.assertEqual(node_seq[2].key, 4)

    def test_retrieve_decomposition(self):

        self.T.add(2, None, None, self.graph_1, 0.1, 0.1, 10, [], 0)
        self.T.add(3, None, None, self.graph_1, 0.11, 0.1, 10, [], 2)
        self.T.add(4, None, None, self.graph_1, 0.01, 0.01, 10, [], 2)

        self.T.root.finished = False
        self.T.root.children[0].finished = False
        self.T.root.children[0].children[0].finished = False
        self.T.root.children[0].children[1].finished = True

        decomp_nodes, best_cost, graph = self.T.retrieve_decomposition(self.T.root)


        self.assertEqual(best_cost[0], 0.01)
        self.assertEqual(best_cost[1], 0.01)
        self.assertEqual(graph, self.graph_1)
        self.assertEqual(decomp_nodes[0].key, 0)
        self.assertEqual(decomp_nodes[1].key, 2)
        self.assertEqual(decomp_nodes[2].key, 4)

    def test_is_empty(self):
        self.T = N_ary_Tree()
        self.assertTrue(self.T.is_empty())

        self.T.add(0, None, None, self.graph_1, 0.0, 0.0, 10, [])
        self.assertFalse(self.T.is_empty())

        self.T.add(2, None, None, self.graph_1, 0.1, 0.1, 10, [], 0)
        self.assertFalse(self.T.is_empty())

    def test_total_size(self):
        size = self.T.total_size

        self.assertEqual(size, 1)

        self.T.add(2, None, None, None, 0, 0, 0, [], 0)
        self.T.add(3, None, None, None, 0, 0, 0, [], 2)
        self.T.add(4, None, None, None, 0, 0, 0, [], 2)
        self.T.add(5, None, None, None, 0, 0, 0, [], 3)

        size = self.T.total_size

        self.assertEqual(size, 5)

    def test_print_tree(self):

        self.T.add(2, None, None, self.graph_1, 0.1, 0.1, 10, [], 0)
        self.T.add(3, None, None, self.graph_1, 0.11, 0.1, 10, [], 2)
        self.T.add(4, None, None, self.graph_1, 0.01, 0.01, 10, [], 2)

        tree_string = self.T.print_tree(self.T.root, "")

        self.assertEqual(tree_string, "N0(\n\tN2(\n\tN3(),N4()))")
