from src.architecture_graph.level_Graph import level_Graph
from src.evaluation.Pauli import H
from src.circuit.QuantumCircuit import QuantumCircuit



dimension = 3 # select dimension of your single qudit .


# declare the edges on the energy level graph between logic states .
edges = [
        (1, 0, {"delta_m": 0, "sensitivity": 3}),
        (0, 2, {"delta_m": 0, "sensitivity": 3}),
        ]
        
# name explicitly the logic states .
nodes = [0, 1, 2]

# declare physical levels in order of maping of the logic states just declared .
# i.e. here we will have Logic 0 -> Phys. 0, have Logic 1 -> Phys. 1, have Logic 1 -> Phys. 1 .

nmap = [0, 1, 2]

# Construct the qudit energy level graph, the last field is the list of logic state that are used for the calibrations of the operations.
# note: only the first is one counts in our current cost fucntion.

graph = level_Graph(edges, nodes, nmap, [1])


# Construct quantum circuit with 1 qudit, 0 classical bit, dimension of the qudit, graph of the qudit, flag for compile with verification .
QC = QuantumCircuit(1, 0, dimension, graph, verify = True)


# add custom gate to qudit 0, the matrix field is a nump array .
QC.custom_unitary(0, H(dimension).matrix)

# Visualize initial circuit .
QC.draw()

# Compile .
QC.DFS_decompose()

# alternative : QR_decompose()

# Propagate Z gates backwards .
QC.Z_prop(back = True)

# Visualize the results
QC.draw()

# Save the results to json .
path = "./"
QC.to_json(path)



# NOTE: for customizing the cost functions access file ./src/utils/cost_functions.py
