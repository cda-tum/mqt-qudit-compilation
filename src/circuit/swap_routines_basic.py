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

def gate_chain_condition(previous_gates, current):
    if(not previous_gates):
        return current
    new_source = current.lev_a
    new_target = current.lev_b
    theta = current.theta
    phi = current.phi

    #######################################
    #correction
    #l = len(previous_gates)
    phi = phi + len(previous_gates)* np.pi
    ##########################################

    last_gate = previous_gates[-1]
    last_source = last_gate.lev_a  #original_lev_a R10 -> R01 leva levb -> matrix
    last_target = last_gate.lev_b  #original_lev_b

    # Very unelegant sequence of if-s
    if(new_source == last_source):
        if( new_target > last_target): # changed lower one with lower one
            pass
        elif( new_target < last_target ): # changed higher one one with lower
            phi = phi * -1
    elif(new_target == last_target):
        if(new_source < last_source): # changed
            theta = theta * -1
        elif(new_source > last_source):
            theta = theta * -1
            phi = phi * -1
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
    #print("----")
    i = len(path)-2

    while(i > 0):

        phy_n_i = placement.nodes[path[i]]['lpmap']
        phy_n_ip1 = placement.nodes[path[i+1]]['lpmap']
        #print("PI PULSEEEEEEEEEEEEEEEEEEEE")
        if (phy_n_i > phy_n_ip1):
            pi_gate_phy = R(np.pi, -np.pi/2, phy_n_i , phy_n_ip1, dimension) # TODO CHANGE BACK TO + PI/2
        else:
            pi_gate_phy = R(np.pi, np.pi/2, phy_n_i, phy_n_ip1, dimension)


        pi_gate_phy  = gate_chain_condition(pi_pulses_routing, pi_gate_phy)
        pi_pulses_routing.append( pi_gate_phy )


        pi_gate_logic = R(np.pi, np.pi, path[i], path[i + 1], dimension) # doesnt really matter its just logical

        cost_of_pi_pulses += rotation_cost_calc( pi_gate_logic, placement )

        placement = placement.swap_nodes(path[i+1], path[i])
        path = swap_elements(path, i+1, i)

        i -= 1

    return ( cost_of_pi_pulses, pi_pulses_routing, placement )