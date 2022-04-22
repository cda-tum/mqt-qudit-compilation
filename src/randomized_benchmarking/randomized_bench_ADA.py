import gc
import time

from src.evaluation.Pauli import H
from src.decomposition.Adaptive_decomposition import *
from src.decomposition.QR_decomp import *
from src.evaluation.Evaluation_Graphs import *
from src.evaluation.Verifier import Verifier
from src.randomized_benchmarking.Zprop_alone import alone_propagate_z




def RB_ADA(dimension, path, edges_MAP, graph_combo_in, graph_to_use_in, nodes_to_use_in, back):


    GLOBAL_SEQUENCE_ADA = []

    GLOBAL_FUNCTION = np.identity(dimension, dtype=complex)

    GLOBAL_INI_MAP = graph_to_use_in.lpmap

    graph_to_use = graph_to_use_in
    nodes_to_use = nodes_to_use_in

    ################################################

    GROUP = np.load(path, allow_pickle=True)

    for indx, matrix_to_analyze in enumerate(GROUP):

        GLOBAL_FUNCTION = matmul(GLOBAL_FUNCTION, matrix_to_analyze)

        operation = Custom_Unitary(matrix_to_analyze, dimension)
        #############################################################

        #                        EXECUTION

        #############################################################

        QR = QR_decomp(operation, graph_to_use)

        decomp, algorithmic_cost, total_cost = QR.execute()




        Adaptive = Adaptive_decomposition(operation, graph_to_use, (1.1 * algorithmic_cost, 1.1 * total_cost),
                                          dimension)

        ini_map = list(graph_to_use.lpmap)

        start = time.time()
        matrices_decomposed, best_cost, final_graph = Adaptive.execute()
        end = time.time()

        final_map = list(final_graph.lpmap)


        print("Adaptive elapsed time")
        Adaptive_time = end - start
        print(Adaptive_time, "\n")

        print("COST QR,   ", (algorithmic_cost, total_cost))
        print("BEST COST ADA,   ", best_cost, "\n")

        ###############################################################################################

        #      VERIFICATION         #

        ################################################################################################

        V1 = Verifier(decomp, operation, nodes_to_use, ini_map, ini_map, dimension)

        V2 = Verifier(matrices_decomposed, operation, nodes_to_use, ini_map, final_map, dimension)

        V1r = V1.verify()
        V2r = V2.verify()

        print(V1r)
        print(V2r)

        if (V1r == False or V2r == False):
            raise Exception


        GLOBAL_SEQUENCE_ADA = GLOBAL_SEQUENCE_ADA + matrices_decomposed


        ###################################################################
        #                   UPDATE GRAPH
        graph_to_use = final_graph
        ###################################################################


        gc.collect()

    #######################
    #      Z PROP         #
    #######################

    new_ada, tail = alone_propagate_z(dimension, GLOBAL_SEQUENCE_ADA, back)

    if back:
        fin_ada = tail + new_ada

    else:
        fin_ada = new_ada + tail

    GLOBAL_FUNCTION = Custom_Unitary(GLOBAL_FUNCTION, dimension)

    V2z = Verifier(fin_ada, GLOBAL_FUNCTION, nodes_to_use, GLOBAL_INI_MAP, graph_to_use.lpmap, dimension)

    V2rz = V2z.verify()

    if (V2rz == False):
        raise Exception

    return_list = []
    for gate in fin_ada:
        try:
            test_for_type_by_EAFP = gate.lev_b
            # object is R
            return_list.append(['R',gate.theta, gate.phi, (gate.lev_a, gate.lev_b) ])
        except AttributeError:
            try:
                test_for_type_by_EAFP_2 = gate.lev
                return_list.append(['RZ', gate.theta,  (-1, gate.lev)])

            except AttributeError:
                pass


    return return_list





