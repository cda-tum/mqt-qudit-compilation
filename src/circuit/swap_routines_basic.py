import networkx as nx
import numpy as np


from binq.src.circuit.Rotations import R

from binq.src.utils.r_utils import rotation_cost_calc



def swap_elements(l, i, j):
    a = l[i]
    b = l[j]
    l[i] = b
    l[j] = a
    return l



def route_states2rotate_basic(gate, orig_placement):

    placement = orig_placement

    dimension = gate.dimension

    cost_of_pi_pulses = 0
    pi_pulses_routing = []

    source = gate.original_lev_a
    target = gate.original_lev_b

    path = nx.shortest_path(placement, source, target)

    i = len(path)-2

    while(i > 0):

        phy_n_i = placement.nodes[path[i]]['lpmap']
        phy_n_ip1 = placement.nodes[path[i+1]]['lpmap']

        pi_gate_phy = R(np.pi, 0, phy_n_i , phy_n_ip1, dimension)
        pi_pulses_routing.append( pi_gate_phy )

        pi_gate_logic = R(np.pi, 0, path[i] , path[i+1], dimension)
        cost_of_pi_pulses += rotation_cost_calc( pi_gate_logic, placement )

        placement = placement.swap_nodes(path[i+1], path[i])
        path = swap_elements(path, i+1, i)

        i -= 1

    return ( cost_of_pi_pulses, pi_pulses_routing, placement )