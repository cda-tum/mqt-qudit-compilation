import gc

from circuit.Z_prop_shallow import remove_Z
from decomposition.QR_decomp import QR_decomp
from src.decomposition.Adaptive_decomposition import *
from src.architecture_graph.level_Graph import *
from src.circuit.Rotations import Rz, R, Custom_Unitary

class QuantumCircuit:
    
    def __init__(self, qudits, bits, dimension, graph):
        
        self.qudits = list(range(qudits))
        self.bits = list(range(bits))
        self.qreg = [[] for x in range(qudits)]
        self.reg = [[] for x in range(bits)] 
        self.dimension = dimension
        self.energy_level_graph = graph
        
    def R(self, qudit_line, theta, phi, lev_a, lev_b ):
        
        self.qreg[qudit_line].append( R(theta, phi, lev_a, lev_b , self.dimension))

    def Rz(self, qudit_line, theta, lev):
        
        self.qreg[qudit_line].append( Rz(theta, lev, self.dimension) )
        
    def custom_unitary(self, qudit_line, unitary):

        self.qreg[qudit_line].append(Custom_Unitary(unitary, self.dimension))


    def draw(self):
        custom_counter = 0

        for line in self.qreg:
            print("!0>---", end ="")
            for gate in line:
                if (isinstance(gate, Rz)):
                    print("--[Rz(" + str(round(gate.theta,2))+")]--", end ="")

                elif (isinstance(gate, R)):
                    print("--[R(" + str(round(gate.theta,2)) + "," + str(round(gate.phi,2))+")]--", end ="")

                elif(isinstance(gate, Custom_Unitary)):
                    print("--[C" + str(custom_counter)+ "]--", end ="")
                    custom_counter = custom_counter+1

            print()



    ####################################################################
    #
    #               DECOMPOSITION
    #
    ####################################################################

    def Z_prop(self):
        remove_Z(self)

    def DFS_decompose(self):

        new_qreg = []

        for line in self.qreg:
            
            clean_line = []
            
            for gate in line:

                QR = QR_decomp(gate, self.energy_level_graph)

                decomp, algorithmic_cost, total_cost = QR.execute()

                Adaptive = Adaptive_decomposition(gate, self.energy_level_graph, (algorithmic_cost, total_cost), self.dimension)

                matrices_decomposed, best_cost, final_graph = Adaptive.execute()

                clean_line = clean_line + matrices_decomposed
                gc.collect()

            new_qreg.append(clean_line)

            self.qreg = new_qreg

        return

    def QR_decompose(self):

        new_qreg = []

        for line in self.qreg:

            clean_line = []

            for gate in line:
                QR = QR_decomp(gate, self.energy_level_graph)

                decomp, algorithmic_cost, total_cost = QR.execute()

                clean_line = clean_line + decomp
                gc.collect()

            new_qreg.append(clean_line)

            self.qreg = new_qreg

        return