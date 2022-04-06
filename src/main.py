from architecture_graph.level_Graph import level_Graph
from circuit.QuantumCircuit import QuantumCircuit
from circuit.Rotations import Custom_Unitary
from evaluation.Evaluation_Graphs import graph_3_3, nodes_3_3, nmap3_3, graph_5_3,  nodes_5_3, nmap5_3
from evaluation.Pauli import H, S, X
from evaluation.Verifier import Verifier
from utils.r_utils import matmul
import numpy as np

dimension = 3

H1 = H(dimension)
S1 = S(dimension)
X1 = X(dimension)


edges_3_3 = [(1, 0, {"delta_m": 0, "sensitivity": 3}),
             (0, 2, {"delta_m": 0, "sensitivity": 3}),
             ]
nodes_3_3 = [0, 1, 2]
nmap3_3 = [0, 1, 2]

graph_3_3 = level_Graph(edges_3_3, nodes_3_3, nmap3_3, [1])

graph_3_3.phase_storing_setup()
graph_3_3.nodes[0]['phase_storage'] = 0


QC = QuantumCircuit(1, 0, dimension, graph_3_3, verify = True)
#QC.custom_unitary(0, np.identity(dimension, dtype='complex'))
#QC.custom_unitary(1, np.identity(dimension, dtype='complex'))
#QC.custom_unitary(2, np.identity(dimension, dtype='complex'))
#QC.custom_unitary(3, np.identity(dimension, dtype='complex'))
H2 = Custom_Unitary( matmul(H1.matrix, H1.matrix), dimension)
QC.custom_unitary(0, H1.matrix)
QC.custom_unitary(0, H1.matrix)


"""
QC.R(0, 1, 2, 0, 1)

QC.Rz(0, 1, 0)
QC.Rz(0, 1, 0)

QC.R(0, 1, 2, 0, 2)

QC.Rz(0, 1, 0)
QC.Rz(0, 2, 1)
QC.Rz(0, 3, 2)

QC.R(0, 1, 2, 1, 2)

QC.Rz(0, 1, 0)
"""

QC.draw()

QC.DFS_decompose()

V2 = Verifier(QC.qreg[0], H2, nodes_3_3, nmap3_3, QC.energy_level_graph.lpmap, dimension)
V2r = V2.verify()

print()
QC.draw()

print()
print("Zprop")


QC.Z_prop(back = False)

V2 = Verifier(QC.qreg[0], H2, nodes_3_3, nmap3_3, QC.energy_level_graph.lpmap, dimension)
V2rZ = V2.verify()

print()
QC.draw()
#QC.to_json("/home/k3vn/Desktop/")
print("DONE")
