from architecture_graph.level_Graph import level_Graph
from circuit.QuantumCircuit import QuantumCircuit
from evaluation.Pauli import H, S, X

dimension = 5
H1 = H(dimension)
S1 = S(dimension)
X1 = X(dimension)

edges_5 = [(0, 3, {"delta_m": 1, "sensitivity": 5}),
(0, 4, {"delta_m": 0, "sensitivity": 3}),
(1, 4, {"delta_m": 0, "sensitivity": 3}),
(1, 2, {"delta_m": 1, "sensitivity": 5})
]
nodes_5 = [ 0, 1, 2, 3, 4]
nmap5 = [ 0, 4, 2, 3, 1]
graph_5 = level_Graph(edges_5, nodes_5, nmap5, [0])


QC = QuantumCircuit(4, 0, dimension, graph_5)


QC.draw()

print("ADDED GATE")
for i in range(2):
    for j in range(4):
        QC.custom_unitary(j, H1.matrix)

QC.draw()
print("DECOMPOSE")

QC.DFS_decompose()
#QC.Z_prop()

QC.draw()
print("DONE")

QC = QuantumCircuit(4, 0, dimension, graph_5)


QC.draw()

print("ADDED GATE")
for i in range(5):
    for j in range(4):
        QC.custom_unitary(j, H1.matrix)

QC.draw()
print("DECOMPOSE")

QC.QR_decompose()
#QC.Z_prop()

QC.draw()
print("DONE")

