from unittest import TestCase
from binq.src.architecture_graph.level_Graph import level_Graph
from binq.src.decomposition.tree_struct import *
import numpy as np


class TestNode(TestCase):
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

        ## NODES CAN BE INFERRED BY THE EDGES
        self.graph_1 = level_Graph(test_sample_edges_1, test_sample_nodes_1)
        self.graph_1.define__states([1], [0], [2, 3, 4, 5])

        self.U = np.array([[0.57735 + 0.00000j, 0.57735 + 0.00000j, 0.57735 + 0.00000j],
                      [0.57735 + 0.00000j, -0.28868 + 0.50000j, -0.28868 - 0.50000j],
                      [0.57735 + 0.00000j, -0.28868 - 0.50000j, -0.28868 + 0.50000j]], dtype='complex')
        self.root = Node(0, None, self.U, self.graph_1, 0, 10e-4, [], -1)

    def test_add(self):
        self.root.add(1, None, self.U, self.graph_1, 0, 10e-4, [])
        self.assertEqual(self.root.size, 1)

    def test_print(self):
        print(self.root)




class TestN_ary_Tree(TestCase):
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

        ## NODES CAN BE INFERRED BY THE EDGES
        self.graph_1 = level_Graph(test_sample_edges_1, test_sample_nodes_1)
        self.graph_1.define__states([1], [0], [2, 3, 4, 5])

        self.U = np.array([[0.57735 + 0.00000j, 0.57735 + 0.00000j, 0.57735 + 0.00000j],
                           [0.57735 + 0.00000j, -0.28868 + 0.50000j, -0.28868 - 0.50000j],
                           [0.57735 + 0.00000j, -0.28868 - 0.50000j, -0.28868 + 0.50000j]], dtype='complex')
        self.T = N_ary_Tree()
        self.T.add(0, None, None, None, 0, 10, [])


    def test_find_node(self):
        self.T.root.add(2, None, None, None, 0, 0, [])

        node = self.T.find_node(self.T.root, 2)
        self.assertEqual(node.key, 2)

    def test_depth(self):
        self.T.root.add(2, None, None, None, 0, 0, [])

        d = self.T.depth(0)
        self.assertEqual(d,1)


    def test_add(self):
        self.T.root.add(2, None, None, None, 0, 0, [])
        self.T.add(3, None, None, None, 0, 0, [], 2)
        node = self.T.find_node(self.T.root, 3)
        self.assertEqual(node.key, 3)


    def test_min_cost_decomp(self):

        self.T.add(2, None, None, self.graph_1, 0.1, 10, [], 0)
        self.T.add(3, None, None, self.graph_1, 0.1, 10, [], 2)
        self.T.add(4, None, None, self.graph_1, 0.01, 10, [], 2)

        self.T.root.finished = True
        self.T.root.children[0].finished = True
        self.T.root.children[0].children[0].finished=True
        self.T.root.children[0].children[1].finished = True

        node_seq, best_cost, final_graph = self.T.min_cost_decomp(self.T.root)
        self.assertEqual(best_cost, 0.01)
        self.assertEqual(final_graph, self.graph_1)
        self.assertEqual(node_seq[0].key, 0)
        self.assertEqual(node_seq[1].key, 2)
        self.assertEqual(node_seq[2].key, 4)


    def test_found_checker(self):
        self.T.add(2, None, None, self.graph_1, 0.1, 10, [], 0)
        self.T.add(3, None, None, self.graph_1, 0.1, 10, [], 2)
        self.T.add(4, None, None, self.graph_1, 0.01, 10, [], 2)

        self.T.root.finished = False
        self.T.root.children[0].finished = False
        self.T.root.children[0].children[0].finished = False
        self.T.root.children[0].children[1].finished = True

        self.assertTrue( self.T.found_checker(self.T.root) )

    def test_retrieve_decomposition(self):
        self.T.add(2, None, None, self.graph_1, 0.1, 10, [], 0)
        self.T.add(3, None, None, self.graph_1, 0.1, 10, [], 2)
        self.T.add(4, None, None, self.graph_1, 0.01, 10, [], 2)

        self.T.root.finished = False
        self.T.root.children[0].finished = False
        self.T.root.children[0].children[0].finished = False
        self.T.root.children[0].children[1].finished = True

        decomp_nodes, bcost, graph = self.T.retrieve_decomposition(self.T.root)

        self.assertEqual(bcost, 0.01)
        self.assertEqual(graph, self.graph_1)
        self.assertEqual(decomp_nodes[0].key, 0)
        self.assertEqual(decomp_nodes[1].key, 2)
        self.assertEqual(decomp_nodes[2].key, 4)

    def test_is_empty(self):
        self.T = N_ary_Tree()
        self.assertTrue(self.T.is_empty())
        self.T.add(0, None, None, None, 0, 10, [])
        self.assertFalse(self.T.is_empty())
        self.T.add(2, None, None, self.graph_1, 0.1, 10, [], 0)
        self.assertFalse(self.T.is_empty())


    def test_print_tree(self):
        self.T.add(2, None, None, self.graph_1, 0.1, 10, [], 0)
        self.T.add(3, None, None, self.graph_1, 0.1, 10, [], 2)
        self.T.add(4, None, None, self.graph_1, 0.01, 10, [], 2)
        self.T.add(5, None, None, self.graph_1, 0.1, 10, [], 2)
        self.T.add(6, None, None, self.graph_1, 0.01, 10, [], 4)

        self.T.root.finished = False
        self.T.root.children[0].finished = False
        self.T.root.children[0].children[0].finished = False
        self.T.root.children[0].children[1].finished = False
        self.T.root.children[0].children[2].finished = False
        self.T.root.children[0].children[1].children[0].finished = True

       #print(self.T)
        self.T.print_tree(self.T.root, "")
