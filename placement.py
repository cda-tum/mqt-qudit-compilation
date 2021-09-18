
import networkx as nx


def level_Graph(edges, nodes_number):
    
    G = nx.Graph()
    G.add_nodes_from(list(range(nodes_number)))
    G.add_edges_from(edges)
    
    return G

def distance_nodes(G, source, target):
    path = nx.shortest_path(G, source, target)
    return len(path)-1


def update_list(lst, num_a, num_b):
    new_lst = []

    mod_index = []
    for i, t in enumerate(lst):

        tupla = [0, 0]
        if (t[0] == num_a):
            tupla[0] = 1
        elif (t[0] == num_b):
            tupla[0] = 2

        if (t[1] == num_a):
            tupla[1] = 1
        elif (t[1] == num_b):
            tupla[1] = 2

        mod_index.append(tupla)

    for i, t in enumerate(lst):
        substituter = list(t)

        if (mod_index[i][0] == 1):
            substituter[0] = num_b
        elif (mod_index[i][0] == 2):
            substituter[0] = num_a

        if (mod_index[i][1] == 1):
            substituter[1] = num_b
        elif (mod_index[i][1] == 2):
            substituter[1] = num_a

        new_lst.append(tuple(substituter))

    return new_lst


def swap_nodes(G, node_a, node_b):
    edges = list(G.edges)
    nodes = list(G.nodes)

    attribute_list = []
    for e in edges:
        attribute_list.append(G.get_edge_data(*e))

    swapped_nodes_edges = update_list(edges, node_a, node_b)

    new_edge_list = []
    for i, e in enumerate(swapped_nodes_edges):
        new_edge_list.append((*e, attribute_list[i]))

    return level_Graph(new_edge_list, len(nodes))
