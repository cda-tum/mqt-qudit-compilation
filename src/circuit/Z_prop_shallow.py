#############################################################

####            Z GATES PROPAGATION

####################################################################
####################################################################
####################################################################

from circuit.Rotations import Rz, R
from utils.r_utils import newMod


def tag_generator(gates):
    tag_number = 0
    tags = []
    is_reset = False

    for g in gates:
        if (isinstance(g, Rz) and is_reset):
            tag_number += 1
            is_reset = False
        else:
            is_reset = True

        tags.append(tag_number)

    return tags

######################################
#####################################

def propagate_Z_backward(QC, line_num):
    line = QC.qreg[line_num]

    tags = tag_generator(line)

    list_of_Zrots = []
    list_of_XYrots = []
    fixed_sequence = []

    for gate_index in range(len(line)):

        if (isinstance(line[gate_index], Rz)):

            list_of_Zrots.append((line[gate_index], tags[gate_index]))

        elif (isinstance(line[gate_index], R)):

            list_of_XYrots.append((line[gate_index], tags[gate_index]))

    levels = {}

    for Rz_gate_i, Rz_gate_tag  in list_of_Zrots:

        key1 = Rz_gate_i.lev
        key2 = Rz_gate_tag

        if key1 in levels:
            if key2 in levels[key1]:

                for tag in levels[key1]:
                    if (tag < key2):
                        levels[key1][tag] = newMod( levels[key1][tag] + Rz_gate_i.theta )

                        levels[key1][key2] += Rz_gate_i.theta
            else:
                for tag in levels[key1]:
                    if (tag < key2):
                        levels[key1][tag] = newMod( levels[key1][tag] + Rz_gate_i.theta )

                        levels[key1][key2] = Rz_gate_i.theta

        else:
            levels[key1] = {}
            levels[key1][key2] = Rz_gate_i.theta

    for gate_tuple in list_of_XYrots:
        R_gate_i = gate_tuple[0]
        R_gate_tag = gate_tuple[1]

        phi = 0

        if (R_gate_i.lev_a in levels):
            for z_tags in levels[R_gate_i.lev_a]:
                if (z_tags > R_gate_tag):
                    phi += levels[R_gate_i.lev_a][z_tags]

        if (R_gate_i.lev_b in levels):
            for z_tags in levels[R_gate_i.lev_b]:
                if (z_tags > R_gate_tag):
                    phi -= levels[R_gate_i.lev_b][z_tags]

        old_phi = R_gate_i.phi

        new_phi = newMod( old_phi + phi )

        fixed_sequence.append( R(R_gate_i.theta, new_phi, R_gate_i.lev_a, R_gate_i.lev_b, R_gate_i.dimension) )

    fixed_sequence

    return fixed_sequence


# ----------------------------------------------------------------------------

def propagate_Z_forward(QC, line_num):
    line = QC.qreg[line_num]

    tags = tag_generator(line)

    list_of_Zrots = []
    list_of_XYrots = []
    fixed_sequence = []

    for gate_index in range(len(line)):

        if (isinstance(line[gate_index], Rz)):

            list_of_Zrots.append((line[gate_index], tags[gate_index]))

        elif (isinstance(line[gate_index], R)):

            list_of_XYrots.append((line[gate_index], tags[gate_index]))

    levels = {}

    for Rz_gate_i, Rz_gate_tag in reversed(list_of_Zrots):

        key1 = Rz_gate_i.lev
        key2 = Rz_gate_tag

        if key1 in levels:
            if key2 in levels[key1]:

                for tag in levels[key1]:
                    if (tag > key2):
                        levels[key1][tag] = newMod( levels[key1][tag] + Rz_gate_i.theta )

                        levels[key1][key2] += Rz_gate_i.theta
            else:
                for tag in levels[key1]:
                    if (tag > key2):
                        levels[key1][tag] = newMod( levels[key1][tag] + Rz_gate_i.theta )

                        levels[key1][key2] = Rz_gate_i.theta

        else:
            levels[key1] = {}
            levels[key1][key2] = Rz_gate_i.theta

    for R_gate_i, R_gate_tag in reversed(list_of_XYrots):

        phi = 0

        if (R_gate_i.lev_a in levels):
            for z_tags in levels[R_gate_i.lev_a]:
                if (z_tags < R_gate_tag):
                    phi += levels[R_gate_i.lev_a][z_tags]

        if (R_gate_i.lev_b in levels):
            for z_tags in levels[R_gate_i.lev_b]:
                if (z_tags < R_gate_tag):
                    phi -= levels[R_gate_i.lev_b][z_tags]

        old_phi = R_gate_i.phi

        new_phi = newMod( old_phi + phi )

        fixed_sequence.append( R(R_gate_i.theta, new_phi, R_gate_i.lev_a, R_gate_i.lev_b, R_gate_i.dimension) )

    

    return fixed_sequence

# ----------------------------------------------------------------------------

def remove_Z(QC, back=True):

    if(back):
        for num_line in range(len(QC.qreg)):
            QC.qreg[num_line] = propagate_Z_backward(QC, num_line)
    else:
        for num_line in range(len(QC.qreg)):
            QC.qreg[num_line] = propagate_Z_forward(QC, num_line)

    return


