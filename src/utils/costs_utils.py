from src.circuit.swap_routines_basic import route_states2rotate_basic
from utils.cost_functions import rotation_cost_calc


def cost_calculator(gate, placement, non_zeros):
    cost_of_pi_pulses, pi_pulses_routing, new_placement = route_states2rotate_basic(gate, placement)

    gate_cost = rotation_cost_calc(gate, new_placement)

    total_costing = (gate_cost + cost_of_pi_pulses) * non_zeros

    return total_costing, pi_pulses_routing, new_placement, cost_of_pi_pulses, gate_cost

##########################################
