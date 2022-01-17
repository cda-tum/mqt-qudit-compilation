from src.architecture_graph.level_Graph import level_Graph



#####################################################


edges_7_1 = [(0, 6, {"delta_m": 1, "sensitivity": 5}),
           (0, 4, {"delta_m": 0, "sensitivity": 3}),
           (0, 1, {"delta_m": 0, "sensitivity": 3}),
           (2, 1, {"delta_m": 0, "sensitivity": 3}),
           (2, 5, {"delta_m": 1, "sensitivity": 5}),
           (2, 3, {"delta_m": 1, "sensitivity": 5})
           ]
nodes_7_1 = [ 0, 1, 2, 3, 4, 5, 6]
nmap7_1 =    [0, 2, 1, 6, 3, 4, 5]
graph_7_1 = level_Graph(edges_7_1, nodes_7_1, nmap7_1, [0])



edges_7_2 = [(6, 0, {"delta_m": 1, "sensitivity": 5}),
           (6, 5, {"delta_m": 0, "sensitivity": 3}),
           (6, 3, {"delta_m": 0, "sensitivity": 3}),
           (1, 5, {"delta_m": 0, "sensitivity": 3}),
           (1, 4, {"delta_m": 0, "sensitivity": 3}),
           (1, 3, {"delta_m": 1, "sensitivity": 5}),
           (1, 2, {"delta_m": 1, "sensitivity": 5})
           ]
nodes_7_2 = [ 0, 1, 2, 3, 4, 5, 6]
nmap7_2 =   [ 3, 2, 1, 4, 6, 5, 0]
graph_7_2 = level_Graph(edges_7_2, nodes_7_2, nmap7_2, [0])


edges_7_3 = [(1, 0, {"delta_m": 1, "sensitivity": 5}),
               (1, 2, {"delta_m": 0, "sensitivity": 3}),
                (1, 3, {"delta_m": 0, "sensitivity": 3}),
               (4, 2, {"delta_m": 0, "sensitivity": 3}),
               (4, 3, {"delta_m": 0, "sensitivity": 3}),
               (4, 5, {"delta_m": 1, "sensitivity": 5}),
               (4, 6, {"delta_m": 1, "sensitivity": 5})
               ]
nodes_7_3 = [ 0, 1, 2, 3, 4, 5, 6 ]
nmap7_3 =   [ 0, 5, 2, 6, 4, 3, 1 ]
graph_7_3 = level_Graph(edges_7_3, nodes_7_3, nmap7_3, [3])

################################################################




edges_5 = [(0, 3, {"delta_m": 1, "sensitivity": 5}),
(0, 4, {"delta_m": 0, "sensitivity": 3}),
(1, 4, {"delta_m": 0, "sensitivity": 3}),
(1, 2, {"delta_m": 1, "sensitivity": 5})
]
nodes_5 = [ 0, 1, 2, 3, 4]
nmap5 = [ 0, 4, 2, 3, 1]
graph_5 = level_Graph(edges_5, nodes_5, nmap5, [0])


#####################################################


edges_5_1 = [(4, 1, {"delta_m": 1, "sensitivity": 5}),
           (4, 3, {"delta_m": 0, "sensitivity": 3}),
           (0, 3, {"delta_m": 0, "sensitivity": 3}),
           (0, 2, {"delta_m": 1, "sensitivity": 5})
           ]
nodes_5_1 = [ 0, 1, 2, 3, 4]
nmap5_1 =   [ 2, 1, 3, 4, 0]
graph_5_1 = level_Graph(edges_5_1, nodes_5_1, nmap5_1,  [0])


edges_5_2 = [(3, 0, {"delta_m": 1, "sensitivity": 5}),
               (3, 1, {"delta_m": 0, "sensitivity": 3}),
               (3, 4, {"delta_m": 0, "sensitivity": 3}),
               (2, 4, {"delta_m": 0, "sensitivity": 3}),
               (2, 1, {"delta_m": 1, "sensitivity": 5})
               ]
nodes_5_2 = [ 0, 1, 2, 3, 4]
nmap5_2 =   [ 3, 2, 1, 4, 0]
graph_5_2 = level_Graph(edges_5_2, nodes_5_2, nmap5_2,  [0])


edges_5_3 = [(4, 1, {"delta_m": 1, "sensitivity": 5}),
             (4, 2, {"delta_m": 0, "sensitivity": 3}),
             (4, 0, {"delta_m": 0, "sensitivity": 3}),
             (3, 1, {"delta_m": 1, "sensitivity": 5})
            ]
nodes_5_3 = [ 0, 1, 2, 3, 4]
nmap5_3 =   [ 2, 0, 1, 4, 3]
graph_5_3 = level_Graph(edges_5_3, nodes_5_3, nmap5_3,  [3])






################################################################

edges_3_1 = [(1, 2, {"delta_m": 0, "sensitivity": 3}),
            (0, 2, {"delta_m": 0, "sensitivity": 3}),
           ]
nodes_3_1 = [0, 1, 2]
nmap3_1 =   [2, 0, 1]

graph_3_1 = level_Graph(edges_3_1, nodes_3_1, nmap3_1,  [0])



edges_3_2 = [(2, 1, {"delta_m": 0, "sensitivity": 3}),
            (0, 1, {"delta_m": 0, "sensitivity": 3}),
           ]
nodes_3_2 = [0, 1, 2]
nmap3_2 =   [1, 2, 0]

graph_3_2 = level_Graph(edges_3_2, nodes_3_2, nmap3_2,  [0])




edges_3_3 = [(1, 0, {"delta_m": 0, "sensitivity": 3}),
            (0, 2, {"delta_m": 0, "sensitivity": 3}),
            ]
nodes_3_3 = [0, 1, 2]
nmap3_3 =   [0, 1, 2]

graph_3_3 = level_Graph(edges_3_3, nodes_3_3, nmap3_3,  [1])
#-----------------------------------------------------------------


edges_3_4 = [(1, 0, {"delta_m": 0, "sensitivity": 3}),
            (0, 2, {"delta_m": 0, "sensitivity": 3}),
            ]
nodes_3_4 = [0, 1, 2]
nmap3_4 =   [0, 1, 2]

graph_3_4 = level_Graph(edges_3_4, nodes_3_4, nmap3_4,  [0])

######################################################
######################################################

edges_7_4 = [(1, 0, {"delta_m": 1, "sensitivity": 5}),
               (1, 2, {"delta_m": 0, "sensitivity": 3}),
               (1, 3, {"delta_m": 0, "sensitivity": 3}),
               (4, 2, {"delta_m": 0, "sensitivity": 3}),
               (4, 3, {"delta_m": 0, "sensitivity": 3}),
               (4, 5, {"delta_m": 1, "sensitivity": 5}),
               (4, 6, {"delta_m": 1, "sensitivity": 5})
               ]
nodes_7_4 = [ 0, 1, 2, 3, 4, 5, 6]
nmap7_4 =   [ 0, 5, 2, 6, 4, 3, 1 ]
graph_7_4 = level_Graph(edges_7_4, nodes_7_4, nmap7_4, [0])


