from binq.src.Exceptions.Exceptions import SequenceFoundException
from binq.src.circuit.Rotations import *
from binq.src.decomposition.tree_struct import N_ary_Tree

from binq.src.utils.costs_utils import *
from binq.src.utils.r_utils import *


class Adaptive_decomposition:


    def __init__(self, gate, graph_orig, cost_limit=(0,0), dimension = -1):
        self.U = gate.matrix
        self.graph = graph_orig
        self.cost_limit = cost_limit
        self.dimension = dimension

        self.TREE = N_ary_Tree()

    def execute(self):

        self.TREE.add(0, custom_Unitary(np.identity(self.dimension, dtype='complex'), self.dimension), self.U, self.graph, 0, 0, self.cost_limit, [])
        try:
            print("WAIT FOR ADAPTIVE...")
            self.DFS(self.TREE.root)
            print("ADAPTIVE FINISHED\n")
        except SequenceFoundException:
            pass
        finally:
            matrices_decomposed, best_cost, final_graph = self.TREE.retrieve_decomposition(self.TREE.root)

            if(matrices_decomposed!=[]):
                matrices_decomposed = self.Z_extraction(matrices_decomposed)
            else:
                print("couldn't decompose\n")

            tree_print = self.TREE.print_tree(self.TREE.root, "TREE: ")
            print(tree_print)

            return matrices_decomposed, best_cost, final_graph








    def Z_extraction(self, decomposition):
        print("Z EXTRACTION INITIATED")
        ###########################################################################################################
        matrices = []

        for d in decomposition[1:]: #exclude the identity matrix coming from the root of the tree of solutions which is just for correctness
            matrices = matrices + d.PI_PULSES
            matrices = matrices + [d.rotation]


        U_ = decomposition[-1].U_of_level #take U of last elaboration which should be the diagonal matrix found
        ###########################################################################################################

        # check if close to diagonal
        Ucopy = U_.copy()

        # is the diagonal noisy?
        valid_diag = (abs(np.diag(Ucopy)) > 1.0e-4).sum()  # > 1.0e-4
        print("valid: " + str(valid_diag))

        # are the non diagonal entries zeroed-out
        filtered_Ucopy = abs(Ucopy) > 1.0e-4
        np.fill_diagonal(filtered_Ucopy, 0)

        not_diag = filtered_Ucopy.sum(axis=0).sum()
        print("not_diag: " + str(not_diag))
        #---------------------------------------------------------------------------------------------------------------------

        if ( not_diag or not valid_diag):  # if is diagonal enough then somehow signal end of algorithm
            raise Exception('Matrix isnt close to diagonal!')
        #@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=#@=
        else:
            diag_U = np.diag(U_)
            dimension = U_.shape[0]      # TODO eay fix

            for i in range(dimension):   #TODO take care of this variable because imported globally

                if( abs(np.angle(diag_U[i])> 1.0e-4)):
                    print("theta rotation :  ", np.angle(diag_U[i]))

                    print("U before phase rotation")
                    print(U_.round(4))
                    phase_gate = Rz( np.angle(diag_U[i]), i, dimension)

                    U_ = matmul( phase_gate.matrix, U_)

                    print('---')
                    print("U after phase rotation")
                    print(U_.round(4))

                    print('@@@@@@@')
                    print(phase_gate.matrix.round(4))
                    print('@@@@@@@')
                    print()
                    matrices.append( phase_gate )


            return matrices










    def DFS(self, current_root,   level = 0):
        print(".",  end="")
        #######################

        # check if close to diagonal
        Ucopy = current_root.U_of_level.copy()
        current_placement = current_root.graph


        #is the diagonal noisy?
        valid_diag = (abs(np.diag(Ucopy))> 1.0e-4).sum() #> 1.0e-4
        #print("valid: "+ str(valid_diag))

        # are the non diagonal entries zeroed-out
        filtered_Ucopy = abs(Ucopy) > 1.0e-4
        np.fill_diagonal(filtered_Ucopy, 0)

        not_diag = filtered_Ucopy.sum(axis=0).sum()
        #print("not_diag: "+ str(not_diag))
        ############################################

        if( (not not_diag) and valid_diag ):# if is diagonal enough then somehow signal end of algorithm
            #print("condition 2")

            print(current_root.U_of_level)
            print(current_root.key)

            print("\n\n ARRIVED\n\n")

            current_root.finished = True

            raise SequenceFoundException(current_root.key)

            #just in case something happens
            return



        #----------------------------------


        ## CHECKING FOR BEST CHOICE ON CERTAIN STEP
        U_ = current_root.U_of_level

        dimension = U_.shape[0]
        #print("dimension is "+str(dimension))

        #print("checking level")
        for c in range(dimension):

            for r in range(dimension):

                for r2 in range(r, dimension):

                    if( abs(U_[r,c])>1.0e-8 and abs(U_[r2,c])>1.0e-4 and r >= c and r2 > r):

                        theta = 2 * np.arctan( abs(U_[r2,c]/U_[r,c]))
                        phi = -(np.angle(U_[r,c]) - np.angle(U_[r2,c]))


                        rotation_involved = R(theta, phi,r, r2, dimension)

                        U_temp = matmul(  rotation_involved.matrix, U_ )
                        U_temp = U_temp.round(12)


                        non_zeros = np.count_nonzero(abs(U_temp)>1.0e-4)


                        estimated_cost, pi_pulses_routing, new_placement, cost_of_pi_pulses, gate_cost = cost_calculator(rotation_involved, current_placement, non_zeros)

                        next_step_cost = (estimated_cost + current_root.current_cost)
                        decomp_next_step_cost = ( cost_of_pi_pulses + gate_cost + current_root.current_decomp_cost)

                        branch_condition = current_root.max_cost[1] - decomp_next_step_cost #SECOND POSITION IS PHYISCAL COST
                        branch_condition_2 = current_root.max_cost[0] - next_step_cost  # FIRST IS ALGORITHMIC COST

                        if(  branch_condition > 0 or abs(branch_condition) < 1.0e-12): #if cost is better can be only candidate otherwise try them all
                            if (branch_condition_2 > 0 or abs(branch_condition_2) < 1.0e-12):


                                new_key = current_root.key + (current_root.size + 1)

                                #TODO FIX KEY SYSTEM BECAUSE NOT UNIQUE

                                physical_rotation = R(theta, phi, new_placement.nodes[r]['lpmap'],new_placement.nodes[r2]['lpmap'], dimension)

                                current_root.add(new_key, physical_rotation, U_temp, new_placement, next_step_cost, decomp_next_step_cost, current_root.max_cost, pi_pulses_routing)



        if( current_root.children != None):
            # sort children by minimum cost, in order to get closer to minimum cost paths
            #current_root.children = sorted(current_root.children, key=lambda x: x.current_cost)

            for child in current_root.children:
                self.DFS(child, level+1)
        #===================================================================================

        return



