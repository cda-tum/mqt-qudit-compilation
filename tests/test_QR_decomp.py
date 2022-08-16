from unittest import TestCase

from architecture_graph.level_Graph import level_Graph
from decomposition.QR_decomp import QR_decomp
from evaluation.Pauli import H
from evaluation.Verifier import Verifier


class TestQR_decomp(TestCase):
    def test_execute(self):

        ##### DIM 3
        dim = 3
        test_sample_edges = [(0, 2, {"delta_m": 0, "sensitivity": 1}),
                             (1, 2, {"delta_m": 0, "sensitivity": 1}),
                             ]
        test_sample_nodes = [0, 1, 2]
        test_sample_nodes_map = [0, 1, 2]

        graph_1 = level_Graph(test_sample_edges, test_sample_nodes, test_sample_nodes_map, [0])

        Htest = H(dim)
        QR = QR_decomp(Htest, graph_1, Z_prop = False, not_stand_alone = False)

        decomp, algorithmic_cost, total_cost = QR.execute()

        V = Verifier(decomp, Htest, test_sample_nodes, test_sample_nodes_map, graph_1.lpmap, dim)
        self.assertEqual(len(decomp), 7)
        self.assertTrue(V.verify())

        self.assertEqual( (decomp[0].lev_a,decomp[0].lev_b ), (1, 2))
        self.assertEqual( (decomp[1].lev_a, decomp[0].lev_b), (1, 2))
        self.assertEqual( (decomp[2].lev_a, decomp[0].lev_b), (0, 2))
        self.assertEqual( (decomp[3].lev_a, decomp[0].lev_b), (1, 2))
        self.assertEqual( (decomp[4].lev_a, decomp[0].lev_b), (1, 2))
        self.assertEqual( decomp[5].lev, 1)
        self.assertEqual( decomp[6].lev, 2)

