import numpy as np

#########################################
SP_PENALTY = 2 #TODO REFINE MEASUREMENT OF PENALTY FOR SP LEVELS


def analysis_of_rotation():
    #TODO trigger the right type of rotation and give feedback of number of pi pulses required


def cost_calculator(gate, placement, non_zeros):
    source = gate.lev_a
    target = gate.lev_b
    gate_cost = gate.cost

    if(placement.is_Sp(source) or placement.is_Sp(target) ):
        theta_on_units = gate.theta / np.pi
        gate_cost = gate_cost + ( SP_PENALTY*abs(np.mod(theta_on_units+0.25, 0.5) - 0.25) )*10.0e-04

    #TODO ADD CALCULATION OF INEFFICIENCY OF S +1/2
    #TODO COEFF = 2 ^...

    dist = placement.distance_nodes( source, target )

    return ( number_pi_pulses, gate_cost * dist * non_zeros )

##########################################

def theta_corrector(angle):

    theta_in_units_of_pi = np.mod( (angle / np.pi), 2)
    if(theta_in_units_of_pi < 0.2):
        theta_in_units_of_pi +=  2.0

    return (theta_in_units_of_pi * np.pi)

