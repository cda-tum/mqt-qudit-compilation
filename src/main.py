from circuit.QuantumCircuit import QuantumCircuit
from evaluation.Evaluation_Graphs import graph_3_3
from evaluation.Pauli import H, S, X

dimension = 3

H1 = H(dimension)
S1 = S(dimension)
X1 = X(dimension)


QC = QuantumCircuit(1, 0, dimension, graph_3_3)

QC.R(0, 1, 2, 0, 1)

QC.Rz(0, 1, 0)
QC.Rz(0, 1, 0)

QC.R(0, 1, 2, 0, 2)

QC.Rz(0, 1, 0)
QC.Rz(0, 2, 1)
QC.Rz(0, 3, 2)

QC.R(0, 1, 2, 1, 2)

QC.Rz(0, 1, 0)

QC.draw()

QC.DFS_decompose()
print("Zprop")
QC.Z_prop(back=True)

QC.draw()
#QC.to_json("/home/k3vn/Desktop/")
print("DONE")
