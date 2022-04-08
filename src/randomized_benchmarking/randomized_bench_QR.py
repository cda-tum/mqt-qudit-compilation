import gc
import time

from evaluation.Pauli import H
from src.decomposition.QR_decomp import *
from src.evaluation.Evaluation_Graphs import *
from src.evaluation.Verifier import Verifier
from src.randomized_benchmarking.Zprop_alone import alone_propagate_z

DIAGNOSE = False


def RB_QR(dimension, path, graph_to_use_in, nodes_to_use_in, back):
    GLOBAL_SEQUENCE_QR_dag = []
    GLOBAL_SEQUENCE_QR = []

    GLOBAL_FUNCTION = np.identity(dimension, dtype=complex)



    graph_to_use = graph_to_use_in  # todo
    nodes_to_use = nodes_to_use_in  # todo

    ################################################

    GROUP = np.load(path, allow_pickle=True)

    for indx, matrix_to_analyze in enumerate(GROUP):

        GLOBAL_FUNCTION = matmul( GLOBAL_FUNCTION, matrix_to_analyze )

        operation = Custom_Unitary(matrix_to_analyze, dimension)
        #############################################################

        #                        EXECUTION

        #############################################################

        QR = QR_decomp(operation, graph_to_use, not_stand_alone=False)

        startqr = time.time()
        decomp, algorithmic_cost, total_cost = QR.execute()
        endqr = time.time()

        #print("QR elapsed time")
        QR_time = endqr - startqr
        #print(QR_time, "\n")

        #print("COST QR,   ", (algorithmic_cost, total_cost))

        ###############################################################################################

        #      VERIFICATION         #

        ################################################################################################

        V1 = Verifier(decomp, operation, nodes_to_use, graph_to_use_in.lpmap, graph_to_use_in.lpmap, dimension)

        V1r = V1.verify()

        #print(V1r)

        if (V1r == False):
            raise Exception

        rev_decomp = []
        for gate in reversed(decomp):
            try:
                test_for_type_by_EAFP = gate.lev_b
                # object is R
                rev_decomp.append(['R', gate.theta, gate.phi+np.pi, (gate.lev_a, gate.lev_b)])
            except AttributeError:
                try:
                    test_for_type_by_EAFP_2 = gate.lev
                    rev_decomp.append(['RZ', gate.theta, (-1, gate.lev)])

                except AttributeError:
                    pass


        GLOBAL_SEQUENCE_QR_dag = GLOBAL_SEQUENCE_QR_dag + rev_decomp
        GLOBAL_SEQUENCE_QR = GLOBAL_SEQUENCE_QR + decomp
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

    if DIAGNOSE:
        u = np.identity(3)
        print("--- BINQ COMPILATION FINISHED ---\n ----->> PRINT UNITARIES!\n")
        for i, g in enumerate(fin_qr[::-1]):
            flt = g.matrix.flatten()
            re = np.asarray([np.around(np.real(f), 2) for f in flt])
            im = np.asarray([np.around(np.imag(f), 2) for f in flt])
            mat = np.reshape(re + 1j * im, (3, 3))
            print(f"U{i}:\n{mat}")
            u = np.dot(g.matrix, u)
        print("-----> FINAL: ")
        flt = u.flatten()
        re = np.asarray([np.around(np.real(f), 2) for f in flt])
        im = np.asarray([np.around(np.imag(f), 2) for f in flt])
        mat = np.reshape(re + 1j * im, (3, 3))
        print(mat)

    #return return_list
    return GLOBAL_SEQUENCE_QR_dag

# edges_3_1 = [(1, 2, {"delta_m": 0, "sensitivity": 3}),
#              (0, 2, {"delta_m": 0, "sensitivity": 3}),
#              ]
# nodes_3_1 = [0, 1, 2]
# nmap3_1 = [2, 0, 1]
#
graph_3_1 = level_Graph(edges_3_1, nodes_3_1, nmap3_1, [0])
#
# edges_MAP = None
# dimension = 3
# back = True
#
#
# RB_QR(dimension, "/home/k3vn/Downloads/unitaries_dim_3.npy", graph_3_1, nodes_3_1, True)