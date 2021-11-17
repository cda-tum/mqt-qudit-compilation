from binq.src.evaluation.Clifford_Generator import Clifford_Generator
from binq.src.evaluation.Pauli import H, S, X
from binq.src.evaluation.Verifier import Verifier
from binq.src.architecture_graph.level_Graph import level_Graph
from binq.src.decomposition.Adaptive_decomposition import *
from binq.src.decomposition.QR_decomp import *
import time

################################################



"""
C3 = Clifford_Generator(3,9) #log2(500)=9
C3.generate()
print("ok3")
C5 = Clifford_Generator(5,12)#log2(4000) =circa 12
C5.generate()
print("ok5")
C7 = Clifford_Generator(7,13)# 2^14= 16384
C7.generate()
print("ok7")
"""
################################################




dimension = 3
# graph without ancillas

#####################################################


edges_7 = [(0, 5, {"delta_m": 1, "sensitivity": 5}),
           (0, 4, {"delta_m": 0, "sensitivity": 3}),
           (0, 3, {"delta_m": 0, "sensitivity": 3}),
           (0, 2, {"delta_m": 1, "sensitivity": 5}),
           (1, 4, {"delta_m": 0, "sensitivity": 3}),
           (1, 3, {"delta_m": 1, "sensitivity": 5}),
           (1, 6, {"delta_m": 1, "sensitivity": 5})
           ]
nodes_7 = [ 0, 1, 2, 3, 4, 5, 6]

graph_7 = level_Graph(edges_7, nodes_7, nodes_7, [0])

################################################################

# graph without ancillas
#####################################################


edges_5 = [(0, 3, {"delta_m": 1, "sensitivity": 5}),
           (0, 4, {"delta_m": 0, "sensitivity": 3}),
           (1, 4, {"delta_m": 0, "sensitivity": 3}),
           (1, 2, {"delta_m": 1, "sensitivity": 5})
           ]
nodes_5 = [ 0, 1, 2, 3, 4]

graph_5 = level_Graph(edges_5, nodes_5, nodes_5,  [0])


################################################################

edges_3 = [(0, 2, {"delta_m": 0, "sensitivity": 3}),
           (1, 2, {"delta_m": 0, "sensitivity": 3}),
           ]
nodes_3 = [0, 1, 2]
nmap = [2, 0, 1]

graph_3 = level_Graph(edges_3, nodes_3, nmap,  [0])


###############################################################
#                            EXECUTION

#############################################################

H = H( dimension )

S = S( dimension)

HS = custom_Unitary(matmul(H.matrix, S.matrix), dimension)

X = X(dimension)
###############################################################


QR = QR_decomp(HS, graph_3)


startqr = time.time()
decomp, algorithmic_cost, total_cost = QR.execute()
endqr = time.time()



###############################################################

Adaptive = Adaptive_decomposition(HS, graph_3, (algorithmic_cost, total_cost ), dimension)

start = time.time()
matrices_decomposed, best_cost, final_graph = Adaptive.execute()
end = time.time()

###################################################################

print("QR elapsed time")
QR_time = endqr - startqr
print(QR_time)


print("Adaptive elapsed time")
Adaptive_time = end - start
print(Adaptive_time)

print("COST QR,   ", (algorithmic_cost, total_cost ))
print("BEST COST ADA,   ", best_cost)

final_map = final_graph.lpmap

V1 = Verifier(decomp, HS,  nodes_3, nmap, nmap, dimension)
V2 = Verifier(matrices_decomposed, HS, nodes_3, nmap, final_map, dimension)
print(V1.verify())
print(V2.verify())




#########################################################################################
