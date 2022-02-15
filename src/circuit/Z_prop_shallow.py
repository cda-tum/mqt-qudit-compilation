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


# ----------------------------------------------------------------

def propagate_z(QC, line_num, back):
    line = QC.qreg[line_num]

    tags = tag_generator(line)

    list_of_Zrots = []
    list_of_XYrots = []
    fixed_sequence = []

    for gate_index in range(len(line)):
        try:
            test_for_type_by_EAFP = line[gate_index].lev_b
            # object is R
            list_of_XYrots.append((line[gate_index], tags[gate_index]))
        except AttributeError:
            try:
                test_for_type_by_EAFP_2 = line[gate_index].lev
                # object is Rz
                list_of_Zrots.append((line[gate_index], tags[gate_index]))
            except AttributeError:
                pass

    levels = {}

    for Rz_gate_i, Rz_gate_tag in list_of_Zrots:

        tag_r = Rz_gate_tag
        e_lev_key = Rz_gate_i.lev

        if tag_r in levels:
            if e_lev_key in levels[tag_r]:
                levels[tag_r][e_lev_key] = Pi_mod(levels[tag_r][e_lev_key] + Rz_gate_i.theta)
            else:
                levels[tag_r][e_lev_key] = Pi_mod(Rz_gate_i.theta)
        else:
            levels[tag_r] = {}
            levels[tag_r][e_lev_key] = Pi_mod(Rz_gate_i.theta)

    for R_gate_i, R_gate_tag in list_of_XYrots:

        delta_phi = 0

        # respects commutation rules
        if back:
            for z_tag in list(levels):
                # where propagation happens
                if z_tag > R_gate_tag:
                    if R_gate_i.lev_a in levels[z_tag]:
                        delta_phi = Pi_mod(delta_phi - levels[z_tag][R_gate_i.lev_a])
                    if R_gate_i.lev_b in levels[z_tag]:
                        delta_phi = Pi_mod(delta_phi + levels[z_tag][R_gate_i.lev_b])
        else:
            for z_tag in reversed(list(levels)):
                # where propagation happens
                if z_tag <= R_gate_tag:
                    if R_gate_i.lev_a in levels[z_tag]:
                        delta_phi = Pi_mod(delta_phi + levels[z_tag][R_gate_i.lev_a])
                    if R_gate_i.lev_b in levels[z_tag]:
                        delta_phi = Pi_mod(delta_phi - levels[z_tag][R_gate_i.lev_b])

        old_phi = R_gate_i.phi
        new_phi = Pi_mod(old_phi + delta_phi)

        fixed_sequence.append(R(R_gate_i.theta, new_phi, R_gate_i.lev_a, R_gate_i.lev_b, R_gate_i.dimension))

    aggregated_Z = {}

    for z_tag in list(levels):
        for level in list(levels[z_tag]):
            if level in list(aggregated_Z):
                aggregated_Z[level] = Pi_mod(aggregated_Z[level] + levels[z_tag][level])
            else:
                aggregated_Z[level] = Pi_mod(levels[z_tag][level])

    Zseq = []
    for e_lev in list(aggregated_Z):
        Zseq.append(Rz(aggregated_Z[e_lev], e_lev, QC.dimension))

    return fixed_sequence, Zseq


def remove_Z(QC, back=True):
    for num_line in range(len(QC.qreg)):
        fixed_seq, z_tail = propagate_z(QC, num_line, back)
        if back:
            QC.qreg[num_line] = z_tail + fixed_seq
        else:
            QC.qreg[num_line] = fixed_seq + z_tail

    return
