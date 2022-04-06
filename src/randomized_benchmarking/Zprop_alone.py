from circuit.Rotations import R, Rz
from utils.r_utils import Pi_mod


def alone_propagate_z(dimension, line, back):
    Z_angles = {}
    list_of_Zrots = []
    list_of_XYrots = []


    for i in range(dimension):
        Z_angles[i] = 0.0

    if(back):
        line.reverse()

    for gate_index in range(len(line)):
        try:
            test_for_type_by_EAFP = line[gate_index].lev_b
            # object is R
            if(back):
                new_phi = Pi_mod(line[gate_index].phi + Z_angles[ line[gate_index].lev_a  ] - Z_angles[ line[gate_index].lev_b  ] )
            else:
                new_phi = Pi_mod( line[gate_index].phi - Z_angles[ line[gate_index].lev_a  ] + Z_angles[ line[gate_index].lev_b  ] )

            list_of_XYrots.append( R(line[gate_index].theta, new_phi, line[gate_index].lev_a, line[gate_index].lev_b, line[gate_index].dimension  ))
        except AttributeError:
            try:
                test_for_type_by_EAFP_2 = line[gate_index].lev
                # object is Rz
                Z_angles[line[gate_index].lev] = Pi_mod( Z_angles[line[gate_index].lev] + line[gate_index].theta )
            except AttributeError:
                pass
    if(back):
        list_of_XYrots.reverse()

    Zseq = []
    for e_lev in list(Z_angles):
        Zseq.append(Rz(Z_angles[e_lev], e_lev, dimension))


    return list_of_XYrots, Zseq
