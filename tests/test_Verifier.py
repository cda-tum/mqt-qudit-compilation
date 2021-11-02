from unittest import TestCase

from binq.src.architecture_graph.level_Graph import level_Graph
from binq.src.decomposition.Adaptive_decomposition import Adaptive_decomposition
from binq.src.decomposition.QR_decomp import QR_decomp
from binq.src.evaluation.Pauli import H
from binq.src.evaluation.Verifier import Verifier


class TestVerifier(TestCase):

    def setUp(self) -> None:
        self.dimension = 5

        edges_5 = [(0, 3, {"delta_m": 1, "sensitivity": 5}),
                   (0, 4, {"delta_m": 0, "sensitivity": 3}),
                   (1, 4, {"delta_m": 0, "sensitivity": 3}),
                   (1, 2, {"delta_m": 1, "sensitivity": 5})
                   ]
        nodes_5 = [0, 1, 2, 3, 4]

        ## NODES CAN BE INFERRED BY THE EDGES
        self.graph_5 = level_Graph(edges_5, nodes_5)
        self.graph_5.define__states([1], [0], [2, 3, 4])

        self.H = H( self.dimension )

    def test_verify(self):

        QR = QR_decomp(self.H, self.graph_5)
        decomp, total_cost = QR.execute()
        Adaptive = Adaptive_decomposition(self.H, self.graph_5, total_cost)
        matrices_decomposed, best_cost, final_graph = Adaptive.execute()

        V1 = Verifier(decomp, self.H, self.dimension)
        V2 = Verifier(matrices_decomposed, self.H,  self.dimension)
        self.assertTrue(V1.verify())
        self.assertTrue(V2.verify())
