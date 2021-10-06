from QuantumCircuit import *

from binq.src.decomposition.BFS import *
from binq.src.decomposition.algorithm import *
import timeit


dimension = 6
edges = [(0,5, {"delta_m":0, "sensitivity": 1}),
         (0,4, {"delta_m":0, "sensitivity": 1}),
         (0,3, {"delta_m":1, "sensitivity": 3}),
         (0,2, {"delta_m":1, "sensitivity": 3}),
         (1,5, {"delta_m":0, "sensitivity": 1}),
         (1,4, {"delta_m":0, "sensitivity": 1}),
         (1,3, {"delta_m":1, "sensitivity": 3}),
         (1,2, {"delta_m":1, "sensitivity": 3})
         ]

# to access attribute graph[node 1][node 2][name attr]
circ = QuantumCircuit(1, 1, dimension)
circ.energy_level_graph(edges)

print(circ.energy_level_graph.nodes)

"""
U= np.array([[0.57735 + 0.00000j ,  0.57735 + 0.00000j,   0.57735 + 0.00000j],
             [0.57735 + 0.00000j,  -0.28868 + 0.50000j , -0.28868 - 0.50000j],
             [0.57735 + 0.00000j,  -0.28868 - 0.50000j , -0.28868 + 0.50000j]],dtype='complex')
"""
U = np.array([[ 0.95105652+0.j ,     0.+0.j,    0.+0.j,     0.+0.j,     0.+0.j,    -0.25+0.18163563j],
            [ 0.0954915 +0.j,   0.9045085 +0.j, 0.23776413-0.17274575j,  0.+0.j,     0.+0.j,     0.23776413-0.17274575j],
            [ 0.+0.j,   -0.25-0.18163563j,  0.95105652+0.j,     0.+0.j,     0.+0.j ,    0.+0.j],
            [ 0.+0.j ,  0.+0.j,     0.+0.j, 1.+0.j,     0.+0.j,      0.+0.j ],
            [ 0.+0.j ,     0. +0.j ,      0. +0.j,  0.  +0.j,     1. +0.j,     0. +0.j   ]  ,
            [ 0.23776413+0.17274575j,  -0.23776413-0.17274575j,  -0.0954915 +0.j, 0. +0.j  ,    0.  +0.j  ,   0.9045085 +0.j ]])

standard_decomp, cost_limit = algorithm(U , circ)


TREE = N_ary_Tree()
TREE.add(0, custom_Unitary(np.identity(3, dtype='complex' ),  3), U, 0, cost_limit)


start = timeit.timeit()
BFS(TREE.root, circ)
end = timeit.timeit()

print("elapsed time")
print(end - start)



decomp, best_cost = TREE.retrieve_decomposition(TREE.root)
matrices_decomposed = Z_extraction(decomp)

tree_print = TREE.print_tree(TREE.root,"TREE: ")
print(tree_print)

for m in matrices_decomposed:
    print(m)
print("\n:)__:)__:)__:)__:)__:)__:)__:)__:)__:)__:)__:)__:)__:)__:)")






