import numpy as np


def theta_corrector(angle):
    theta_in_units_of_pi = np.mod(abs(angle / np.pi), 4)
    if angle < 0:
        theta_in_units_of_pi = theta_in_units_of_pi * -1
    if abs(theta_in_units_of_pi) < 0.2:
        theta_in_units_of_pi += 4.0

    return theta_in_units_of_pi * np.pi


def phi_cost(theta):
    theta_on_units = theta / np.pi

    Err = abs(theta_on_units) * 1e-04
    return Err


def theta_cost(theta):
    theta_on_units = theta / np.pi

    Err = (4 * abs(theta_on_units) + abs(np.mod(abs(theta_on_units) + 0.25, 0.5) - 0.25)) * 1e-04
    return Err


def rotation_cost_calc(gate, placement):
    source = gate.original_lev_a
    target = gate.original_lev_b

    gate_cost = gate.cost

    if placement.is_irnode(source) or placement.is_irnode(target):
        SP_PENALTY = min(placement.distance_nodes(placement._1stInode, source),
                         placement.distance_nodes(placement._1stInode, target)) + 1

        gate_cost = SP_PENALTY * theta_cost(gate.theta)

    return gate_cost
