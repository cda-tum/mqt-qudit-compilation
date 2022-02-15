# TODO TO INTEGRATE WITH QUANTUM CIRCUIT CLASS
# TODO TO FIX AND INTEGRATE

import networkx as nx
import numpy as np

from src.Exceptions.Exceptions import RoutingException
from src.circuit.Rotations import R
from utils.cost_functions import rotation_cost_calc


def swap_assignment(a, b):
    return b, a


def swap_elements(l, i, j):
    a = l[i]
    b = l[j]
    l[i] = b
    l[j] = a
    return l


def pi_swap_routine(path, i, next, placement, dimension):
    swapping_list = []
    cost = 0

    trace = list(range(next, i + 2))
    trace.reverse()
    index = 0

    while (index < len(trace) - 1):
        pi_gate = R(np.pi, 0, path[trace[index]], path[trace[index + 1]], dimension)
        swapping_list.append(pi_gate)
        cost += rotation_cost_calc(pi_gate, placement)

        placement = placement.swap_nodes(path[trace[index]], path[trace[index + 1]])

        path = swap_elements(path, trace[index], trace[index + 1])
        index += 1

    index -= 1
    while (index > 0):
        pi_gate = R(np.pi, 0, path[trace[index - 1]], path[trace[index]], dimension)
        swapping_list.append(pi_gate)
        cost += rotation_cost_calc(pi_gate, placement)

        placement = placement.swap_nodes(path[trace[index - 1]], path[trace[index]])
        path = swap_elements(path, trace[index - 1], trace[index])
        index -= 1

    return (cost, swapping_list, placement, path)


def find_next_available(i, lista):
    counter = i - 1
    while (counter >= 0):
        if (lista[counter] >= 0):
            return counter
        counter -= 1

    # return -1


def rotate_over_ancilla(path, source, target, placement, dimension):
    swapping_list = []
    cost = 0
    target = target + 1  # because target is signaling the first encountered negative node
    neighbours_source = [n for n in placement.neighbors(path[source]) if n >= 0]
    neighbours_target = [n for n in placement.neighbors(path[target]) if n >= 0]

    sensitivity_source = [placement.get_edge_sensitivity(path[source], node) for node in neighbours_source]
    sensitivity_target = [placement.get_edge_sensitivity(path[target], node) for node in neighbours_target]

    if (len(sensitivity_source) > 0):
        invert = False
        best_n_s_index = np.argmin(sensitivity_source)
        node_to_go_s = neighbours_source[best_n_s_index]

        pi_gate = R(np.pi, 0, path[source], node_to_go_s, dimension)
        swapping_list.append(pi_gate)
        cost += rotation_cost_calc(pi_gate, placement)

        placement = placement.swap_nodes(path[source], node_to_go_s)

    elif (len(sensitivity_target) > 0):
        invert = True
        best_n_t_index = np.argmin(sensitivity_target)
        node_to_go_t = neighbours_target[best_n_t_index]

        pi_gate = R(np.pi, 0, path[target], node_to_go_t, dimension)
        swapping_list.append(pi_gate)
        cost += rotation_cost_calc(pi_gate, placement)

        placement = placement.swap_nodes(path[target], node_to_go_t)
    else:
        raise RoutingException

    return (cost, swapping_list, placement, invert)


def route_states2rotate_ancilla_fixed(gate, orig_placement):
    placement = orig_placement

    dimension = gate.shape[0]

    cost_of_pi_pulses = 0
    pi_pulses_routing = []

    source = gate.lev_a
    target = gate.lev_b

    path = nx.shortest_path(placement, source, target)

    i = len(path) - 2

    while (i > 0):

        if (path[i] >= 0):
            pi_gate = R(np.pi, 0, path[i], path[i + 1], dimension)
            pi_pulses_routing.append(pi_gate)
            cost_of_pi_pulses += rotation_cost_calc(pi_gate, placement)

            placement = placement.swap_nodes(path[i + 1], path[i])
            path = swap_elements(path, i + 1, i)

            i -= 1
        elif (path[i] < 0):

            next_swap = find_next_available(i, path)

            if (next_swap == 0 and path[next_swap] == source):

                routine_cost, sequence, placement, invert_routing = rotate_over_ancilla(path, next_swap, i, placement,
                                                                                        dimension)
                pi_pulses_routing += sequence
                cost_of_pi_pulses += routine_cost

                if (invert_routing):
                    # switched
                    source, target = swap_assignment(source, target)
                path = nx.shortest_path(placement, source, target)
                i = len(path) - 2

            else:
                if (next_swap > 0):
                    routine_cost, sequence, placement, path = pi_swap_routine(path, i, next_swap, placement, dimension)
                    pi_pulses_routing += sequence
                    cost_of_pi_pulses += routine_cost

                else:
                    # worst case scenarion routing is not possible
                    pi_pulses_routing += []
                    cost_of_pi_pulses += np.inf

                i = next_swap - 1

    return (cost_of_pi_pulses, pi_pulses_routing, placement)
