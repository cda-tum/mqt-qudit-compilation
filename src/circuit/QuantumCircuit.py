import gc
import json

from circuit.Z_prop_shallow import remove_Z
from decomposition.QR_decomp import QR_decomp
from src.decomposition.Adaptive_decomposition import *
from .Rotations import Rz, R, Custom_Unitary


class QuantumCircuit:

    def __init__(self, qudits, bits, dimension, graph):

        self.qudits = list(range(qudits))
        self.bits = list(range(bits))
        self.qreg = [[] for _ in range(qudits)]
        self.reg = [[] for _ in range(bits)]
        self.dimension = dimension
        self.energy_level_graph = graph

    def R(self, qudit_line, theta, phi, lev_a, lev_b):

        self.qreg[qudit_line].append(R(theta, phi, lev_a, lev_b, self.dimension))

    def Rz(self, qudit_line, theta, lev):

        self.qreg[qudit_line].append(Rz(theta, lev, self.dimension))

    def custom_unitary(self, qudit_line, unitary):

        self.qreg[qudit_line].append(Custom_Unitary(unitary, self.dimension))

    def draw(self):
        custom_counter = 0

        for line in self.qreg:
            print("|0>---", end="")
            for gate in line:
                if isinstance(gate, Rz):
                    print("--[Rz" + str(gate.lev) + "(" + str(round(gate.theta, 2)) + ")]--", end="")

                elif isinstance(gate, R):
                    print("--[R" + str(gate.lev_a) + str(gate.lev_b) + "(" + str(round(gate.theta, 2)) + "," + str(
                        round(gate.phi, 2)) + ")]--", end="")

                elif isinstance(gate, Custom_Unitary):
                    print("--[C" + str(custom_counter) + "]--", end="")
                    custom_counter = custom_counter + 1

            print("---=||")

    def to_json(self, absolute_path, name="QCjsoned"):
        repr_as_dict = {}
        temp = []

        for i, e in enumerate(list(self.energy_level_graph.edges)):
            temp.append((str(e), i))
        temp = dict(temp)

        repr_as_dict['0'] = dict(temp)
        counter = 1

        for j, line in enumerate(self.qreg):
            for gate in line:
                if isinstance(gate, Rz):
                    repr_as_dict[str(counter)] = {"theta": gate.theta, "carrier": gate.lev, "particle": j, "type": 'z'}


                elif isinstance(gate, R):
                    repr_as_dict[str(counter)] = {"theta": gate.theta, "phi": gate.phi, "carrier": temp[str((gate.lev_a, gate.lev_b))], "particle": j , "type": 'g'}

                counter += 1

        with open( absolute_path+name+'.json', 'w') as fp:
            json.dump(repr_as_dict, fp)

    ####################################################################
    #
    #               DECOMPOSITION
    #
    ####################################################################

    def Z_prop(self, back):
        remove_Z(self, back)

    def DFS_decompose(self):

        new_qreg = []

        for line in self.qreg:

            clean_line = []

            for gate in line:
                QR = QR_decomp(gate, self.energy_level_graph)

                decomp, algorithmic_cost, total_cost = QR.execute()

                Adaptive = Adaptive_decomposition(gate, self.energy_level_graph, (algorithmic_cost, total_cost),
                                                  self.dimension)

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
