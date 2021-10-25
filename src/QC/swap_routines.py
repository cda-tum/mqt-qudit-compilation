####################################################################
####################################################################
########################### OUT OF CLASS ###########################
####################################################################
# TODO TO INTEGRATE WITH QUANTUM CIRCUIT CLASS

import networkx as nx
import numpy as np

from binq.src.QC.Rotations import R
from binq.src.utils.costs_utils import rotation_cost_calc




def pi_swap_routine(i, next, placement, dimension):

    swapping_list = []
    cost = 0

    trace = list(range(next, i+2))
    trace.reverse()
    index = 0

    while(index < len(trace)-1):
        pi_gate = R(np.pi, 0, trace[index] , trace[index+1] , dimension)
        swapping_list.append(pi_gate)
        cost += rotation_cost_calc( pi_gate, placement )

        placement = placement.swap_nodes(trace[index], trace[index+1])

        index += 1

    while (index > 0):
        pi_gate = R(np.pi, 0, trace[index-1], trace[index], dimension)
        swapping_list.append(pi_gate)
        cost += rotation_cost_calc(pi_gate, placement)

        placement = placement.swap_nodes(trace[index-1], trace[index])
        index -= 1

    return (cost, swapping_list, placement)



def find_next_available(i, lista):
    counter = i-1
    while(counter > 0):
        if(lista[counter] >= 0):
            return counter
        c = c-1

    return -1

def route_states2rotate(gate, placement):

    dimension = gate.shape[0]

    cost_of_pi_pulses = 0
    pi_pulses_routing = []

    source = gate.lev_a
    target = gate.lev_b

    path = nx.shortest_path( source, target )

    i = len(path)-2

    while(i > 0):

        if(path[i] >= 0):
            pi_gate = R(np.pi, 0, path[i] , path[i+1], dimension)
            pi_pulses_routing.append( pi_gate )
            cost_of_pi_pulses += rotation_cost_calc( pi_gate, placement )

            placement = placement.swap_nodes(path[i+1], path[i])

        elif(path[i] < 0):
            next_swap = find_next_available(i, path)

            if( next_swap > 0 ):
                routine_cost, sequence, placement = pi_swap_routine(i, next_swap, placement, dimension)
                pi_pulses_routing += sequence
                cost_of_pi_pulses += routine_cost

            else:
                pi_pulses_routing += []
                cost_of_pi_pulses += np.inf



    return ( cost_of_pi_pulses, pi_pulses_routing, placement )

