from unittest import TestCase
import numpy as np

from circuit.Rotations import Custom_Unitary
from src.architecture_graph.level_Graph import level_Graph
from src.decomposition.Adaptive_decomposition import Adaptive_decomposition
from src.decomposition.QR_decomp import QR_decomp
from src.evaluation.Pauli import H, X
from src.evaluation.Verifier import Verifier


class TestVerifier(TestCase):

    def setUp(self) -> None:


        edges = [(0, 3, {"delta_m": 1, "sensitivity": 5}),
                   (0, 4, {"delta_m": 0, "sensitivity": 3}),
                   (1, 4, {"delta_m": 0, "sensitivity": 3}),
                   (1, 2, {"delta_m": 1, "sensitivity": 5})
                   ]
        nodes = [0, 1, 2, 3, 4]
        nodes_map = [0, 2, 1, 4, 3]


        self.graph = level_Graph(edges, nodes, nodes_map, [0])



    def test_verify(self):

        dimension = 2

        sequence = [ Custom_Unitary( np.identity( dimension, dtype='complex'), dimension),
                     H(dimension),
                     H(dimension)
                    ]
        target = Custom_Unitary( np.identity( dimension, dtype='complex'), dimension)

        nodes = [0, 1]
        initial_map = [0, 1]
        final_map = [0, 1]

        V1 = Verifier(sequence, target, nodes, initial_map, final_map, dimension)

        self.assertTrue( V1.verify() )

        ##################################################################

        dimension = 3

        nodes_3 = [0, 1, 2]
        initial_map_3 = [0, 1, 2]
        final_map_3 = [0, 2, 1]
        V1.dimension = 3

        sequence_3 = [Custom_Unitary(np.identity(dimension, dtype='complex'), dimension),
                    H(dimension),
                    X(dimension),
                    X(dimension),
                    X(dimension)
                    ]

        target_3 = H(dimension)

        V1 = Verifier(sequence_3, target_3, nodes_3, initial_map_3, final_map_3, dimension)

        self.assertTrue(V1.verify())




