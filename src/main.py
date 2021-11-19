from binq.src.evaluation.Clifford_Generator import Clifford_Generator
from binq.src.evaluation.Verifier import Verifier
from binq.src.decomposition.Adaptive_decomposition import *
from binq.src.decomposition.QR_decomp import *
from binq.src.evaluation.Evaluation_Graphs import *
import time
import glob
import gc


from csv import DictWriter


################################################
# CREATING DATASET OF MATRICES
"""
C3 = Clifford_Generator(3,9) #log2(500)=9
C3.generate()
print("ok3")
C5 = Clifford_Generator(5,12)#log2(4000) =circa 12
C5.generate()
print("ok5")
C7 = Clifford_Generator(7,13)# 2^14= 16384
C7.generate()
print("ok7")
"""

dimension = 7
graph_combo = "g7_3"
graph_to_use = graph_7_3
nodes_to_use = nodes_7_3
nmap_to_use = nmap7_3
################################################

files_to_read = glob.glob("/home/k3vn/Documents/Compiler/binq/data/"+"dim"+str(dimension)+"/*.csv")

for file in files_to_read:

    IDbin = [int(i) for i in file.split() if i.isdigit() and (i=='0' or i=='1')]
    IDbin = " ".join(str(x) for x in IDbin)

    print("####################################")
    print(IDbin)
    #if(IDbin == "0 0 0 0 1 0 1 1 0 1 0"):
    #    lol = 5
    print("####################################")

    C_loader = Clifford_Generator(dimension)
    matrix_to_analyze = C_loader.load_from_csv(file)

    operation = custom_Unitary( matrix_to_analyze  , dimension)
    #############################################################

    #                        EXECUTION

    #############################################################
    QR = QR_decomp( operation, graph_to_use)

    startqr = time.time()
    decomp, algorithmic_cost, total_cost = QR.execute()
    endqr = time.time()
    print(len(decomp))
    ###############################################################

    Adaptive = Adaptive_decomposition(operation, graph_to_use, (algorithmic_cost, 5*total_cost ), dimension)

    start = time.time()
    matrices_decomposed, best_cost, final_graph = Adaptive.execute()
    end = time.time()
    print(len(matrices_decomposed))
    ###################################################################

    print("QR elapsed time")
    QR_time = endqr - startqr
    print(QR_time)


    print("Adaptive elapsed time")
    Adaptive_time = end - start
    print(Adaptive_time)

    ###############################################################################################
    print("COST QR,   ", (algorithmic_cost, total_cost ))
    print("BEST COST ADA,   ", best_cost)

    ###############################################################################################
    numRzQR = sum(isinstance(x, Rz) for x in decomp )
    numRzADA = sum(isinstance(x, Rz) for x in matrices_decomposed )
    print(numRzQR)
    print(numRzADA)
    ################################################################################################

    final_map = final_graph.lpmap

    V1 = Verifier(decomp, operation,  nodes_to_use, nmap_to_use, nmap_to_use, dimension)
    V2 = Verifier(matrices_decomposed, operation, nodes_to_use, nmap_to_use, final_map, dimension)
    V1r = V1.verify()
    V2r = V2.verify()

    print(V1r)
    print(V2r)


    field_names = ['ID','graphcombo', 'timeQR', 'timeADA', 'algoCostQR', 'algoCostADA', 'decoCostQR', 'decoCostADA', 'numRzQR', 'numRzADA', 'succQR', 'succADA' ]

    # Dictionary
    ada_algo = best_cost[0]
    ada_cost = best_cost[1]
    record = {'ID': IDbin,'graphcombo': graph_combo, 'timeQR':QR_time, 'timeADA':Adaptive_time, 'algoCostQR':algorithmic_cost, 'algoCostADA':ada_algo, 'decoCostQR':total_cost, 'decoCostADA':ada_cost, 'numRzQR':numRzQR, 'numRzADA':numRzADA, 'succQR':V1r, 'succADA':V2r }


    with open('/binq/data/evaluation/dim7/evalg73.csv', 'a') as f_object:
        
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
    
        # Pass the dictionary as an argument to the Writerow()
        dictwriter_object.writerow(record)
    
        # Close the file object
        f_object.close()

    gc.collect()
#########################################################################################
