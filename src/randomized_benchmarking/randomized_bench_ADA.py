import gc
import time

from src.decomposition.Adaptive_decomposition import *
from src.decomposition.QR_decomp import *
from src.evaluation.Evaluation_Graphs import *
from src.evaluation.Verifier import Verifier
from Zprop_alone import alone_propagate_z

# MAKE YOUR OWN GRAPH EXAMPLE


edges_3_4 = [(1, 0, {"delta_m": 0, "sensitivity": 3}),
             (0, 2, {"delta_m": 0, "sensitivity": 3}),
             ]
nodes_3_4 = [0, 1, 2]
nmap3_4 = [0, 1, 2]

graph_3_4 = level_Graph(edges_3_4, nodes_3_4, nmap3_4, [0])

edges_MAP = None

# CHOICE OF GRAPH FOR TESTING
dimension = 3

graph_combo = "graph_3_4"  # todo
graph_to_use = graph_3_4  # todo
nodes_to_use = nodes_3_4  # todo
nmap_to_use = nmap3_4  # todo

back = True

################################################

GROUP = np.load("/home/k3vn/Downloads/unitaries_dim_3.npy", allow_pickle=True)

for indx, matrix_to_analyze in enumerate(GROUP):

    operation = Custom_Unitary(matrix_to_analyze, dimension)

    #############################################################

    #                        EXECUTION

    #############################################################
    ini_lpmap = list(graph_to_use.lpmap)

    QR = QR_decomp(operation, graph_to_use)

    startqr = time.time()
    decomp, algorithmic_cost, total_cost = QR.execute()
    endqr = time.time()

    Adaptive = Adaptive_decomposition(operation, graph_to_use, (1.1 * algorithmic_cost, 1.1 * total_cost), dimension)

    start = time.time()
    matrices_decomposed, best_cost, final_graph = Adaptive.execute()
    end = time.time()

    final_map = list(final_graph.lpmap)

    ###################################################################
    #                   UPDATE GRAPH
    graph_to_use = final_graph
    ###################################################################

    print("QR elapsed time")
    QR_time = endqr - startqr
    print(QR_time, "\n")

    print("Adaptive elapsed time")
    Adaptive_time = end - start
    print(Adaptive_time, "\n")

    print("COST QR,   ", (algorithmic_cost, total_cost))
    print("BEST COST ADA,   ", best_cost, "\n")

    ###############################################################################################

    #      VERIFICATION         #

    ################################################################################################

    V1 = Verifier(decomp, operation, nodes_to_use, nmap_to_use, nmap_to_use, dimension)

    V2 = Verifier(matrices_decomposed, operation, nodes_to_use, ini_lpmap, final_map, dimension)

    V1r = V1.verify()
    V2r = V2.verify()

    print(V1r)
    print(V2r)

    if (V1r == False or V2r == False):
        raise Exception

    ###############################################################################################

    #      Z PROP         #

    qr_decomp, z_tail = alone_propagate_z(dimension, decomp, back)
    ADA_decomp, z_tailADA = alone_propagate_z(dimension, matrices_decomposed, back)

    if back:
        qr_decomp = z_tail + qr_decomp
        ADA_decomp = z_tailADA + ADA_decomp

    else:
        qr_decomp = qr_decomp + z_tail
        ADA_decomp = ADA_decomp + z_tailADA

    V1 = Verifier(qr_decomp, operation, nodes_to_use, nmap_to_use, nmap_to_use, dimension)

    V2 = Verifier(ADA_decomp, operation, nodes_to_use, ini_lpmap, final_map, dimension)

    V1rz = V1.verify()
    V2rz = V2.verify()

    if (V1rz == False or V2rz == False):
        raise Exception

    ################################################################################################

    ### save results
    field_names = ['ID', 'graphcombo', 'timeQR', 'timeADA', 'decoCostQR', 'decoCostADA', 'succQR', 'succADA', 'sucZQR',
                   'sucZADA'
                   ]

    # Dictionary
    ada_algo = best_cost[0]
    ada_cost = best_cost[1]
    record = {'ID': indx, 'graphcombo': graph_combo, 'timeQR': QR_time, 'timeADA': Adaptive_time,
              'decoCostQR': total_cost, 'decoCostADA': ada_cost, 'succQR': V1r, 'succADA': V2r, 'sucZQR': V1rz,
              'sucZADA': V2rz
              }

    repr_as_dict_QR = {}

    counter = 1

    for j, gate in enumerate(qr_decomp):
        if isinstance(gate, Rz):
            repr_as_dict_QR[str(counter)] = {"theta": gate.theta, "carrier": gate.lev, "particle": j, "type": 'z'}


        elif isinstance(gate, R):
            repr_as_dict_QR[str(counter)] = {"theta": gate.theta, "phi": gate.phi,
                                             "carrier": edges_MAP[str((gate.lev_a, gate.lev_b))], "particle": j,
                                             "type": 'g'}

        counter += 1

    repr_as_dict_ADA = {}

    counter = 1

    for j, gate in enumerate(ADA_decomp):
        if isinstance(gate, Rz):
            repr_as_dict_ADA[str(counter)] = {"theta": gate.theta, "carrier": gate.lev, "particle": j, "type": 'z'}


        elif isinstance(gate, R):
            repr_as_dict_ADA[str(counter)] = {"theta": gate.theta, "phi": gate.phi,
                                              "carrier": edges_MAP[str((gate.lev_a, gate.lev_b))], "particle": j,
                                              "type": 'g'}

        counter += 1

    gc.collect()
##############################
