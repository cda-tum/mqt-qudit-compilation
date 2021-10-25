import numpy as np

#########################################
from binq.src.QC.swap_routines import *


def rotation_cost_calc(gate, placement):
    SP_PENALTY = 2  # TODO REFINE MEASUREMENT OF PENALTY FOR SP LEVELS

    source = gate.lev_a
    target = gate.lev_b
    gate_cost = gate.cost

    if(placement.is_Sp(source) or placement.is_Sp(target)):
        theta_on_units = gate.theta / np.pi
        gate_cost = gate_cost + ( SP_PENALTY*abs(np.mod(theta_on_units+0.25, 0.5) - 0.25) )*10.0e-04

    return gate_cost

def cost_calculator(gate, placement, non_zeros):


    cost_of_pi_pulses, pi_pulses_routing, new_placement = route_states2rotate(gate, placement)

    gate_cost = rotation_cost_calc(gate, placement)

    return ( (gate_cost + cost_of_pi_pulses) * non_zeros , pi_pulses_routing, new_placement )

##########################################

def theta_corrector(angle):

    theta_in_units_of_pi = np.mod( (angle / np.pi), 2)
    if(theta_in_units_of_pi < 0.2):
        theta_in_units_of_pi +=  2.0

    return (theta_in_units_of_pi * np.pi)

