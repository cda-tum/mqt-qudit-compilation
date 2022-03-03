from circuit.QuantumCircuit import QuantumCircuit
from circuit.Rotations import Custom_Unitary
from evaluation.Evaluation_Graphs import graph_3_3, nodes_3_3, nmap3_3, graph_5_3,  nodes_5_3, nmap5_3
from evaluation.Pauli import H, S, X
from evaluation.Verifier import Verifier
from utils.r_utils import matmul

dimension = 5

H1 = H(dimension)
S1 = S(dimension)
X1 = X(dimension)


QC = QuantumCircuit(1, 0, dimension, graph_5_3, verify= True)
QC.custom_unitary(0, H1.matrix)
QC.custom_unitary(0, H1.matrix)
H2 = Custom_Unitary( matmul(H1.matrix, H1.matrix), dimension)


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

V2 = Verifier(QC.qreg[0], H2, nodes_5_3, nmap5_3, QC.energy_level_graph.lpmap, dimension)
V2r = V2.verify()

print()
QC.draw()

print()
print("Zprop")


QC.Z_prop(back = True)

V2 = Verifier(QC.qreg[0], H2, nodes_5_3, nmap5_3, QC.energy_level_graph.lpmap, dimension)
V2rZ = V2.verify()

print()
QC.draw()
#QC.to_json("/home/k3vn/Desktop/")
print("DONE")
