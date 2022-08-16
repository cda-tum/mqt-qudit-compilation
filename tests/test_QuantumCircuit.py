from unittest import TestCase

from src.architecture_graph.level_Graph import level_Graph
from src.circuit.QuantumCircuit import QuantumCircuit
import numpy as np

from src.circuit.Rotations import R
from src.evaluation.Pauli import H
from src.evaluation.Verifier import Verifier
from src.utils.r_utils import matmul


class TestQuantumCircuit(TestCase):
    def setUp(self) -> None:
        test_sample_edges = [(0, 2, {"delta_m": 0, "sensitivity": 1}),
                             (1, 2, {"delta_m": 0, "sensitivity": 1}),
                             ]
        test_sample_nodes = [0, 1, 2]
        test_sample_nodes_map = [1, 0, 2]

        self.graph_1 = level_Graph(test_sample_edges, test_sample_nodes, test_sample_nodes_map, [0])
        self.graph_1.phase_storing_setup()

        self.QC = QuantumCircuit(1, 0, 3, self.graph_1, True)

    def test_r(self):
        self.QC.R(0, np.pi, np.pi / 2, 0, 1)
        testing_matrix = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        self.assertTrue(np.allclose(testing_matrix, self.QC.qreg[0][0].matrix))

    def test_rz(self):
        self.QC.Rz(0, np.pi, 0)
        testing_matrix = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.assertTrue(np.allclose(testing_matrix, self.QC.qreg[0][0].matrix))

    def test_custom_unitary(self):
        prepare_custom = matmul(R(np.pi , np.pi / 2, 0, 1, 3).matrix, R(np.pi , np.pi / 2, 0, 1, 3).matrix)
        self.QC.custom_unitary(0, prepare_custom)
        testing_matrix = R(2*np.pi, np.pi / 2, 0, 1, 3).matrix
        self.assertTrue(np.allclose(testing_matrix, self.QC.qreg[0][0].matrix))


    def test_dfs_decompose(self):
        Htest = H(3)
        self.QC.custom_unitary(0, Htest.matrix)
        self.QC.DFS_decompose()

        test_sample_nodes = [0, 1, 2]
        test_sample_nodes_map = [1, 0, 2]

        V = Verifier(self.QC.qreg[0], H(3), test_sample_nodes, test_sample_nodes_map, self.QC.energy_level_graph.lpmap,
                     3)
        self.assertEqual(len(self.QC.qreg[0]), 7)
        self.assertTrue(V.verify())


        ##############################################

        dim = 5
        test_sample_edges = [(0, 4, {"delta_m": 0, "sensitivity": 1}),
                             (0, 3, {"delta_m": 1, "sensitivity": 3}),
                             (0, 2, {"delta_m": 1, "sensitivity": 3}),
                             (1, 4, {"delta_m": 0, "sensitivity": 1}),
                             (1, 3, {"delta_m": 1, "sensitivity": 3}),
                             (1, 2, {"delta_m": 1, "sensitivity": 3})
                             ]
        test_sample_nodes = [0, 1, 2, 3, 4]
        test_sample_nodes_map = [3, 2, 4, 1, 0]

        graph_1 = level_Graph(test_sample_edges, test_sample_nodes, test_sample_nodes_map, [0])
        graph_1.phase_storing_setup()
        self.QC = QuantumCircuit(1, 0, dim, graph_1, True)

        Htest = H(dim)

        self.QC.custom_unitary(0, Htest.matrix)
        self.QC.DFS_decompose()


        V = Verifier(self.QC.qreg[0], H(dim), test_sample_nodes, test_sample_nodes_map, self.QC.energy_level_graph.lpmap,
                     dim)
        self.assertEqual(len(self.QC.qreg[0]), 17)
        self.assertTrue(V.verify())


    def test_qr_decompose(self):
        Htest = H(3)
        self.QC.custom_unitary(0, Htest.matrix)
        self.QC.QR_decompose()

        test_sample_nodes = [0, 1, 2]
        test_sample_nodes_map = [1, 0, 2]

        V = Verifier(self.QC.qreg[0], H(3), test_sample_nodes, test_sample_nodes_map, self.QC.energy_level_graph.lpmap, 3)
        self.assertEqual(len(self.QC.qreg[0]), 7)
        self.assertTrue(V.verify())


