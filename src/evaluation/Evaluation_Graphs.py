from binq.src.architecture_graph.level_Graph import level_Graph



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
nmap7 = [5,6,4,3,1,2,0]
graph_7 = level_Graph(edges_7, nodes_7, nmap7, [0])
"""

edges_7 = [(0, 5, {"delta_m": 1, "sensitivity": 5}),
           (0, 4, {"delta_m": 0, "sensitivity": 3}),
           (0, 3, {"delta_m": 0, "sensitivity": 3}),
           (0, 2, {"delta_m": 1, "sensitivity": 5}),
           (1, 4, {"delta_m": 0, "sensitivity": 3}),
           (1, 3, {"delta_m": 1, "sensitivity": 5}),
           (1, 6, {"delta_m": 1, "sensitivity": 5})
           ]
nodes_7 = [ 0, 1, 2, 3, 4, 5, 6]
nmap7 = [5,6,4,3,1,2,0]
graph_7 = level_Graph(edges_7, nodes_7, nmap7, [0])


edges_7 = [(0, 5, {"delta_m": 1, "sensitivity": 5}),
           (0, 4, {"delta_m": 0, "sensitivity": 3}),
           (0, 3, {"delta_m": 0, "sensitivity": 3}),
           (0, 2, {"delta_m": 1, "sensitivity": 5}),
           (1, 4, {"delta_m": 0, "sensitivity": 3}),
           (1, 3, {"delta_m": 1, "sensitivity": 5}),
           (1, 6, {"delta_m": 1, "sensitivity": 5})
           ]
nodes_7 = [ 0, 1, 2, 3, 4, 5, 6]
nmap7 = [5,6,4,3,1,2,0]
graph_7 = level_Graph(edges_7, nodes_7, nmap7, [0])
"""
################################################################







#####################################################


edges_5 = [(0, 3, {"delta_m": 1, "sensitivity": 5}),
           (0, 4, {"delta_m": 0, "sensitivity": 3}),
           (1, 4, {"delta_m": 0, "sensitivity": 3}),
           (1, 2, {"delta_m": 1, "sensitivity": 5})
           ]
nodes_5 = [ 0, 1, 2, 3, 4]
nmap5 = [ 0, 4, 2, 3, 1]
graph_5 = level_Graph(edges_5, nodes_5, nmap5,  [0])











################################################################

edges_3 = [(0, 2, {"delta_m": 0, "sensitivity": 3}),
           (1, 2, {"delta_m": 0, "sensitivity": 3}),
           ]
nodes_3 = [0, 1, 2]
nmap3 = [2, 1, 0]

graph_3 = level_Graph(edges_3, nodes_3, nmap3,  [0])
