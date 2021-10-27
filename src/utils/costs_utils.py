
#########################################
from binq.src.QC.swap_routines import *
from binq.src.utils.r_utils import rotation_cost_calc


def cost_calculator(gate, placement, non_zeros):


    cost_of_pi_pulses, pi_pulses_routing, new_placement = route_states2rotate(gate, placement)

    gate_cost = rotation_cost_calc(gate, placement)

    return ( (gate_cost + cost_of_pi_pulses) * non_zeros , pi_pulses_routing, new_placement )

##########################################


