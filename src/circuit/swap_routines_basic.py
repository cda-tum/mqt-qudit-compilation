import networkx as nx
import numpy as np


from src.circuit.Rotations import R

from src.utils.r_utils import rotation_cost_calc

def swap_elements(l, i, j):
    a = l[i]
    b = l[j]
    l[i] = b
    l[j] = a
    return l


def phase_storage_processing(gate, graph):
    #return gate, graph # DEBUG LINE


    inode = graph._1stInode
    if 'phase_storage' not in graph.nodes[inode]:
        return gate, graph

    g_lev_a = gate.lev_a
    g_lev_b = gate.lev_b
    new_g_phi = gate.phi # old phase still inside the gate

    #find node by physical level associated
    logic_nodes =[None, None]
    for n, d in graph.nodes(data=True):
        if(d['lpmap'] == g_lev_a):
            logic_nodes[0] = n
        if(d['lpmap'] == g_lev_b):
            logic_nodes[1] = n

    if(logic_nodes[0] != None):
        new_g_phi = new_g_phi + graph.nodes[logic_nodes[0]]['phase_storage']
    if(logic_nodes[1] != None):
        new_g_phi = new_g_phi - graph.nodes[logic_nodes[1]]['phase_storage']


    #only pi pulses can update online the graph
    if(gate.phi < 0 and ( abs( abs(gate.theta)-3.14)<1e-2) and ( abs(abs(gate.phi)-1.57)<1e-2)):
        graph.nodes[logic_nodes[1]]['phase_storage'] = graph.nodes[logic_nodes[1]]['phase_storage'] + np.pi
    elif( gate.phi > 0 and ( abs( abs(gate.theta)-3.14)<1e-2) and ( abs(abs(gate.phi)-1.57)<1e-2) ):
        graph.nodes[logic_nodes[0]]['phase_storage'] = graph.nodes[logic_nodes[0]]['phase_storage'] + np.pi

    fixed_gate = R(gate.theta, new_g_phi, g_lev_a, g_lev_b, gate.dimension)

    return fixed_gate, graph


def gate_chain_condition(previous_gates, current):
    if(not previous_gates):
        return current
    new_source = current.lev_a
    new_target = current.lev_b
    theta = current.theta
    phi = current.phi


    last_gate = previous_gates[-1]
    last_source = last_gate.lev_a
    last_target = last_gate.lev_b

    # all phi flips are removed because already applied
    if(new_source == last_source):
        if( new_target > last_target): # changed lower one with lower one
            pass
        elif( new_target < last_target ): # changed higher one one with lower
            pass

    elif(new_target == last_target):
        if(new_source < last_source):
            theta = theta * -1
        elif(new_source > last_source):
            theta = theta * -1

    elif (new_source == last_target):
        theta = theta * -1

    elif (new_target == last_source):
        pass


    return  R(theta, phi, current.lev_a, current.lev_b, current.dimension )


def route_states2rotate_basic(gate, orig_placement):

    placement = orig_placement

    dimension = gate.dimension

    cost_of_pi_pulses = 0
    pi_pulses_routing = []

    source = gate.original_lev_a #
    target = gate.original_lev_b #

    path = nx.shortest_path(placement, source, target)

    i = len(path)-2

    while(i > 0):

        phy_n_i = placement.nodes[path[i]]['lpmap']
        phy_n_ip1 = placement.nodes[path[i+1]]['lpmap']


        pi_gate_phy = R(np.pi, -np.pi/2, phy_n_i , phy_n_ip1, dimension)



        pi_gate_phy  = gate_chain_condition(pi_pulses_routing, pi_gate_phy)



        pi_pulses_routing.append( pi_gate_phy )

        # doesnt really matter its just logical, we need only the angle
        pi_gate_logic = R(np.pi, -np.pi/2, path[i], path[i + 1], dimension)
        ####

        cost_of_pi_pulses += rotation_cost_calc( pi_gate_logic, placement )

        placement = placement.swap_nodes(path[i+1], path[i])
        path = swap_elements(path, i+1, i)

        pi_gate_phy, placement = phase_storage_processing(pi_gate_phy, placement)

        i -= 1

    return ( cost_of_pi_pulses, pi_pulses_routing, placement )