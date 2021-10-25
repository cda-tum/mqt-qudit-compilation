################## CIRCUIT

###                  ALL THE CLASSES HAVE TO BE REFACTORED TO FOLLOW DESIGN PATTERNS


from binq.src.decomposition.Adaptive_decomposition import *
from binq.src.decomposition.tree_struct import *
from binq.src.architecture_graph.level_Graph import *
from binq.src.utils.costs_utils import *


class QuantumCircuit:
    
    def __init__(self, qubits, bits, dimension):
        
        self.qubits = list(range(qubits))
        self.bits = list(range(bits))
        self.qreg = [[] for x in range(qubits)] 
        self.reg = [[] for x in range(bits)] 
        self.dimension = dimension
        self.energy_level_graph = None
        
    def R(self, qubit_line, theta, phi, lev_a, lev_b ):
        
        self.qreg[qubit_line].append( R(theta, phi, lev_a, lev_b , self.dimension))

    def PI_PULSE(self, qubit_line, lev_a, lev_b, additional_bookmark, seq_flag):

        self.qreg[qubit_line].append( PI_PULSE(lev_a, lev_b, additional_bookmark, seq_flag, self.dimension))

        
    def Rz(self, qubit_line, theta, lev):
        
        self.qreg[qubit_line].append( Rz(theta, lev, self.dimension))
        
    def custom_unitary(self, qubit_line, unitary):
        
        self.qreg[qubit_line].append( custom_Unitary(unitary, self.dimension) )

    def energy_level_graph(self, edges):
        self.energy_level_graph = level_Graph( edges, self.dimension)


#@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=
    ####################################################################
    ####################################################################
    ####################################################################

    ####            Z GATES PROPAGATION

    ####################################################################
    ####################################################################
    ####################################################################

    
    def tag_generator(self, gates):
        tag_number = 0
        tags = []
        is_reset = False

        for g in gates:
            if(isinstance(g,Rz) and is_reset):
                tag_number+=1
                is_reset = False
            else:
                is_reset = True

            tags.append(tag_number)


        return tags



    def propagate_Z(self, line_num):
        line = self.qreg[line_num]

        tags = self.tag_generator(line)

        list_of_Zrots = []
        list_of_XYrots = []
        fixed_sequence = []

        for gate_index in range(len(line)):

            if(isinstance( line[gate_index] , Rz)):

                list_of_Zrots.append( ( line[gate_index] , tags[gate_index] ))

            elif(isinstance( line[gate_index],  R)):

                list_of_XYrots.append(( line[gate_index] , tags[gate_index] ))

        levels = {}

        for gate_tuple in list_of_Zrots:

            Rz_gate_i =  gate_tuple[0]
            Rz_gate_tag = gate_tuple[1]

            key1 = Rz_gate_i.lev
            key2 = Rz_gate_tag


            if key1 in levels:
                if key2 in levels[key1]:

                    for tag in levels[key1]:
                        if(tag < key2):

                            levels[key1][tag]  = np.mod( (levels[key1][tag]  + Rz_gate_i.theta), 2*np.pi)

                            levels[key1][key2] += Rz_gate_i.theta
                else:
                    for tag in levels[key1]:
                        if (tag < key2):
                            levels[key1][tag] = np.mod((levels[key1][tag] + Rz_gate_i.theta), 2 * np.pi)

                            levels[key1][key2] = Rz_gate_i.theta

            else:
                levels[key1] = {}
                levels[key1][key2] =  Rz_gate_i.theta


        for gate_tuple in list_of_XYrots:
            R_gate_i =  gate_tuple[0]
            R_gate_tag = gate_tuple[1]


            phi = 0

            if( R_gate_i.lev_a in levels):
                for z_tags in levels[ R_gate_i.lev_a ]:
                    if(z_tags > R_gate_tag):
                        phi += levels[R_gate_i.lev_a][z_tags]

            if( R_gate_i.lev_b in levels):
                for z_tags in levels[R_gate_i.lev_b]:
                    if (z_tags > R_gate_tag):
                        phi -= levels[R_gate_i.lev_b][z_tags]

            old_phi = R_gate_i.phi

            new_phi = np.mod( (old_phi + phi) , 2*np.pi)

            fixed_sequence.append( R( R_gate_i.theta, new_phi, R_gate_i.lev_a, R_gate_i.lev_b, R_gate_i.dimension ) )

        self.qreg[line_num] = fixed_sequence
        
        return fixed_sequence
    
    #----------------------------------------------------------------------------
    
    def remove_Z(self):

        for num_line in range(len(self.qreg)):

            self.qreg[num_line] = self.propagate_Z(num_line)

        return



# @@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=@@@=@=@=
    ####################################################################
    ####################################################################
    ####################################################################
    #
    #               DECOMPOSITION
    #
    ####################################################################
    ####################################################################
    ####################################################################

    #### badly implemented to refactor
    ## TODO REIMPLEMENT, OLD VERSION NOT ALIGNED



    def decompose(self, algorithm=None):

        new_qreg = []

        for line in self.qreg:
            
            clean_line = []
            
            for gate in line:

                standard_decomposition, standard_cost = algorithm(gate.matrix, self.energy_level_graph)

                if(type_alg=="BFS"):
                    TREE = N_ary_Tree()
                    TREE.add(0, custom_Unitary(np.identity(self.dimension, dtype='complex'), 3), gate, 0, standard_cost)

                    BFS(TREE.root)

                    BFS_decomposition, BFS_cost = TREE.retrieve_decomposition(TREE.root)
                    matrices_decomposed = self.Z_extraction(BFS_decomposition)

                    clean_line = clean_line + matrices_decomposed
                else:
                    clean_line = clean_line + standard_decomposition

            new_qreg.append(clean_line)

            self.qreg = new_qreg

    ####################################################################
    ####################################################################
    ####################################################################
    #
    #               SWAPPING ROUTINES (- integrated)
    #
    ####################################################################
    ####################################################################
    ####################################################################

    def swap_route_levels(self, qubit_line, lev_a, lev_b):
        #TODO TODO COMPLETE INTEGRATION IN QUANTUM CIRCUIT

        if(lev_a == lev_b):
            raise Exception

        else:
            dist = self.energy_level_graph.distance_nodes(lev_a, lev_b)

            additional_bookmark = self.get_bookmark( lev_a, lev_b)

            if(dist > 1):
                path = self.energy_level_graph.shortest_path(self, lev_a, lev_b)
                #TODO IN CASE TO REWRITE FOR ARBITRARY SORTING
                self.PI_PULSE( qubit_line, path[0], path[1], additional_bookmark, True)
                self.PI_PULSE( qubit_line, path[1], path[2], additional_bookmark, True)
                self.PI_PULSE( qubit_line, path[0], path[1], additional_bookmark, True)

            else:
                self.PI_PULSE(qubit_line, lev_a, lev_b, additional_bookmark, False)

            self.energy_level_graph.swap_nodes(lev_a, lev_b)

