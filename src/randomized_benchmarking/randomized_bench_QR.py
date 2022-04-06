import gc
import time

from evaluation.Pauli import H
from src.decomposition.QR_decomp import *
from src.evaluation.Evaluation_Graphs import *
from src.evaluation.Verifier import Verifier
from Zprop_alone import alone_propagate_z



def RB_QR(dimension, path, edges_MAP, graph_combo_in, graph_to_use_in, nodes_to_use_in, back):

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
    return return_list


edges_3_1 = [(1, 2, {"delta_m": 0, "sensitivity": 3}),
             (0, 2, {"delta_m": 0, "sensitivity": 3}),
             ]
nodes_3_1 = [0, 1, 2]
nmap3_1 = [2, 0, 1]

graph_3_1 = level_Graph(edges_3_1, nodes_3_1, nmap3_1, [0])

edges_MAP = None
dimension = 3
back = True


RB_QR(dimension, "/home/k3vn/Downloads/unitaries_dim_3.npy", None, "", graph_3_1, nodes_3_1, True)