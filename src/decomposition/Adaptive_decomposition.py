from src.Exceptions.Exceptions import SequenceFoundException
from src.circuit.Rotations import *
from src.circuit.swap_routines_basic import gate_chain_condition, phase_storage_processing
from src.decomposition.tree_struct import N_ary_Tree

from src.utils.costs_utils import *
from src.utils.r_utils import *
np.seterr(all='ignore')

class Adaptive_decomposition:


    def __init__(self, gate, graph_orig, cost_limit=(0,0), dimension = -1):
        self.U = gate.matrix

        self.graph = graph_orig
        self.graph.phase_storing_setup()

        self.cost_limit = cost_limit
        self.dimension = dimension

        self.TREE = N_ary_Tree()

    def execute(self):

        self.TREE.add(0, custom_Unitary(np.identity(self.dimension, dtype='complex'), self.dimension), self.U, self.graph, 0, 0, self.cost_limit, [])
        try:
            self.DFS(self.TREE.root)
        except SequenceFoundException:
            pass
        finally:
            matrices_decomposed, best_cost, final_graph = self.TREE.retrieve_decomposition(self.TREE.root)

            if(matrices_decomposed!=[]):
                matrices_decomposed, final_graph = self.Z_extraction(matrices_decomposed, final_graph)
            else:
               print("couldn't decompose\n")

            tree_print = self.TREE.print_tree(self.TREE.root, "TREE: ")
           #print(tree_print)

            return matrices_decomposed, best_cost, final_graph








    def Z_extraction(self, decomposition, placement, phase_propagation=False):

        matrices = []

        for d in decomposition[1:]: #exclude the identity matrix coming from the root of the tree of solutions which is just for correctness
            matrices = matrices + d.PI_PULSES
            matrices = matrices + [d.rotation]


        U_ = decomposition[-1].U_of_level #take U of last elaboration which should be the diagonal matrix found
        ###########################################################################################################

        # check if close to diagonal
        Ucopy = U_.copy()

        # is the diagonal noisy?
        valid_diag = any(abs(np.diag(Ucopy)) > 1.0e-4) # > 1.0e-4
       #print("valid: " + str(valid_diag))

        # are the non diagonal entries zeroed-out
        filtered_Ucopy = abs(Ucopy) > 1.0e-4
        np.fill_diagonal(filtered_Ucopy, 0)

        not_diag = filtered_Ucopy.any()


        if ( not_diag or not valid_diag):  # if is diagonal enough then somehow signal end of algorithm
            raise Exception('Matrix isnt close to diagonal!')
        else:
            diag_U = np.diag(U_)
            dimension = U_.shape[0]

            for i in range(dimension):   #TODO take care of this variable because imported globally

                if( abs(np.angle(diag_U[i]))> 1.0e-4):

                    if (phase_propagation):
                        inode = self._1stInode
                        if ('phase_storage' in self.nodes[inode]):
                            placement.nodes[i]['phase_storage'] = placement.nodes[i]['phase_storage'] + np.angle(diag_U[i])
                    else:
                        phy_n_i = placement.nodes[i]['lpmap']

                        phase_gate = Rz( np.angle(diag_U[i]), phy_n_i, dimension)

                        U_ = matmul( phase_gate.matrix, U_)

                        matrices.append( phase_gate )

            return matrices, placement



    def DFS(self, current_root,   level = 0):


        # check if close to diagonal
        Ucopy = current_root.U_of_level.copy()

        current_placement = current_root.graph


        #is the diagonal noisy?
        valid_diag = any(abs(np.diag(Ucopy))> 1.0e-4)


        # are the non diagonal entries zeroed-out
        filtered_Ucopy = abs(Ucopy) > 1.0e-4
        np.fill_diagonal(filtered_Ucopy, 0)

        not_diag = filtered_Ucopy.any()


        if( (not not_diag) and valid_diag ):# if is diagonal enough then somehow signal end of algorithm

            current_root.finished = True

            raise SequenceFoundException(current_root.key)

            #just in case something happens
            return

        U_ = current_root.U_of_level

        dimension = U_.shape[0]



        for c in range(dimension):

            for r in range(c, dimension):

                for r2 in range(r+1, dimension):


                    if (abs(U_[r2, c]) > 1.0e-8 and (abs(U_[r,c])>1.0e-18 or abs(U_[r,c])==0  ) ):


                        theta = 2 * np.arctan2( abs(U_[r2, c]), abs(U_[r, c]) )

                        phi = -( np.pi/2 + np.angle(U_[r,c]) - np.angle(U_[r2,c]))


                        rotation_involved = R(theta, phi,r, r2, dimension)

                        U_temp = matmul(  rotation_involved.matrix, U_ )

                        non_zeros = np.count_nonzero(abs(U_temp)>1.0e-4)


                        estimated_cost, pi_pulses_routing, new_placement, cost_of_pi_pulses, gate_cost = cost_calculator(rotation_involved, current_placement, non_zeros)

                        next_step_cost = (estimated_cost + current_root.current_cost)
                        decomp_next_step_cost = ( cost_of_pi_pulses + gate_cost + current_root.current_decomp_cost)

                        branch_condition = current_root.max_cost[1] - decomp_next_step_cost #SECOND POSITION IS PHYISCAL COST
                        branch_condition_2 = current_root.max_cost[0] - next_step_cost  # FIRST IS ALGORITHMIC COST

                        if(  branch_condition > 0 or abs(branch_condition) < 1.0e-12): #if cost is better can be only candidate otherwise try them all

                            if (new_placement.nodes[r ]['lpmap'] > new_placement.nodes[r2]['lpmap']):
                                phi = phi * -1

                            physical_rotation = R(theta, phi, new_placement.nodes[r]['lpmap'],new_placement.nodes[r2]['lpmap'], dimension)

                            physical_rotation = gate_chain_condition(pi_pulses_routing, physical_rotation)

                            ##############################
                            physical_rotation, new_placement = phase_storage_processing(physical_rotation, new_placement)
                            """
                            ################# EXPERIMENT###############################
                            for pipi in pi_pulses_routing:

                                logic_nodes = [None, None]
                                for n, d in new_placement.nodes(data=True):
                                    if (d['lpmap'] == pipi.lev_a):
                                        logic_nodes[0] = n
                                    if (d['lpmap'] == pipi.lev_b):
                                        logic_nodes[1] = n

                                #U_temp = matmul( pipi.matrix, U_temp)
                                U_temp = matmul( R(pipi.theta,pipi.phi, logic_nodes[0] , logic_nodes[1], pipi.dimension  ).matrix, U_temp)

                                U_temp = matmul(Rz(np.pi, logic_nodes[1], dimension).matrix,  U_temp)

                            ################# REMOVE EXPERIMENT###############################
                            """
                            self.TREE.global_id_counter = self.TREE.global_id_counter +1
                            new_key = self.TREE.global_id_counter

                            if(new_key in [0,1,5,8]):
                                lll = 0
                            current_root.add(new_key, physical_rotation, U_temp, new_placement, next_step_cost, decomp_next_step_cost, current_root.max_cost, pi_pulses_routing)



        if( current_root.children != None):

            for child in current_root.children:
                self.DFS(child, level+1)
        #===================================================================================

        return



