#############################################################
#            Z GATES PROPAGATION
#############################################################
from utils.r_utils import Pi_mod
from .Rotations import R, Rz


def tag_generator(gates):
    tag_number = 0
    tags = []
    is_reset = False

    for g in gates:
        # BASED ON EAFP
        try:
            test_for_type_by_EAFP = g.lev_b
            is_reset = True

        except AttributeError:
            if (is_reset):
                tag_number += 1
                is_reset = False

        tags.append(tag_number)

    return tags



def propagate_z(QC, line_num, back):
    Z_angles = {}
    list_of_Zrots = []
    list_of_XYrots = []
    line = QC.qreg[line_num]

    for i in range(QC.dimension):
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
        Zseq.append(Rz(Z_angles[e_lev], e_lev, QC.dimension))


    return list_of_XYrots, Zseq



def remove_Z(QC, back=True):
    for num_line in range(len(QC.qreg)):
        fixed_seq, z_tail = propagate_z(QC, num_line, back)
        if back:
            QC.qreg[num_line] = z_tail + fixed_seq
        else:
            QC.qreg[num_line] = fixed_seq + z_tail

    return
