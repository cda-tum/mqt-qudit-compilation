import gc
import time

from evaluation.Pauli import H
from src.decomposition.QR_decomp import *
from src.evaluation.Evaluation_Graphs import *
from src.evaluation.Verifier import Verifier
from Zprop_alone import alone_propagate_z


def RB_QR(dimension, path, edges_MAP, graph_combo_in, graph_to_use_in, nodes_to_use_in, back):
    GLOBAL_SEQUENCE_QR = []
    GLOBAL_SEQUENCE_QR_WITH_INVERSION = []
    rev_decomp = []

    GLOBAL_FUNCTION = np.identity(dimension, dtype=complex)

    graph_to_use = graph_to_use_in  # todo
    nodes_to_use = nodes_to_use_in  # todo

    ################################################

    GROUP = np.load(path, allow_pickle=True)

    for indx, matrix_to_analyze in enumerate(GROUP):

        GLOBAL_FUNCTION = matmul(GLOBAL_FUNCTION, matrix_to_analyze)

        operation = Custom_Unitary(matrix_to_analyze, dimension)
        #############################################################

        #                        EXECUTION

        #############################################################

        QR = QR_decomp(operation, graph_to_use, not_stand_alone=False)

        startqr = time.time()
        decomp, algorithmic_cost, total_cost = QR.execute()
        endqr = time.time()

        print("QR elapsed time")
        QR_time = endqr - startqr
        print(QR_time, "\n")

        print("COST QR,   ", (algorithmic_cost, total_cost))

        ###############################################################################################

        #      VERIFICATION         #

        ################################################################################################

        V1 = Verifier(decomp, operation, nodes_to_use, graph_to_use_in.lpmap, graph_to_use_in.lpmap, dimension)

        V1r = V1.verify()

        print(V1r)

        if (V1r == False):
            raise Exception

        GLOBAL_SEQUENCE_QR = GLOBAL_SEQUENCE_QR + decomp



        for gate in reversed(decomp):
            try:
                test_for_type_by_EAFP = gate.lev_b
                # object is R
                rev_decomp.append( R( gate.theta, -gate.phi, gate.lev_a, gate.lev_b, dimension ) )
            except AttributeError:
                try:
                    test_for_type_by_EAFP_2 = gate.lev
                    rev_decomp.append( Rz( -gate.theta, gate.lev, dimension ) )

                except AttributeError:
                    pass

        GLOBAL_SEQUENCE_QR_WITH_INVERSION = rev_decomp + GLOBAL_SEQUENCE_QR_WITH_INVERSION
        gc.collect()

    ###############################################################################################

    #      Z PROP         #

    qr_decomp, z_tail = alone_propagate_z(dimension, GLOBAL_SEQUENCE_QR, back)

    if back:
        fin_qr = z_tail + qr_decomp

    else:
        fin_qr = qr_decomp + z_tail

    GLOBAL_FUNCTION = Custom_Unitary(GLOBAL_FUNCTION, dimension)
    V1 = Verifier(fin_qr, GLOBAL_FUNCTION, nodes_to_use, graph_to_use.lpmap, graph_to_use.lpmap, dimension)

    V1rz = V1.verify()

    if (V1rz == False):
        raise Exception

    ##################################################################

    qr_decomp_rev, z_tail_rev = alone_propagate_z(dimension, GLOBAL_SEQUENCE_QR_WITH_INVERSION, back)

    if back:
        fin_qr_rev = z_tail_rev + qr_decomp_rev

    else:
        fin_qr_rev = qr_decomp_rev + z_tail_rev

    target = np.identity(dimension, dtype=complex)

    for rotation in fin_qr_rev:
        target = matmul(rotation.matrix , target )
        deb = target.round(2)

    gf = GLOBAL_FUNCTION.matrix.round(2)
    res = ( abs( target - GLOBAL_FUNCTION.matrix ) < 10e-5 ).all()

    ##################################################################

    return_list = []
    for gate in fin_qr:
        try:
            test_for_type_by_EAFP = gate.lev_b
            # object is R
            return_list.append(['R', gate.theta, gate.phi, (gate.lev_a, gate.lev_b)])
        except AttributeError:
            try:
                test_for_type_by_EAFP_2 = gate.lev
                return_list.append(['RZ', gate.theta, (-1, gate.lev)])

            except AttributeError:
                pass


    return return_list


