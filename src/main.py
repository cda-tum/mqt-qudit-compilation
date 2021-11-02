from binq.src.evaluation.Pauli import H
from binq.src.evaluation.Verifier import Verifier
from binq.src.architecture_graph.level_Graph import level_Graph
from binq.src.decomposition.Adaptive_decomposition import *
from binq.src.decomposition.QR_decomp import *
import timeit

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

#-------------------------------------------------------------

###############################################################
QR = QR_decomp(H, graph_3)


startqr = timeit.timeit()
decomp, total_cost = QR.execute()
endqr = timeit.timeit()



###############################################################

Adaptive = Adaptive_decomposition(H, graph_3, total_cost)

start = timeit.timeit()
matrices_decomposed, best_cost, final_graph = Adaptive.execute()
end = timeit.timeit()



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