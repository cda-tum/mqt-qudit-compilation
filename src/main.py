from binq.src.evaluation.Pauli import H, S
from binq.src.evaluation.Verifier import Verifier
from binq.src.architecture_graph.level_Graph import level_Graph
from binq.src.decomposition.Adaptive_decomposition import *
from binq.src.decomposition.QR_decomp import *
import time

################################################


dimension = 3


# graph without ancillas

# DISCLAIMER: THERE SHOULD BE AT LEAST ALWAYS TWO -contiguous- LOGIC LEVELS
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

## NODES CAN also BE INFERRED BY THE EDGES
graph_7 = level_Graph(edges_7, nodes_7)
graph_7.define__states([1], [0], [ 2, 3, 4, 5, 6])

################################################################

# graph without ancillas
#####################################################


edges_5 = [(0, 3, {"delta_m": 1, "sensitivity": 5}),
           (0, 4, {"delta_m": 0, "sensitivity": 3}),
           (1, 4, {"delta_m": 0, "sensitivity": 3}),
           (1, 2, {"delta_m": 1, "sensitivity": 5})
           ]
nodes_5 = [ 0, 1, 2, 3, 4]

## NODES CAN BE INFERRED BY THE EDGES
graph_5 = level_Graph(edges_5, nodes_5)
graph_5.define__states([1], [0], [ 2, 3, 4])

################################################################

edges_3 = [(0, 2, {"delta_m": 0, "sensitivity": 3}),
           (1, 2, {"delta_m": 0, "sensitivity": 3}),
           ]
nodes_3 = [0, 1, 2 ]

## NODES CAN BE INFERRED BY THE EDGES
graph_3 = level_Graph(edges_3, nodes_3)
graph_3.define__states([1], [0], [ 2])

###############################################################
#                            EXECUTION

#############################################################

H = H( dimension )




S = S( dimension)
HS = custom_Unitary(matmul(H.matrix, S.matrix), dimension)
R02 = R(np.pi, 0 , 0, 2, dimension) # already native uncompilable
R12 = R(np.pi, 0 , 1, 2, dimension)

R_custom = custom_Unitary(matmul(HS.matrix, R12.matrix), dimension)

#-------------------------------------------------------------

###############################################################
QR = QR_decomp(HS, graph_3)


startqr = time.time()
decomp, total_cost = QR.execute()
endqr = time.time()



###############################################################

Adaptive = Adaptive_decomposition(HS, graph_3, total_cost)

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

print("COST QR,   ", total_cost)
print("BEST COST ADA,   ", best_cost)



V1 = Verifier(decomp, H, dimension)
V2 = Verifier(matrices_decomposed, H, dimension)
is_correct = V1.verify()
is_correct = V2.verify()


#########################################################################################