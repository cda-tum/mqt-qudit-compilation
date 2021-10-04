import numpy as np

#########################################


def cost_calculator(gate, placement, non_zeros):
    source = gate.lev_a
    target = gate.lev_b

    #TODO ADD CALCULATION OF INEFFICIENCY OF S +1/2
    #TODO COEFF = 2 ^...

    dist = placement.distance_nodes( source, target )

    return (number_pi_pulses, gate.cost * dist * non_zeros )

##########################################

def theta_corrector(angle):

    theta_in_units_of_pi = np.mod( (angle / np.pi), 2)
    if(theta_in_units_of_pi < 0.2):
        theta_in_units_of_pi +=  2.0

    return (theta_in_units_of_pi * np.pi)

