from binq.src.circuit.Rotations import *
from binq.src.utils.costs_utils import *
from binq.src.utils.r_utils import *


class QR_decomp:

    def __init__(self, gate , graph_orig):

        self.U = gate.matrix
        self.graph = graph_orig

    def execute(self):

        decomp=[]
        total_cost = 0
        algorithmic_cost = 0

        U_ = self.U
        dimension= self.U.shape[0]


        l=list(range(self.U.shape[0]))
        l.reverse()

        for c in range(self.U.shape[1]):

            diag_index = l.index(c)

            for r in l[:diag_index]:

                if( abs(U_[r,c])>1.0e-8 and abs(U_[r-1,c])>1.0e-4  ): ###check error change loop


                    theta = 2 * np.arctan( abs(U_[r,c]/U_[r-1,c]))

                    phi = -(np.angle(U_[r-1,c]) - np.angle(U_[r,c]))

                    rotation_involved = R(theta,phi,r-1,r,dimension)

                    U_ = matmul(rotation_involved.matrix, U_)



                    non_zeros = np.count_nonzero(abs(U_)>1.0e-4)


                    estimated_cost, pi_pulses_routing, unused_placement, cost_of_pi_pulses, gate_cost = cost_calculator(rotation_involved, self.graph, non_zeros)



                    # PI PULSES ROTATION TO U
                    # ROTATION TO U
                    # PI PULSES ROTATION TO U

                    #pi pulse append without checking if it could multiple ones

                    decomp += pi_pulses_routing
                    physical_rotation = R( theta, phi, self.graph.nodes[r-1]['lpmap'], self.graph.nodes[r]['lpmap'], dimension)
                    decomp.append(physical_rotation)

                    for pi_g in reversed(pi_pulses_routing):
                        pi_g.matrix = pi_g.dag
                        decomp.append(pi_g) #reversed and dag

                    algorithmic_cost += estimated_cost
                    total_cost += 2*cost_of_pi_pulses+gate_cost




        """Change of plans since the matrices now are sigle entry the linear system is just an identity matrix arg[diag(U)] 
        """
        diag_U = np.diag(U_)
        print("Extracting The Z gates in a standard way")
        for i in range(dimension):

            if( abs(np.angle(diag_U[i])> 1.0e-4)):
                print("theta rotation :  ", np.angle(diag_U[i]))

                print("U before phase rotation")
                print(U_.round(4))
                phase_gate = Rz(np.angle(diag_U[i]), i, dimension)

                U_ = matmul(phase_gate.matrix, U_)

                print('---')
                print("U after phase rotation")
                print(U_.round(4))

                print('@@@@@@@')
                print(phase_gate.matrix.round(4))
                print('@@@@@@@')
                print()

                decomp.append( phase_gate )


        print("TOTAL COST: ", total_cost)

        return decomp, algorithmic_cost, total_cost
