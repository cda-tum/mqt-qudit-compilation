from r_utils import *
from Rotations import *

def algorithm(U , circ):
    
    decomp=[]
    total_cost = 0
    
    U_ = U
    dimension= U.shape[0]
    print("dimension is "+str(dimension))
    

    l=list(range(U.shape[0]))
    l.reverse()
    
    for c in range(U.shape[1]):
        
        diag_index = l.index(c)
        
        for r in l[:diag_index]:

            if( abs(U_[r,c])>1.0e-8 and abs(U_[r-1,c])>1.0e-4  ): ###check error change loop
                
                print("=======================================================")
                print(' r is '+str(r))
                print(' c is '+str(c))
                print("=======================================================")
                
                theta = 2 * np.arctan( abs(U_[r,c]/U_[r-1,c]))
                
                phi = -(np.angle(U_[r-1,c]) - np.angle(U_[r,c]))
                
                print(theta)
                print(phi)
                
                print(U_.round(4))
                rotation_involved = R(theta,phi,r-1,r,dimension)
                
                U_ = matmul(rotation_involved.matrix, U_)
                
                print('---')
                print(U_.round(4))
                
                print('@@@@@@@')
                print(rotation_involved.matrix.round(4))
                print()
                


                
                non_zeros = np.count_nonzero(abs(U_)>1.0e-4)
                print("non-zeros:   "+ str(non_zeros))

                flag_pi_pulses, estimated_cost = cost_calculator(rotation_involved, circ.energy_level_graph, non_zeros)
                print("estimated_cost :   "+str(estimated_cost))

                #pi pulse append without checking if it could multiple ones

                decomp.append(PI_PULSE())
                decomp.append(rotation_involved)

                total_cost += estimated_cost

                
    """Change of plans since the matrices now are sigle entry the linear system is just an identity matrix arg[diag(U)] 
    """
    diag_U = np.diag(U_)
    print("Extracting The Z gates in a standard way")
    for i in range(dimension):
        
        if( abs(np.mod(np.angle(diag_U[i]),1.0e-13))> 1.0e-4):
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

    return decomp, total_cost
